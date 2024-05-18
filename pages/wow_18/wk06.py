import itertools
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import assets


@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W06,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )


@st.cache_data
def transform_data(*segment):
    if not segment:
        return pd.DataFrame()
    
    data18w06 = load_data()
    data18w06_filtered = data18w06.loc[
        data18w06.Segment.isin(segment), ["Category", "Sub-Category", "Region", "Sales"]
    ]
    data18w06_transformed = data18w06_filtered.groupby(
        by=["Category", "Sub-Category", "Region"]
    ).sum()

    level0 = data18w06_transformed.index.get_level_values(0)
    level1 = data18w06_transformed.index.get_level_values(1)
    level0_sum = [data18w06_transformed.loc[idx].sum().iloc[0] for idx in level0]
    level1_sum = [
        data18w06_transformed.loc[idx].sum().iloc[0] for idx in zip(level0, level1)
    ]

    return (
        data18w06_transformed.assign(
            level0_sum=level0_sum,
            level1_sum=level1_sum,
        )
        .sort_values(by=["level0_sum", "level1_sum", "Sales"])
        .reset_index()
    )

@st.cache_data
def plot_figure(*segment):
    if not segment:
        return go.Figure()
    
    data18w06_transformed = transform_data(*segment)
    
    colors = {
        "South": "#F43C63",
        "Central": "#1BA3A6",
        "East": "#BCBD22",
        "West": "#4E79A7",
    }
    gridColor = "#CBCBCB"

    fig = go.Figure()

    # Line coordinates
    coords = []
    for _, group in itertools.groupby(
        zip(
            data18w06_transformed.Sales,
            data18w06_transformed.Category,
            data18w06_transformed["Sub-Category"],
        ),
        key=lambda x: x[1:],
    ):
        coords.extend(group),
        coords.append((None, None, None))
    x, y1, y2 = list(zip(*coords))

    fig.add_trace(go.Scatter(
        mode="lines",
        x=x,
        y=[y1, y2],
        line=dict(
            color="black",
            width=1,
        ),
        showlegend=False,
        hoverinfo="none",
    ))

    for region, color in colors.items():
        data = data18w06_transformed.loc[data18w06_transformed["Region"]==region]
        fig.add_trace(go.Scatter(
            mode="markers",
            name=region,
            x=data.Sales,
            y=[data.Category, data["Sub-Category"]],
            marker=dict(
                color=color,
                size=13,
                line_color="black",
                line_width=1,
            ),
            meta=[region],
            hovertemplate="Region: %{meta[0]}<br>Sales: $%{x:.3s}<extra></extra>",
            hoverlabel=dict(
                bgcolor="white",
            )
        ))

    fig.add_annotation(
        text="<b>Category  Sub-Category</b>",
        x=-0.01, xref="paper", xanchor="right",
        y=1, yref="paper", yanchor="middle",
        showarrow=False,
    )

    fig.update_layout(
        yaxis=dict(
            gridcolor=gridColor,
            linecolor=gridColor,
            mirror=True,
            gridwidth=1,
            ticksuffix="  ",
        ),
        xaxis=dict(
            gridcolor=gridColor,
            zeroline=False,
            linecolor=gridColor,
            mirror=True,
            gridwidth=1,
            nticks=6,
            tickprefix="$",
            title=dict(
                text="Sales",
            )
        ),
        legend=dict(
            x=0, xref="paper", xanchor="left",
            y=1.025, yref="paper", yanchor="bottom",
            orientation="h",
        ),
        plot_bgcolor="white",
        width=600, height=800,
    )
    return fig
