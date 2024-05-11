import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import assets

bar_fill_color = "#BAB0AC"
bar_highlight_color = "#4E79A7"

def convert_month_name(dt, start_month, long=False):
    if (dt.month - start_month < 3 and dt.month - start_month >= 0) or dt.month - start_month < -9:
        return "Q1"
    elif (dt.month - start_month < 6 and dt.month - start_month >= 0) or dt.month - start_month < -6:
        return "Q2"
    else:
        return dt.strftime("%B" if long else "%b")

@st.cache_data
def load_data():
    return pd.read_csv(
                assets.DATA_18W05,
                index_col=0,
                parse_dates=["Order Date", "Ship Date"],
                engine="pyarrow",
            )

@st.cache_data
def trans_data(years, start_month):
    if not years:
        return pd.DataFrame()
    
    data18w05 = load_data()
    filter_by_year = data18w05["Order Date"].dt.year.isin(years)
    data18w05_filtered = data18w05.loc[filter_by_year, ["Order Date", "Sales"]]

    data18w05_transformed = (
        data18w05_filtered.sort_values(by="Order Date").assign(
            Month=data18w05_filtered["Order Date"].dt.month,
            Group_name=data18w05_filtered["Order Date"].apply(
                convert_month_name, args=(start_month,)
            ),
            Month_fullname=data18w05_filtered["Order Date"].apply(
                convert_month_name, args=(start_month, True)
            ),
        )
        .groupby(by="Group_name")
        .agg({"Sales": "sum", "Month": "first", "Month_fullname": "first"})
    )
    return data18w05_transformed.replace({
            "Month": {
                data18w05_transformed.loc["Q1", "Month"]: start_month,
                data18w05_transformed.loc["Q2", "Month"]: start_month+1,
            }
        }).sort_values(by="Month")



@st.cache_data
def get_figure(years, start_month):
    if not years:
        return go.Figure()
    
    data18w05_transformed = trans_data(years, start_month)

    colors = [
        bar_fill_color if (c != "Q1" and c != "Q2") else bar_highlight_color
        for c in data18w05_transformed.index
    ]

    fig = go.Figure(
        data=go.Bar(
            x=data18w05_transformed.index,
            y=data18w05_transformed["Sales"],
            marker=dict(
                color=colors,
            ),
            customdata=data18w05_transformed,
            hovertemplate="<b>%{customdata[2]} Sales</b><br>%{y}<extra></extra>",
        )
    )

    fig.add_annotation(
        text="Week 5, 2018 | Designed by: Chenyu Lue",
        showarrow=False,
        x=1, xref="paper", xanchor="right",
        y=-0.08, yref="paper", yanchor="top",
    )
    
    fig.update_layout(
        width=500,
        height=600,
        yaxis=dict(
            tickformat=",.0f",
            tickprefix="$",
            gridcolor="#DEDEDE",
            title="Sales",
        ),
        plot_bgcolor="white",
        title=dict(
            text=(f'<b>How do <span style="color:{bar_highlight_color}">Q1</span> '
                f'and <span style="color:{bar_highlight_color}">Q2</span> '
                'compare to other months?</b>'
            ),
            y=1, yref="paper", yanchor="bottom", pad_b=20,
        )
    )
    return fig                                                                                                                       