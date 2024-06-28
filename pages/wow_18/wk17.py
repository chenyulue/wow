import itertools
from datetime import datetime, timedelta

# Plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import sample_colorscale

import streamlit as st

# Data manipulation
import pandas as pd

# Resources
import assets

@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W17,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )

@st.cache_data
def transform_data():
    data18w17 = load_data()
    return data18w17.loc[:,["Category", "Order Date", "Sales"]].groupby(
        by="Category"
    ).resample(
        "MS", on="Order Date"
    ).sum(numeric_only=True).reset_index()

# chart_type = "Jump"
@st.cache_data
def get_figure(chart_type):
    data18w17_transformed = transform_data()
    
    fig = px.line(
        data18w17_transformed,
        x="Order Date",
        y="Sales",
        facet_row="Category",
        facet_row_spacing=0.05,
        range_x=[datetime(2013, 12, 1), datetime(2018, 1, 1)],
        range_y=[0, 50000],
        width=1000,
        height=800,
    )

    if chart_type == "Step":
        fig.update_traces(
            mode="lines",
            line_shape="hv",
            line_color="#72B966",
        )
    elif chart_type == "Jump":
        fig.update_traces(
            mode="markers",
            marker=dict(
                symbol="line-ew",
                line_color="#4E79A7",
            ),
        )
    else:
        fig.update_traces(
            mode="lines",
            line_shape="linear",
            line_color="#B4B4B4",
        )

    fig.update_traces(
        marker_line_width=3,
        hoverlabel_bgcolor="white",
    )

    for i in range(0, 3):
        cat = fig.data[i].hovertemplate.split("<br>")[0].split("=")[-1]
        fig.data[i].update(
            hovertemplate = f"<b>{cat}</b> | <b>%{{x|%B, %Y}}</b><br><b>%{{y:%,.0f}}</b> in sales",
        )

        ann = fig.layout.annotations[i].text.split("=")[-1].split()
        fig.layout.annotations[i].update(
            text="<br>".join(ann),
            x=0, xref=f"x{i+1 if i>0 else ''} domain", xanchor="left",
            y=0.5, yref=f"y{i+1 if i>0 else ''} domain", yanchor="middle",
            textangle=0, align="left",
            xshift=-160,
            font=dict(
                size=16,
                color="#666666",
            )
        )
        
        fig.update_layout(**{
            f"xaxis{i+1 if i>0 else ''}": dict(
                showgrid=False,
                title_text="",
                tickprefix="<br>",
            ),
            f"yaxis{i+1 if i>0 else ''}": dict(
                showgrid=False,
                zeroline=False,
                tickformat="$,.0f",
                tickfont=dict(
                    color="#666666",
                ),
                title_standoff=5,
            )
        })

    for i in range(0, 3):
        fig.add_shape(
            type="line",
            y0=-0.05, y1=-0.05, yref=f"y{i+1 if i>0 else ''} domain",
            x0=-0.32, x1=1, xref=f"x{i+1 if i>0 else ''} domain",
            line=dict(
                color="#666666",
                width=1,
            ),
        )
        if i == 2:
            fig.add_shape(
                type="line",
                y0=1.05, y1=1.05, yref=f"y{i+1 if i>0 else ''} domain",
                x0=-0.32, x1=1, xref=f"x{i+1 if i>0 else ''} domain",
                line=dict(
                    color="#666666",
                    width=1,
                ),
            )

    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(
            l=200, r=5,
        ),
    )

    return fig