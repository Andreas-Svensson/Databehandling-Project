import plotly_express as px

# Script for plotting DataFrame based on dropdown selection


# Setting up colors commonly used throughout the dashboard, these will be used in styling graphs
# TODO decide on final colors
flag_red = "#8A2234"
flag_blue = "#3C3B6E"
colors = {
    "Gold": "#e7c024",
    "Silver": "#a1e1e1",
    "Bronze": "#e78224",
    "Summer": "#ee7722",
    "Winter": "#22ccff",
}
background = "#0F2537"
element = "#4E5D6C"
text = "#EBEBEB"
highlight = "#02D2D5"


def plot_data(data, dropdown_selection, log):

    # NOTE: currently plotting the same graph regardless of selection
    # TODO add in rest of graphs

    if dropdown_selection:  # == "Medals in USA":
        data = (
            data[["Sport", "Medal"]]
            .groupby("Sport")
            .count()
            .reset_index()
            .sort_index()
            .sort_values(by="Medal", ascending=False)
        )

        # plotting based on parameters
        fig = px.bar(data, x="Sport", y="Medal", log_y=log)

        # color="Year",
        # color_discrete_map=colors
        # color_discrete_map="Årstid"
        # title=dropdown_option,

        # Updating fig with colors
        fig.update_layout(
            # TODO does the fig need a title, or can the text in the dropdown be used instead?
            # moving title to the middle of the screen, and anchoring it to the center, and changing font size
            # title=dict(x=0.5, xanchor="center", font=dict(size=25)),
            # updating text and background colors of the figure
            font=dict(color=text),
            plot_bgcolor=element,
            paper_bgcolor=background,
        )

        return fig

    print("no graph was created in plot data")
    pass  # TODO put return fig here when all plots are ready
