import os
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
import plotly_express as px

# importing scripts from this project:
from layout import Layout
from filter import filter_data, set_default_filters
from plot import plot_data

# for navigating relatively to the absolute path of this directory
dir_path = os.path.dirname(__file__)
path = os.path.join(dir_path, "path")  # placeholder "path" for now

# using __name__ instead of hard typed name allows us to use "main" when deploying dashboard and __main__ when running from this file
# using theme SUPERHERO because we have USA ;)
# meta tag used for responsiveness in dashboard (resizing based on screen size)
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SUPERHERO],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale = 1"}
    ],
)

# setting the dashboard layout based on imported layout module
# (creating an instance of Layout class)
df = pd.read_csv("Data/athlete_events.csv")
app.layout = Layout(df).layout()


@app.callback(
    Output("log-buttons", "value"),
    Output("season-picker", "value"),
    Output("year-slider", "value"),
    Output("amount-results-slider", "value"),
    Input("dropdown", "value"),
)
def set_default_options(dropdown_selection):
    return set_default_filters(df, dropdown_selection)


@app.callback(
    Output("graph-id", "figure"),
    Input("dropdown", "value"),
    Input("log-buttons", "value"),
    Input("season-picker", "value"),
    Input("year-slider", "value"),
    Input("amount-results-slider", "value"),
)
def update_graph(dropdown_selection, log, season, slider, results):

    data = filter_data(df, season, slider)
    return plot_data(data, dropdown_selection, log, results)


if __name__ == "__main__":
    # run app if script is run from main
    app.run_server(debug=True)  # TODO remove from debug mode before deploying
