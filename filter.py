# Script for filtering DataFrame based on selected buttons in dashboard


def filter_data(data, season, slider):
    """Filters data based on button choices before plotting the final graph, this filtering is the same for all graphs"""

    # filters results matching season selection
    data = data[data["Season"].isin([*season])]

    # filters results between min and max value of year slider and sorts by year
    data = data[data["Year"].between(min(slider), max(slider))].sort_values(
        by="Year", ascending=False
    )

    return data


def set_default_filters(df, dropdown_selection):
    """Resets all button choices to default whenever the dropdown is used to show a new graph"""

    # if-statements can be used for customized default settings if required for any graphs
    # for example, the sports graphs have log_y = True as default as opposed to the other graphs
    if dropdown_selection[7:] in ["Basketball", "Boxing", "Football", "Ice Hockey"]:
        return (True, ["Summer", "Winter"], [df["Year"].min(), df["Year"].max()], 30)

    # this default setting will be used for any other dropdown selections
    return (False, ["Summer", "Winter"], [df["Year"].min(), df["Year"].max()], 30)
