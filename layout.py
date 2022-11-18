from dash import html, dcc
import dash_bootstrap_components as dbc


class Layout:
    def __init__(self, df) -> None:
        self._df = df
        self._min = df["Year"].min()
        self._max = df["Year"].max()

    def layout(self):
        """returns the layout of the application"""
        return dbc.Container(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Img(src="assets/usa-flag.png"),
                            html.H1("OS Dashboard - USA"),
                        ],
                    ),
                    id="banner",
                ),
                dbc.Row(
                    className="col-3-wide",
                    children=[
                        dbc.Col(
                            dcc.Dropdown(
                                id="dropdown",
                                className="dropdown",
                                options=[
                                    "Medals in USA",
                                    "Medals per sport",
                                ],  # set this to variable value
                                value="Medals in USA",  # default value of dropdown
                            ),
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.RadioItems(
                                                id="log-buttons",
                                                children=[
                                                    html.Img(src="assets/usa-flag.png")
                                                ],
                                                className="btn-group",  # groups radio items side-by-side
                                                inputClassName="btn-check",  # hides radio buttons checkbox
                                                labelClassName="btn btn-outline-secondary",  # adds an outline to the button, colors it and the text
                                                # labelCheckedClassName="active",
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
                                        ],
                                    ),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id="season-picker",
                                            options=[
                                                dict(label="Summer", value="Summer"),
                                                dict(label="Winter", value="Winter"),
                                            ],
                                            value=["Summer", "Winter"],
                                            inline=True,
                                        )
                                    ),
                                ]
                            ),
                        ),
                    ],
                ),
                dbc.Row(dcc.Graph(id="graph-id")),
                dbc.Row(
                    dcc.RangeSlider(
                        id="year-slider",
                        min=self._min,
                        max=self._max,
                        step=2,
                        tooltip=dict(placement="bottom", always_visible=True),
                        marks=None,
                    )
                ),
                # storing intermediate value on clients browser in order to share between several callbacks
                dcc.Store(id="df-athlete"),
            ]
        )
