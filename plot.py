import pandas as pd
import plotly_express as px

# Script for plotting DataFrame based on dropdown selection


def style(fig):
    """
    Takes figure object, returns styled figure object -
    Updates the colorscheme of a given figure to match that of the dashboard
    """

    # colors used for styling figure
    bg_color = "#0F2537"
    white_ish = "#EBEBEB"

    fig.update_layout(
        # updating text and background colors of the figure
        font=dict(color=white_ish),
        plot_bgcolor=white_ish,
        paper_bgcolor=bg_color,
    )
    return fig


def plot_data(data: pd.DataFrame, dropdown_selection, log, amount_results):
    """
    Takes a filtered dataset and returns a graph object based on:
    dropdown_selection, log, amount_results which are all values of elements in layout.py with respective ID
    """

    if len(data) < 1:  # if all data was filtered out
        # return an empty graph to show that no data was found matching the specific selection
        # also prevents potential errors in trying to plot based on an empty dataframe
        fig = px.line(title="No data for this selection")
        return style(fig)

    if dropdown_selection == "Medals USA":
        # NOTE code for this plot from Max

        country_condition = ["United States"]
        data = data[data["Team"].isin(country_condition)]

        data = (
            data[["Sport", "Medal"]]
            .groupby("Sport")
            .count()
            .reset_index()
            .sort_index()
            .sort_values(by="Medal", ascending=False)
        )

        # plotting based on parameters
        fig = px.bar(
            data.head(amount_results),
            x="Sport",
            y="Medal",
            log_y=log,
            title="Medals USA",
        )

    if dropdown_selection[7:] in ["Basketball", "Boxing", "Football", "Ice Hockey"]:
        # NOTE code for this plot from Elias

        sport = dropdown_selection[7:]
        data = data[data["Sport"] == sport]

        data = data[["Age", "Team", "Medal"]]

        # remove all rows where the medal is NaN
        data = data[data["Medal"].notna()]  # notna() is the same as isnull() == False

        # use groupby to group the data by Team and Medal
        data = data.groupby(["Team", "Medal"])
        data = data.size()  # size() counts the number of rows in each group
        data = data.reset_index(
            name="Count"
        )  # reset_index(name="Count") resets the index and adds a new column named Count

        # -----
        # NOTE: code to be able to use amount of results slider for this graph - by andreas
        # set a value corresponding to each medal type
        custom_dict = {
            "Gold": 0,
            "Silver": 1,
            "Bronze": 2,
        }
        # create a column based on dict values
        data["rank"] = data["Medal"].map(custom_dict)
        # sort by those values primarily, and the count secondarily
        # this results in gold high amount -> low amount, silver high amount -> low amount, bronze high amount -> low amount
        data.sort_values(by=["rank", "Count"], ascending=[True, False], inplace=True)
        # then pick out head(amount_results) to get all 3 medal types, for the top n teams in terms of most gold -> silver -> bronze medals
        data = data[data["Team"].isin(data["Team"].head(amount_results))]
        # -----

        # sort by count of gold medals
        # data = data.sort_values(by=["Count"], ascending=False).reset_index(drop=True)

        # plot the data change the color of medel to gold, silver, bronze.
        fig = px.bar(
            data,  # .head(50),
            x="Team",
            y="Count",
            log_y=log,
            color="Medal",
            # barmode="group",
            category_orders={"Medal": ["Gold", "Silver", "Bronze"]},
            color_discrete_sequence=["gold", "silver", "brown"],
            title="Medal distribution for boxing",
        )

    if dropdown_selection == "Gender Distribution":
        # NOTE code for this plot from Andreas

        data = data.sort_values(by="Year").reset_index(drop=True)

        # dictionary of series title and filtered content from data:
        columns = {
            "Men Global": data[data["Sex"] == "M"].groupby(["Year"]).count()["Sex"],
            "Women Global": data[data["Sex"] == "F"].groupby(["Year"]).count()["Sex"],
            "Combined Global": data.groupby(["Year"]).count()["Sex"],
            "Men USA": data[(data["Sex"] == "M") & (data["NOC"] == "USA")]
            .groupby(["Year"])
            .count()["Sex"],
            "Women USA": data[(data["Sex"] == "F") & (data["NOC"] == "USA")]
            .groupby(["Year"])
            .count()["Sex"],
            "Combined USA": data[data["NOC"] == "USA"].groupby(["Year"]).count()["Sex"],
        }
        # creating new dataframe from dictionary containing the (absolute) amount of gender participants of each game
        df_genders = pd.DataFrame(columns)

        # creating a dictionary of relative amount from absolute amount dataframe
        columns = {
            "Amount Men Global": (
                df_genders["Men Global"] / df_genders["Combined Global"]
            ),
            "Amount Women Global": (
                df_genders["Women Global"] / df_genders["Combined Global"]
            ),
            "Amount Men USA": (df_genders["Men USA"] / df_genders["Combined USA"]),
            "Amount Women USA": (df_genders["Women USA"] / df_genders["Combined USA"]),
        }

        # creating new dataframe from dictionary containing the (relative) amount of gender participants of each game
        df_genders_amount = (
            pd.DataFrame(columns)
            .sort_values(by="Year", ascending=False)
            .head(amount_results)
        )

        # replacing years where no people attended with 0 to better show visually in the graph
        df_genders_amount.fillna(0, inplace=True)

        # list of all series to plot
        lines = [
            "Amount Men Global",
            "Amount Women Global",
            "Amount Men USA",
            "Amount Women USA",
        ]

        # plotting series
        fig = px.line(
            df_genders_amount,
            x=df_genders_amount.index,
            y=lines,
            title="Gender Distribution of Olympic Athletes over time",
            labels={"variable": "Amount", "value": "Amount"},
            log_y=log,
        )

        # styling traces based on what they show
        for trace in lines:
            color = "blue" if "Men" in trace else "red"
            dash = "solid" if "Global" in trace else "dot"
            fig.update_traces(
                patch={"line": {"color": color, "dash": dash}},
                # specifying which line to apply style to
                selector={"legendgroup": trace},
            )

    return style(fig)
