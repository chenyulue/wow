# Plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale
import streamlit as st

# Data manipulation
import pandas as pd
import numpy as np

# Resources
import assets


@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W13,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )


@st.cache_data
def transform_data(year, measure):
    data18w13 = load_data()
    data18w13_transformed = (
        data18w13.loc[:, ["Sub-Category", "Sales"]]
        .groupby(by=["Sub-Category", data18w13["Order Date"].dt.year])
        .sum()
        .unstack()
        .swaplevel(axis=1)
    )

    for y in [2014, 2015, 2016, 2017]:
        data18w13_transformed.loc[:, (y, "% of Total")] = (
            data18w13_transformed.loc[:, (y, "Sales")]
            / data18w13_transformed.loc[:, (y, "Sales")].sum()
        )
        if y != 2014:
            data18w13_transformed.loc[:, (y, "% Diff")] = (
                data18w13_transformed.loc[:, (y, "Sales")]
                - data18w13_transformed.loc[:, (y - 1, "Sales")]
            ) / data18w13_transformed.loc[:, (y - 1, "Sales")]
        else:
            data18w13_transformed.loc[:, (y, "% Diff")] = np.nan

    return data18w13_transformed.sort_index(
        axis=1,
        key=lambda idx: [
            {"Sales": 0, "% of Total": 1, "% Difference": 2}.get(x, x) for x in idx
        ],
    ).sort_values(by=[(year, measure)], ascending=False)


def get_colors(value, minvalue, maxvalue, cm="RdBu"):
    colors = sample_colorscale(cm, 201)
    n = int((value - minvalue) / (maxvalue - minvalue) * 200)
    return colors[n]


@st.cache_data
def get_figure(year, measure):
    data18w13_transformed = transform_data(year, measure)
    maxSales = data18w13_transformed.max().max()
    minSales = data18w13_transformed.min().min()
    saleColors = np.array(
        [
            ["#EBF0F8"] * len(data18w13_transformed),
            [
                get_colors(v, minSales, maxSales)
                for v in data18w13_transformed.loc[:, (2014, "Sales")]
            ],
            ["#EBF0F8"] * len(data18w13_transformed),
            ["#EBF0F8"] * len(data18w13_transformed),
            [
                get_colors(v, minSales, maxSales)
                for v in data18w13_transformed.loc[:, (2015, "Sales")]
            ],
            ["#EBF0F8"] * len(data18w13_transformed),
            ["#EBF0F8"] * len(data18w13_transformed),
            [
                get_colors(v, minSales, maxSales)
                for v in data18w13_transformed.loc[:, (2016, "Sales")]
            ],
            ["#EBF0F8"] * len(data18w13_transformed),
            ["#EBF0F8"] * len(data18w13_transformed),
            [
                get_colors(v, minSales, maxSales)
                for v in data18w13_transformed.loc[:, (2017, "Sales")]
            ],
            ["#EBF0F8"] * len(data18w13_transformed),
            ["#EBF0F8"] * len(data18w13_transformed),
        ]
    )
    fig = go.Figure()

    fig.add_trace(
        go.Table(
            columnwidth=[7] + [6, 7, 6] * 4,
            header=dict(
                values=[("", "Sub-Category")] + list(data18w13_transformed.columns),
                align="center",
                font_size=10,
            ),
            cells=dict(
                values=[data18w13_transformed.index]
                + [
                    data18w13_transformed.loc[:, col]
                    for col in data18w13_transformed.columns
                ],
                align=["left", "right"],
                format=[""] + ["$,.0f", ".2%", ".2%"] * 4,
                height=30,
                fill_color=saleColors,
                font_color=(
                    ["black"]
                    + [
                        [
                            "white" if (v > 90000 or v < 22000) else "black"
                            for v in data18w13_transformed.loc[:, (2014, "Sales")]
                        ],
                        "black",
                        "black",
                    ]
                    + [
                        [
                            "white" if (v > 90000 or v < 22000) else "black"
                            for v in data18w13_transformed.loc[:, (2015, "Sales")]
                        ],
                        "black",
                        "black",
                    ]
                    + [
                        [
                            "white" if (v > 90000 or v < 22000) else "black"
                            for v in data18w13_transformed.loc[:, (2016, "Sales")]
                        ],
                        "black",
                        "black",
                    ]
                    + [
                        [
                            "white" if (v > 90000 or v < 22000) else "black"
                            for v in data18w13_transformed.loc[:, (2017, "Sales")]
                        ],
                        "black",
                        "black",
                    ]
                ),
            ),
        )
    )

    fig.update_layout(
        width=1000,
        height=600,
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=20,
        ),
    )

    return fig
