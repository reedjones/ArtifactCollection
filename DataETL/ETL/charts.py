import enum
import random
import string
from dataclasses import dataclass, field
from typing import List

import numpy as np
import pandas as pd
from django.db.models import TextChoices
from palettable.lightbartlein import colordata

PALETTE = [
    "#465b65",
    "#184c9c",
    "#d33035",
    "#ffc107",
    "#28a745",
    "#6f7f8c",
    "#6610f2",
    "#6e9fa5",
    "#fd7e14",
    "#e83e8c",
    "#17a2b8",
    "#6f42c1",
]


def get_colors():
    """
    Get colors from palette.colors or randomly generate a list
    of colors.  This works great with the palettable module
    but this is not required and will call get_random_colors
    if palette.color is not set
    """
    try:
        palette = colordata._BLUE_TO_DARK_RED_12
        return palette.hex_colors
    except Exception:
        return get_random_colors(6)


def get_random_colors(num, colors=None):
    """
    function to generate a random hex color list
    ``num`` the number of colors required
    ``colors`` the existing color list - additional
    colors will be added if colors exist
    """
    if colors is None:
        colors = []
    while len(colors) < num:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        if color not in colors:
            colors.append(color)

    return colors


def objects_to_df(
    model,
    fields=None,
    exclude=None,
    date_cols=None,
    isqs=False,
    is_values=False,
    int_cols=None,
    **kwargs,
):
    """
    Return a pandas dataframe containing the records in a model
    ``fields`` is an optional list of field_name names. If provided, return only the
    named.
    ``exclude`` is an optional list of field_name names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    ``date_cols`` chart.js doesn't currently handle dates very well so these
    columns need to be converted to a string. Pass in the strftime string
    that would work best as the first value followed by the column names.
    ex:  ['%Y-%m', 'dat_col1', 'date_col2']
    ``kwargs`` can be include to limit the model query to specific records
    """

    if not fields:
        if not is_values:
            fields = [field.name for field in model._meta.get_fields()]
        else:
            fields = model[0].keys()

    if exclude:
        fields = [field for field in fields if field not in exclude]

    if not isqs and not is_values:
        records = model.objects.filter(**kwargs).values_list(*fields)
    elif isqs and not is_values:
        records = model.values_list(*fields)
    else:
        records = model

    df = pd.DataFrame(list(records), columns=fields)

    if date_cols:
        strftime = date_cols.pop(0)
        for date_col in date_cols:
            df[date_col] = df[date_col].apply(lambda x: x.strftime(strftime))

    if int_cols:
        for int_col in int_cols:
            try:
                df = df.astype({int_col: "int"})
            except ValueError:
                try:
                    df = df.astype({int_col: "float"})
                except ValueError:
                    pass

    return df


def get_options():
    """
    the default options that all charts will use
    """
    return {
        "plugins": {
            "datalabels": {
                "borderRadius": 4,
                "color": "white",
                "font": {"weight": "bold"},
                "padding": 6,
            }
        }
    }


def get_legend():
    return {"display": "true", "text": "hello"}


