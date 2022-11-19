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


def plot_data(data: pd.DataFrame, dropdown_selection, log, results):

    # TODO add in rest of graphs

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
        fig = px.bar(data.head(results), x="Sport", y="Medal", log_y=log)

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
        data = data[data["Team"].isin(data["Team"].head(results))]
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

    return style(fig)
