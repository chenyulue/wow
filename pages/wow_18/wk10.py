from datetime import datetime

# Plotly
import plotly.graph_objects as go

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

    return data18w10_calculated


@st.cache_data
def get_figure():
    data18w10_calculated = transform_data()
    width, height = 600, 600
    cm = dict(
        zip(["Corporate", "Consumer", "Home Office"], ["#E84D5B", "#6FB899", "#26979F"])
    )
    BGCOLOR = "#EAE2CF"

    fig = go.Figure()

    for week in data18w10_calculated.index.get_level_values(0).unique():
        for segment in ["Corporate", "Consumer", "Home Office"]:
            r = np.array(data18w10_calculated.loc[(week, segment), ["r1", "r2"]])
            angle = data18w10_calculated.loc[(week, segment), "angle"]
            fig.add_trace(
                go.Scatter(
                    name=segment,
                    mode="lines",
                    meta=[
                        data18w10_calculated.loc[(week, segment), "Sales"],
                        segment,
                        week,
                    ],
                    x=r * np.sin(angle),
                    y=r * np.cos(angle),
                    line=dict(
                        color=cm[segment],
                        width=6,
                    ),
                    showlegend=week == 1,
                    hovertemplate="Salse: %{meta[0]:$,.0f}<br>%{meta[1]}<br>Week %{meta[2]}<extra></extra>",
                )
            )

    fig.add_annotation(
        text="#WOW 2018, Week 10",
        x=0,
        xref="paper",
        xanchor="left",
        y=0,
        yref="paper",
        yanchor="top",
        showarrow=False,
        yshift=-10,
    )
    fig.add_annotation(
        text="By Chenyu Lue",
        x=1,
        xref="paper",
        xanchor="right",
        y=0,
        yref="paper",
        yanchor="top",
        showarrow=False,
        yshift=-10,
    )

    title = dict(
        text=(
            "<span style='font-weight: bold; font-size:24'>KEEP AN EYE ON SALES</span><br>"
            "<span style='font-color:#666666'>Weekly Sales by Segment for 2017</span>"
        ),
        x=0.5,
        xref="paper",
        xanchor="center",
        y=1,
        yref="paper",
        yanchor="bottom",
        pad_b=30,
    )

    fig.update_layout(
        width=width,
        height=height,
        plot_bgcolor=BGCOLOR,
        paper_bgcolor=BGCOLOR,
        title=title,
        legend=dict(
            x=0.5,
            xref="paper",
            xanchor="center",
            y=0.5,
            yref="paper",
            yanchor="middle",
            bgcolor="rgba(255,255,255,0)",
        ),
        xaxis=dict(
            range=(-2.4, 2.4),
            showgrid=False,
            showticklabels=False,
            ticks="",
            zeroline=False,
        ),
        yaxis=dict(
            range=(-2.4, 2.4),
            showgrid=False,
            showticklabels=False,
            ticks="",
            zeroline=False,
        ),
        margin=dict(t=50, l=50, r=50, b=50),
    )
    return fig