def generate_chart_id():
    """
    returns a randomly generated 8 character ascii string
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(8))


class ChartJsOptions(enum.Enum):
    scaleLabel = ("display", "")


@dataclass
class Chart:
    """
    A class for using chart.js charts.
    ``datasets`` the data itself.  this contains the data and some
    of the options for the data.  For example, in a stacked bar chart
    the stack labels.
    ``labels`` the labels for the data
    ``chart_id`` is unique chart ID.  A random id will be generated
    if none s provided.  This needs to be a valid javascript variable
    name.  Do not use '-'
    ``palette`` is a list of colors.  The will generate if none
    are listed
    """

    chart_type: str
    datasets: List = field(default_factory=list)
    labels: List = field(default_factory=list)
    chart_id: str = field(default_factory=generate_chart_id)
    palette: List = field(default_factory=get_colors)
    options: dict = field(default_factory=get_options)
    title: str = "Chart"
    legend: dict = field(default_factory=get_legend)
    xlabel: str = "xlabel"
    ylabel: str = "ylabel"
    description: str = None

    def from_lists(self, values, labels, stacks):
        """
        function to build a chart from lists
        ``values`` is a list of datasets. If the chart is not stacked
        or grouped it will be a list containing one list of the values.
        For a stack it will be each stack as a different list in the values
        list.
        ``labels`` labels are the labels for the individual values
        ``stacks`` stacks are the labels for each datset in the values
        list.  This will only contain one value if there are not stacks
        or groups of data.
        """
        self.datasets = []

        # make sure we have the right number of colors
        if len(self.palette) < len(values):
            get_random_colors(num=len(values), colors=self.palette)

        # build the datasets
        self.datasets.extend(
            {
                "label": stacks[i],  # stacks[i]
                "backgroundColor": self.palette[i],
                "data": values[i],
                "datalabels": {"align": "start", "anchor": "start"},
            }
            for i in range(len(stacks))
        )
        if len(values) == 1:
            self.datasets[0]["backgroundColor"] = self.palette

        self.labels = labels

    def from_df(
        self,
        df,
        values,
        labels,
        stacks=None,
        aggfunc=np.sum,
        round_values=0,
        fill_value=0,
    ):
        """
        function to build a chart from a dataframe
        ``df`` is the datframe to use
        ``values`` is the name of the values column
        ``stacks`` is the name of the stacks column
        ``labels`` is the name of the labels column
        ``aggfunc`` is the aggregate function to use to
         aggregate the values.  Defaults to np.sum
        ``round_values`` the decimal place to round values to
        ``fill_value`` is what to use for empty values
        """
        pivot = pd.pivot_table(
            df,
            values=values,
            index=stacks,
            columns=labels,
            aggfunc=aggfunc,
            fill_value=0,
        )

        pivot = pivot.round(round_values)

        values = pivot.values.tolist()
        labels = pivot.columns.tolist()
        stacks = pivot.index.tolist()

        self.from_lists(values, labels, stacks)

    def get_elements(self):
        """
        function to record all the chart elements by chart type
        this is the function to edit to add a new chart type
        """
        elements = {
            "data": {"labels": self.labels, "datasets": self.datasets},
            "options": self.options,
        }

        if self.chart_type in ["bar", "groupedBar"]:
            elements["type"] = "bar"
            self.options["scales"] = {
                "xAxes": [
                    {
                        "scaleLabel": {"display": "true", "labelString": self.xlabel},
                        "ticks": {"beginAtZero": "true", "autoSkip": "false"},
                    }
                ],
                "yAxes": [
                    {
                        "scaleLabel": {"display": "true", "labelString": self.ylabel},
                        "ticks": {"beginAtZero": "true", "autoSkip": "false"},
                    }
                ],
            }

        elif self.chart_type == "doughnut":
            elements["type"] = "doughnut"

        elif self.chart_type == "horizontalBar":
            elements["type"] = "horizontalBar"
            self.options["scales"] = {
                "scaleLabel": {"display": "true"},
                "xAxes": [
                    {
                        "scaleLabel": {"display": "true", "labelString": self.xlabel},
                        "ticks": {"beginAtZero": "true", "autoSkip": "false"},
                    }
                ],
                "yAxes": [
                    {
                        "scaleLabel": {"display": "true", "labelString": self.ylabel},
                        "ticks": {"beginAtZero": "true", "autoSkip": "false"},
                    }
                ],
            }

        elif self.chart_type == "polarArea":
            elements["type"] = "polarArea"

        elif self.chart_type == "radar":
            elements["type"] = "radar"

        elif self.chart_type == "stackedBar":
            elements["type"] = "bar"
            self.options["scales"] = {
                "scaleLabel": {"display": "true"},
                "xAxes": [
                    {
                        "scaleLabel": {"display": "true", "labelString": self.xlabel},
                        "stacked": "true",
                        "ticks": {"autoSkip": "false"},
                    },
                ],
                "yAxes": [
                    {
                        "scaleLabel": {"display": "true", "labelString": self.ylabel},
                        "stacked": "true",
                        "ticks": {"autoSkip": "false"},
                    }
                ],
            }

        elif self.chart_type == "stackedHorizontalBar":
            elements["type"] = "horizontalBar"
            self.options["scales"] = self.get_bar_scales()

        elements["legend"] = self.legend
        return elements

    def get_scales(self, first_scale=False):
        return {
            "xAxes": [
                {
                    "scaleLabel": {"display": "true", "labelString": self.xlabel},
                    "stacked": "true",
                    "ticks": {"autoSkip": "false"},
                }
            ],
            "yAxes": [
                {
                    "scaleLabel": {"display": "true", "labelString": self.ylabel},
                    "stacked": "true",
                    "ticks": {"autoSkip": "false"},
                }
            ],
        }

    def get_html(self):
        return f'<canvas id="{self.chart_id}"></canvas>'

    def get_js(self):
        return f"""var chartElement = document.getElementById('{self.chart_id}').getContext('2d');
var {self.chart_id}Chart = new Chart(chartElement, {self.get_elements()});"""

    def get_presentation(self, title: str):
        return {"html": self.get_html(), "js": self.get_js(), "title": title.upper()}


ChartTypes = enum.Enum(
    "ChartTypes",
    [
        "bar",
        "doughnut",
        "stackedHorizontalBar",
        "stackedBar",
        "polarArea",
        "radar",
        "groupedBar",
    ],
)
ChartChoices = TextChoices(
    "ChartChoices",
    [
        "bar",
        "doughnut",
        "stackedHorizontalBar",
        "stackedBar",
        "polarArea",
        "radar",
        "groupedBar",
    ],
)
