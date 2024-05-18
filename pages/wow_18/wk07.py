import itertools
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import assets


@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W07,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )


@st.cache_data
def transform_data(years, category):
    if (not years) or (not category):
        return pd.DataFrame()

    data18w07 = load_data()
    filter_cond = data18w07["Order Date"].dt.year.isin(years) & data18w07[
        "Category"
    ].isin(category)

    data18w07_filtered = data18w07.loc[
        filter_cond, ["Order Date", "Sub-Category", "Sales"]
    ]
    data18w07_transformed = (
        data18w07_filtered.iloc[:, [1, 2]]
        .groupby(by=["Sub-Category", data18w07_filtered["Order Date"].dt.month])
        .sum()
        .unstack(level=1)
    )
    data18w07_transformed.columns = data18w07_transformed.columns.droplevel(0)

    return data18w07_transformed.assign(
        **{
            "Grand Total": data18w07_transformed.sum(axis=1),
        }
    ).sort_values(by="Grand Total", ascending=False)


@st.cache_data
def get_figure(years, category):
    if (not years) or (not category):
        return go.Figure()

    data18w07_transformed = transform_data(years, category)

    fig = go.Figure(
        go.Table(
            header=dict(
                values=[""]
                + [
                    datetime(year=1900, month=m, day=1).strftime("%B")
                    if isinstance(m, int)
                    else m
                    for m in data18w07_transformed.columns
                ],
            ),
            cells=dict(
                values=[data18w07_transformed.index]
                + [data18w07_transformed[col].fillna(0) for col in data18w07_transformed.columns],
                align=["left", "right"],
            ),
        )
    )

    minColor = "#A90C38"
    maxColor = "#2E5A87"

    def create_column_colors(col):
        maxValue = data18w07_transformed[col].max()
        minValue = data18w07_transformed[col].min()
        fillColors = [
            maxColor if v == maxValue else (minColor if v == minValue else "#EBF0F8")
            for v in data18w07_transformed[col]
        ]
        textColors = [
            "white" if (v == maxValue or v == minValue) else "black"
            for v in data18w07_transformed[col]
        ]
        return fillColors, textColors

    fillColor, textColor = list(
        zip(*[create_column_colors(col) for col in data18w07_transformed.columns])
    )

    fig.update_traces(
        cells=dict(
            format=["", ",.0f"],
            prefix=["", "$"],
            fill_color=[["#EBF0F8"] * len(data18w07_transformed)] + list(fillColor),
            font_color=[["black"] * len(data18w07_transformed)] + list(textColor),
        ),
        header=dict(
            font_weight="bold",
        ),
    )

    fig.update_layout(
        width=1200,
        height=425,
        margin=dict(
            b=10,
            t=20,
            l=10,
            r=10,
        ),
    )
    return fig
