from dash import html, dcc
import dash_bootstrap_components as dbc


class Layout:
    def __init__(self, df) -> None:
        # takes in df to get min and max values of year, used in range slider at the bottom of dashboard
        self._min = df["Year"].min()
        self._max = df["Year"].max()

    def layout(self):
        """returns the layout of the application"""
        return dbc.Container(
            [
                # first row, banner of the dashboard, card with banner image and title
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.Img(src="assets/usa-flag.png"),
                                html.H1("Olympic Games - USA"),
                            ],
                        ),
                    ],
                    id="banner",
                ),
                # second row, contains 3 columns with input options
                dbc.Row(
                    className="col-3-wide",
                    children=[
                        # first column, contains dropdown to select which graph to display
                        dbc.Col(
                            id="column-one",
                            children=[
                                dcc.Dropdown(
                                    id="dropdown",
                                    className="dropdown",
                                    options=[
                                        "Medals USA",
                                        "Medals Basketball",
                                        "Medals Boxing",
                                        "Medals Football",
                                        "Medals Ice Hockey",
                                        "Gender Distribution",
                                    ],
                                    value="Medals USA",  # default value of dropdown
                                )
                            ],
                        ),
                        # second column, contains 2 button groups to select log_y and summer/winter results
                        dbc.Col(
                            id="column-two",
                            className="radio-group",
                            children=[
                                # using a div here in order to style all contents with the buttons ID
                                html.Div(
                                    id="buttons",
                                    children=[
                                        # first button group of column 2, using RadioItems to select log_y True/False
                                        # (restyled to look like buttons using CSS)
                                        dbc.RadioItems(
                                            id="log-buttons",
                                            className="btn-group",
                                            # these class names taken from https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button_group/
                                            inputClassName="btn-check",
                                            labelClassName="btn btn-outline-primary",
                                            labelCheckedClassName="active",
                                            options=[
                                                {
                                                    "label": "Normal",
                                                    "value": False,
                                                },
                                                {
                                                    "label": "Log",
                                                    "value": True,
                                                },
                                            ],
                                            value=False,
                                        ),
                                        # second button group of column 2, using Checklist to select summer and/or winter
                                        dbc.Checklist(
                                            id="season-picker",
                                            options=[
                                                dict(
                                                    label="Summer",
                                                    value="Summer",
                                                ),
                                                dict(
                                                    label="Winter",
                                                    value="Winter",
                                                ),
                                            ],
                                            value=["Summer", "Winter"],
                                            inline=True,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        # third column, containing results slider
                        dbc.Col(
                            id="column-three",
                            children=[
                                html.P("Results:"),
                                dcc.Slider(
                                    id="amount-results-slider",
                                    min=10,
                                    max=50,
                                    step=10,
                                    value=10,
                                ),
                            ],
                        ),
                    ],
                ),
                # third row, displaying the graph
                dbc.Row(dcc.Graph(id="graph-id")),
                # fourth row, containing year slider, using RangeSlider to be able to select a range of year values
                dbc.Row(
                    id="year-slider-row",
                    children=[
                        html.P("Year span:"),
                        dcc.RangeSlider(
                            id="year-slider",
                            min=self._min,  # uses min and max values of df to know what value the slider should start and end at
                            max=self._max,
                            step=2,
                            # styling the selected options to show as a square below the slider that always shows
                            tooltip=dict(placement="bottom", always_visible=True),
                            marks=None,  # hiding marks because above styling allows us to see which year we have selected
                        ),
                    ],
                ),
            ]
        )
