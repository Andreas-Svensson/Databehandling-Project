import pandas as pd

# Script for filtering DataFrame based on selected buttons in dashboard


def filter_data(data, season, slider):
    """Filters data based on button choices before plotting the final graph, this filtering is the same for all graphs"""

    data = data[data["Season"].isin([*season])]

    if slider:
        data = data[data["Year"].between(min(slider), max(slider))].sort_values(
            by="Year", ascending=False
        )

    return data


def set_default_filters(df, dropdown_selection):
    """Resets all button choices to default whenever the dropdown is used to show a new graph"""

    if dropdown_selection == "Medals USA":
        return (False, ["Summer", "Winter"], [df["Year"].min(), df["Year"].max()], 30)

    if dropdown_selection[7:] in ["Basketball", "Boxing", "Football", "Ice Hockey"]:
        return (True, ["Summer", "Winter"], [df["Year"].min(), df["Year"].max()], 30)

    if dropdown_selection == "Gender Distribution":
        return (False, ["Summer", "Winter"], [df["Year"].min(), df["Year"].max()], 30)

    print("WARNING: No dropdown selection was matched when setting default filters")
    pass
