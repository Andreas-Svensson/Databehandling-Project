from dash import html, dcc
import dash_bootstrap_components as dbc


class Layout:
    def __init__(self, df) -> None:
        self._min = df["Year"].min()
        self._max = df["Year"].max()

    def layout(self):
        """returns the layout of the application"""
        return dbc.Container(
            [
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
                dbc.Row(
                    className="col-3-wide",
                    children=[
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
                                    ],  # set this to variable value
                                    value="Medals USA",  # default value of dropdown
                                )
                            ],
                        ),
                        dbc.Col(
                            id="column-two",
                            className="radio-group",
                            children=[
                                html.Div(
                                    id="buttons",
                                    children=[
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
                dbc.Row(dcc.Graph(id="graph-id")),
                dbc.Row(
                    id="year-slider-row",
                    children=[
                        html.P("Year span:"),
                        dcc.RangeSlider(
                            id="year-slider",
                            min=self._min,
                            max=self._max,
                            step=2,
                            tooltip=dict(placement="bottom", always_visible=True),
                            marks=None,
                        ),
                    ],
                ),
            ]
        )
