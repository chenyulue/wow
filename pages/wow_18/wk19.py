import plotly.express as px
import plotly.graph_objects as go

import streamlit as st

# Data manipulation
import pandas as pd

# Resources
import assets

@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W19,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )

@st.cache_data
def get_customer_sales_figure():
    data18w19 = load_data()
    customer_sales = data18w19.loc[:, ["Customer Name", "Sales"]].groupby(
        by="Customer Name").sum().sort_values(by="Sales").reset_index()

    fig = px.bar(
        customer_sales,
        x="Sales", y="Customer Name",
    )
    fig.update_traces(
        marker_color="#349A52",
        hovertemplate="Customer Name: <b>%{y}</b><br>Sales: <b>%{x:$,.0f}</b>",
        hoverlabel=dict(
            bgcolor="white",
        ),
    )

    fig.update_layout(
        width=500, height=16000,
        plot_bgcolor="white",
        margin=dict(
            l=0, r=0, t=20, b=10,
        ),
        yaxis=dict(
            title_text="",
        )
    )
    return fig

@st.cache_data
def get_subcategory_sales_figure():
    data18w19 = load_data()
    subcategory_sales = data18w19.loc[:, ["Sub-Category", "Sales"]].groupby(
        by="Sub-Category").sum().sort_values(by="Sales").reset_index()

    fig = px.bar(
        subcategory_sales,
        x="Sales", y="Sub-Category",
    )
    fig.update_traces(
        marker_color="#349A52",
        hovertemplate="Sub-Category: <b>%{y}</b><br>Sales: <b>%{x:$,.0f}</b>",
        hoverlabel=dict(
            bgcolor="white",
        )
    )

    fig.update_layout(
        width=300, height=400, #16000,
        plot_bgcolor="white",
        margin=dict(
            l=0, r=0, b=10, t=20
        ),
        yaxis=dict(
            title_text="",
        )
    )
    return fig

@st.cache_data
def get_state_sales_figure():
    data18w19 = load_data()
    usa_code = pd.read_csv(assets.DATA_MAP).loc[:, ["Code", "State"]]
    state_sales = data18w19.loc[:, ["State", "Sales"]].groupby(
        by="State").sum().sort_values(by="Sales").reset_index().merge(
            usa_code, on="State", how="left"
        )

    fig = go.Figure(data=go.Choropleth(
        locations=state_sales["Code"],
        z=state_sales["Sales"],
        locationmode="USA-states",
        colorscale="YlGn",
        customdata=state_sales[["State"]],
        hovertemplate="Country: <b>United States</b><br>State: <b>%{customdata[0]}</b><br>Sales: <b>%{z:$,.0f}</b>"
    ))
    fig.update_traces(
        showscale=False,
    )

    fig.update_layout(
        width=600, height=360,
        geo_scope="usa",
        margin=dict(
            l=10, r=10, b=10, t=20,
        )
    )
    return fig
