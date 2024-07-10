from collections import defaultdict

# Plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import sample_colorscale

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
                assets.DATA_18W18,
                index_col=0,
                parse_dates=["Order Date", "Ship Date"],
                engine="pyarrow",
            )

@st.cache_data
def transform_data():
    data18w18 = load_data()
    data18w18_filtered = data18w18.loc[:, ["Order Date", "Customer ID"]].assign(
        Order_Quarter=pd.PeriodIndex(data18w18["Order Date"], freq="Q")).sort_values(
        by="Order Date")


    quarters = data18w18_filtered["Order_Quarter"].unique()
    data = []
    first_order_customers = []
    next_quarter_orders = defaultdict(list)
    origin_order_customers = defaultdict(list)
    for i, quarter in enumerate(quarters):
        first_quarter = str(quarter).replace('Q', ' - Q')
        filter_cond = (data18w18_filtered["Order_Quarter"]==quarter) & (~data18w18_filtered["Customer ID"].isin(first_order_customers))
        origin = data18w18_filtered.loc[filter_cond, ["Customer ID"]]

        for j in range(i, len(quarters)):
            following_quarter = f"Q{j-i}"
            after = data18w18_filtered.loc[data18w18_filtered["Order_Quarter"]==quarters[j], ["Customer ID"]]
            retention = origin.merge(after, how="inner", on="Customer ID")        
            retention_ratio = retention["Customer ID"].nunique() / origin["Customer ID"].nunique()

            next_quarter_orders[j-i].extend(retention["Customer ID"].unique())
            origin_order_customers[j-i].extend(origin["Customer ID"].unique())
            
            data.append({"Y": first_quarter, "X": following_quarter, "Retention": retention_ratio})

        first_order_customers.extend(origin["Customer ID"].unique())

    data = [{"Y": "Overall<br>Retention", 
            "X": f"Q{i}", 
            "Retention": len(next_quarter_orders[i]) / len(origin_order_customers[i])}
            for i in range(0, 16)] + data

    return pd.DataFrame(data)

# Intermediate
@st.cache_data
def get_intermediate_figure():
    retention_df = transform_data()
    plot_data = retention_df.query("Y!='Overall<br>Retention' and Retention!=0")
    fig = go.Figure(go.Heatmap(
        x=plot_data["X"],
        y=plot_data["Y"],
        z=plot_data["Retention"],
        colorscale="BuGn",
        xgap=2, ygap=2,
        texttemplate="%{z:.0%}",
        hoverongaps=False,
        hoverinfo="none",
        showscale=False,
    ))

    fig.update_layout(
        width=750, height=750,
        plot_bgcolor="white",
        xaxis=dict(
            categoryorder="array",
            categoryarray=[f"Q{i}" for i in range(0, 16)],
            side="top", title_text="",
        ),
        yaxis=dict(
            autorange="reversed",
            showgrid=False,
        ),
        margin=dict(
            pad=5, b=10, r=10,
        ),
        title=dict(
            text=("<b><span style='font-size:16'>CUSTOMER RETENTION</span></b><br>"
                "<span style='font-size:14;color:#666666'>BY COHORT AND QUARTER</span>"),
            x=0.5, xref="container", xanchor="center",
            y=0.95, yref="container", yanchor="top",
        ),
    )
    
    return fig


# Jedi
@st.cache_data
def get_jedi_figure():
    retention_df = transform_data()
    fig = go.Figure(go.Heatmap(
        x=retention_df["X"],
        y=retention_df["Y"],
        z=retention_df["Retention"],
        colorscale="BuGn",
        xgap=2, ygap=2,
        texttemplate="%{z:.0%}",
        hoverongaps=False,
        hoverinfo="none",
        showscale=False,
    ))

    fig.update_layout(
        width=750, height=750,
        plot_bgcolor="white",
        xaxis=dict(
            categoryorder="array",
            categoryarray=[f"Q{i}" for i in range(0, 16)],
            side="top", title_text="",
        ),
        yaxis=dict(
            autorange="reversed",
            showgrid=False,
        ),
        margin=dict(
            pad=5, b=10, r=10,
        ),
        title=dict(
            text=("<b><span style='font-size:16'>CUSTOMER RETENTION</span></b><br>"
                "<span style='font-size:14;color:#666666'>BY COHORT AND QUARTER</span>"),
            x=0.5, xref="container", xanchor="center",
            y=0.95, yref="container", yanchor="top",
        ),
    )

    return fig