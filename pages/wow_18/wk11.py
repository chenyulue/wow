import streamlit as st

# Plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Data manipulation
import pandas as pd
import numpy as np

# Resources
import assets


@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W11,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )


@st.cache_data
def transform_data():
    data18w11 = load_data()
    sales_office_supplies = (
        data18w11.query("Category=='Office Supplies'")[["Sub-Category", "Sales"]]
        .groupby(by="Sub-Category")
        .sum()
    )
    percent_sales_office_supplies = sales_office_supplies / sales_office_supplies.sum()
    return (
        np.round(percent_sales_office_supplies, 2)
        .replace({"Sales": {0.00: 0.01}})
        .sort_values(by="Sales", ascending=False)
    )


@st.cache_data
def get_figure():
    X, Y = np.meshgrid(np.arange(0, 20), np.arange(0, 5))
    percent_round = transform_data()

    fig = make_subplots(
        rows=3,
        cols=3,
        subplot_titles=[
            f'{cat} ({percent_round.loc[cat, "Sales"]:.0%})'
            for cat in percent_round.index
        ],
        vertical_spacing=0.15,
        horizontal_spacing=0.05,
    )

    for i in range(0, 3):
        for j in range(0, 3):
            name = percent_round.index[i * 3 + j]
            highlight_num = int(percent_round.loc[name, "Sales"] * 100)
            colors = ["#5A7993"] * highlight_num + ["#E6E6E6"] * (100 - highlight_num)
            fig.add_trace(
                go.Scatter(
                    name="%{meta[0]}",
                    meta=[name],
                    mode="text",
                    x=X.ravel(),
                    y=Y.ravel(),
                    text=["•"] * 100,
                    textfont=dict(
                        size=35,
                        color=colors,
                    ),
                    hoverinfo="none",
                    showlegend=False,
                ),
                row=i + 1,
                col=j + 1,
            )

            fig.update_layout(
                **{
                    f"yaxis{i*3+j+1}": dict(
                        showticklabels=False,
                        showgrid=False,
                    ),
                    f"xaxis{i*3+j+1}": dict(
                        showticklabels=False,
                        autorange="reversed",
                        showgrid=False,
                    ),
                }
            )

    fig.update_layout(
        width=800,
        height=800,
        plot_bgcolor="white",
        title=dict(
            text="Small Multiple Grids",
            x=0.5,
            xref="paper",
            xanchor="center",
            y=1,
            yref="paper",
            yanchor="bottom",
            pad_b=60,
            font_size=32,
        ),
    )

    return fig
