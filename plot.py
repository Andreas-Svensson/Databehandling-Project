import pandas as pd
import plotly_express as px

# Script for plotting DataFrame based on dropdown selection


# Setting up colors commonly used throughout the dashboard, these will be used in styling graphs
# TODO decide on final colors
colors = {
    "Gold": "#e7c024",
    "Silver": "#a1e1e1",
    "Bronze": "#e78224",
    "Summer": "#ee7722",
    "Winter": "#22ccff",
}
flag_red = "#8A2234"
flag_blue = "#3C3B6E"
background = "#0F2537"
element = "#4E5D6C"
text = "#EBEBEB"
highlight = "#02D2D5"


def style(fig):

    fig.update_layout(
        # TODO does the fig need a title, or can the text in the dropdown be used instead?
        # moving title to the middle of the screen, and anchoring it to the center, and changing font size
        # title=dict(x=0.5, xanchor="center", font=dict(size=25)),
        # updating text and background colors of the figure
        font=dict(color=text),
        plot_bgcolor=text,
        paper_bgcolor=background,
    )
    return fig


def plot_data(data: pd.DataFrame, dropdown_selection, log, amount_results):

    if len(data) < 1:  # if all data was filtered out
        # return an empty graph (to prevent any errors in trying to plot based on an empty dataframe)
        fig = px.line(title="No data for this selection")
        return style(fig)

    if dropdown_selection == "Medals Total":
        data = (
            data[["Sport", "Medal"]]
            .groupby("Sport")
            .count()
            .reset_index()
            .sort_index()
            .sort_values(by="Medal", ascending=False)
        )

        # plotting based on parameters
        fig = px.bar(data.head(amount_results), x="Sport", y="Medal", log_y=log)

        # color="Year",
        # color_discrete_map=colors
        # color_discrete_map="Årstid"
        # title=dropdown_option,

    if dropdown_selection[7:] in ["Basketball", "Boxing", "Football", "Ice Hockey"]:
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

        # NOTE test code by andreas
        custom_dict = {"Gold": 0, "Silver": 1, "Bronze": 2}
        data["rank"] = data["Medal"].map(custom_dict)
        data.sort_values(by=["rank", "Count"], ascending=[True, False], inplace=True)
        data = data[data["Team"].isin(data["Team"].head(amount_results))]
        # ---

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
        """Plotting gender representation comparison between US and globally over time"""

        data = data.sort_values(by="Year", ascending=False).reset_index(drop=True)

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
            title="Gender Distribution of OS Competitors over time",
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
