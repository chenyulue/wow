import itertools
from datetime import datetime, timedelta

# Plotly
import plotly.express as px
import plotly.graph_objects as go

# Altair
import altair as alt

# Data manipulation
import pandas as pd
import numpy as np

# Streamlit
import streamlit as st

# Resources
import assets


@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W10,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )


@st.cache_data
def transform_data():
    data18w10 = load_data()
    data18w10_filtered = data18w10.loc[
        data18w10["Order Date"].dt.year == 2017, ["Order Date", "Segment", "Sales"]
    ].sort_values(by="Order Date")
    data18w10_transformed = (
        data18w10_filtered.assign(
            Week=data18w10_filtered["Order Date"]
            .dt.to_period("W")
            .apply(lambda x: x.week)
        )
        .loc[data18w10_filtered["Order Date"] != datetime(2017, 1, 1)]
        .groupby(by=["Week", "Segment"])
        .sum(numeric_only=True)
    )
    data18w10_calculated = pd.concat(
        [
            data18w10_transformed,
            data18w10_transformed.groupby(level=0, group_keys=False)
            .apply(lambda x: x / x.sum())
            .rename(columns={"Sales": "Sales_percent"}),
        ],
        axis=1,
    ).assign(
        angle=[
            2 * np.pi * (i - 1) / 52
            for i in data18w10_transformed.index.get_level_values(0)
        ]
    )

    def calc_r(df, week, inner_radii=1, segment_gap=0.15):
        df.loc[(week, "Corporate"), "r1"] = inner_radii
        df.loc[(week, "Corporate"), "r2"] = (
            df.loc[(week, "Corporate"), "r1"]
            + df.loc[(week, "Corporate"), "Sales_percent"]
        )
        df.loc[(week, "Consumer"), "r1"] = (
            df.loc[(week, "Corporate"), "r2"] + segment_gap
        )
        df.loc[(week, "Consumer"), "r2"] = (
            df.loc[(week, "Consumer"), "r1"]
            + df.loc[(week, "Consumer"), "Sales_percent"]
        )
        df.loc[(week, "Home Office"), "r1"] = (
            df.loc[(week, "Consumer"), "r2"] + segment_gap
        )
        df.loc[(week, "Home Office"), "r2"] = (
            df.loc[(week, "Home Office"), "r1"]
            + df.loc[(week, "Home Office"), "Sales_percent"]
        )

    for i in data18w10_calculated.index.get_level_values(0).unique():
        calc_r(data18w10_calculated, i)

    return data18w10_calculated.reset_index()


@st.cache_data
def get_figure():
    data18w10_calculated = transform_data()
    width, height = 500, 550
    title = alt.Title(
        "KEEP AN EYE ON SALES",
        subtitle="Weekly Sales by Segment for 2017",
        fontSize=20,
        color="black",
        subtitleFontSize=16,
        subtitleColor="#666666",
    )

    base = alt.Chart(data18w10_calculated, title=title).transform_calculate(
        x1="sin(datum.angle) * datum.r1",
        x2="sin(datum.angle) * datum.r2",
        y1="cos(datum.angle) * datum.r1",
        y2="cos(datum.angle) * datum.r2",
    )

    chart = base.mark_rule(strokeWidth=6, strokeCap="round").encode(
        x=alt.X("x1:Q").axis(None),
        x2="x2:Q",
        y=alt.Y("y1:Q").axis(None),
        y2="y2:Q",
        color=alt.Color("Segment:N")
        .scale(
            domain=["Corporate", "Consumer", "Home Office"],
            range=["#E84D5B", "#6FB899", "#26979F"],
        )
        .sort(["Corporate", "Consumer", "Home Office"])
        .legend(
            title=None,
            legendX=210,
            legendY=220,
            orient="none",
            labelFontSize=13,
            labelColor="black",
            symbolStrokeWidth=6,
        ),
        tooltip=[
            alt.Tooltip("Sales:Q", format="$,.0f"),
            alt.Tooltip("Segment:N"),
            alt.Tooltip("Week:O"),
        ],
    )

    return chart.properties(
        width=width,
        height=height,
    ).configure(background="#EAE2CF", view=alt.ViewConfig(strokeWidth=0))
