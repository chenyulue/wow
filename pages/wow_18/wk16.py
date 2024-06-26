from datetime import datetime

# Plotly
import plotly.express as px

import streamlit as st

# Data manipulation
import pandas as pd
from pandas.tseries.offsets import DateOffset
import numpy as np

# Resources
import assets

@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W16,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )

colorUp, colorDown = "#4E79A7", "#D3480D"

def get_period(end_date: datetime, period_type: str, period_numbers: int):
    freqs = {"Day": "D", "Month": "ME", "Week": "W-SAT"}
    periods = pd.date_range(end=end_date, freq=freqs[period_type], periods=period_numbers)
    if period_type == "Day":
        return periods[0], periods[-1]        
    elif period_type == "Week":
        return periods[0]-DateOffset(days=6), periods[-1]
    elif period_type == "Month":
        return periods[0].replace(day=1), periods[-1]

@st.cache_data
def transform_data(end_date, period_type, period_numbers):
    start, end = get_period(end_date, period_type, period_numbers)

    data18w16 = load_data()

    filter_cond = (data18w16["Order Date"]>=start) & (data18w16["Order Date"]<=end)

    sales_last_n = data18w16.loc[filter_cond, ["Sub-Category", "Sales"]].groupby(
        by="Sub-Category").sum().sort_values(by="Sales")

    filter_previous_cond = ((data18w16["Order Date"]>=start.replace(year=start.year-1)) & 
                            (data18w16["Order Date"]<=end.replace(year=end.year-1)))

    sales_last_n_previous = data18w16.loc[filter_previous_cond, ["Sub-Category", "Sales"]].groupby(
        by="Sub-Category").sum().sort_values(by="Sales").rename(columns={"Sales": "Sales_pre"})

    sales_compare = pd.concat([sales_last_n, sales_last_n_previous], axis=1).fillna(0)

    return sales_compare.assign(
        Diff=np.abs(sales_compare["Sales"] - sales_compare["Sales_pre"]),
        Labels=np.where(
            (sales_compare["Sales"] - sales_compare["Sales_pre"])>0, f"<span style='color:{colorUp}'>▲</span>", 
            np.where(
                (sales_compare["Sales"] - sales_compare["Sales_pre"])<0, f"<span style='color:{colorDown}'>▼</span>", "")),
    ).sort_values(by="Sales")

@st.cache_data
def get_figure(end_date, period_type, period_numbers):
    sales_compare = transform_data(end_date, period_type, period_numbers)
    
    fig = px.bar(
        sales_compare.reset_index(),
        x='Sales',
        y='Sub-Category',
        custom_data=['Sales', 'Diff', 'Labels'],
        # text="Labels",
    )

    fig.update_traces(
        textposition="outside",
        texttemplate=("<span style='font-size:20px'><b>%{customdata[0]:$,.0f}</b></span><br>"
                    "<span style='font-size:16px'>%{customdata[2]}%{customdata[1]:$,.0f}</span>"),
        marker=dict(
            color=colorUp,
        )
    )

    fig.update_layout(
        width=700, height=600,
        plot_bgcolor="white",
        margin=dict(
            l=10, r=20, b=5, t=10,
        ),
        yaxis=dict(
            title_text="",
            ticksuffix="  ",
            showline=True,
            linecolor="black",
        ),
        xaxis=dict(
            title_text="",
            showticklabels=False,
            showgrid=False,
            range=[0, fig.data[0].x.max()*1.2],
        )
    )

    return fig