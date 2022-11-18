import os
import dash

from layout import Layout
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
import plotly_express as px

# for navigating relatively to the absolute path of this directory
dir_path = os.path.dirname(__file__)
path = os.path.join(dir_path, "path")  # placeholder "path" for now

app = dash.Dash(
    # using __name__ instead of hard typed name allows us to use "main" when deploying dashboard and __main__ when running from this file
    __name__,
    # using theme SUPERHERO because we have USA ;)
    external_stylesheets=[
        dbc.themes.SUPERHERO,
    ],
    # meta tag used for responsiveness in dashboard (resizing based on screen size)
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale = 1"}
    ],
)

# setting the dashboard layout based on imported layout module
# (creating an instance of Layout class)
df = pd.read_csv("Data/athlete_events.csv")
a = Layout(df)
app.layout = a.layout()  # df_athlete["Year"].min(), df_athlete["Year"].max()

# Setting up colors commonly used throughout the dashboard, these will be used in styling graphs
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


@app.callback(
    Output("graph-id", "figure"),
    Input("dropdown", "value"),
    Input("log-buttons", "value"),
    Input("season-picker", "value"),
    Input("year-slider", "value"),
)
def update_graph(dropdown_option, log, season, slider):

    # temp variables (will be used with buttons later)
    country = ""  # will use all countries if none is set
    sport = ""

    data = df
    data = data[data["Season"].isin([*season])]

    if slider:  # because slider doesn't start with values set when loading page
        data = data[data["Year"].between(min(slider), max(slider))].sort_values(
            by="Year", ascending=False
        )
        # filtering out results between min and max slider values

    if country:  # "" -> False
        data = data[data["Team"] == country]

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
        # moving title to the middle of the screen, and anchoring it to the center, and changing font size
        # title=dict(x=0.5, xanchor="center", font=dict(size=25)),
        # updating text and background colors of the figure
        font=dict(color=text),
        plot_bgcolor=element,
        paper_bgcolor=background,
    )

    return fig


if __name__ == "__main__":
    # run app if script is run from main
    app.run_server(debug=True)  # TODO remove from debug mode before deploying
