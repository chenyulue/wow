import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import assets

data18w02 = pd.read_csv(assets.DATA_18W02, index_col=0, parse_dates=[
                        "Order Date", "Ship Date"], engine="pyarrow")

def get_fiscal_year(start: int, date: datetime) -> int:
    if date.month >= start:
        return date.year
    return date.year - 1

def strptime(df: pd.DataFrame, start: int):
    cond = df["Fiscal_year"] < df["Order Date"].dt.year
    year = 1941 if start <= 2 else 1940
    return np.where(cond, df["Month_day"] + f", {year}", df["Month_day"] + f", {year-1}")

data18w02_filtered = data18w02.loc[:, ["Order Date", "Sales"]].groupby(
    by="Order Date").sum().reset_index()
data18w02_filtered = data18w02_filtered.assign(
    Month_day=data18w02_filtered["Order Date"].dt.strftime("%B %d"),
)

@st.cache_data
def get_fiscal_data(start_month: int) -> pd.DataFrame:
    return data18w02_filtered.assign(
        Fiscal_year=data18w02_filtered["Order Date"].apply(
            lambda d: get_fiscal_year(start_month, d)),
    )

@st.cache_data
def plot_fiscal_data(start_month: int):
    data18w02_fiscal = get_fiscal_data(start_month)
    
    fiscal_years = data18w02_fiscal["Fiscal_year"].value_counts().index
    data = []
    xrange = []
    for year in fiscal_years:
        filter_cond = data18w02_fiscal["Fiscal_year"] == year
        data18w02_year = data18w02_fiscal.loc[filter_cond, :]
        data18w02_year = data18w02_year.assign(
            Running_sales=data18w02_year["Sales"].cumsum(),
            x_datestr=strptime(data18w02_year, start_month),
        )
        data18w02_year = data18w02_year.assign(
                x_datetime=data18w02_year["x_datestr"].apply(lambda d: datetime.strptime(d, "%B %d, %Y"))
            )
        
        data.append(go.Scatter(
            name=str(year),
            x=data18w02_year.loc[:, "x_datetime"],
            y=data18w02_year["Running_sales"],
            customdata=data18w02_year,
            hovertemplate=("Fiscal Year: %{customdata[3]}<br>"
                        "%{customdata[0]|%Y/%m/%d}<br>"
                        "Running Sum of Sales: %{customdata[4]:$,.0f}<extra></extra>"
            ),
            showlegend=False,
        ))
        xrange.append(data18w02_year["x_datetime"])

    fig = go.Figure(data=data)

    for trace in fig.data:
        fig.add_annotation(
            text=trace["name"],
            x=trace["x"][-1], y=trace["y"][-1],
            xanchor="left", yanchor="middle",
            showarrow=False,
        )

    # Make the xaxis range a little wider than the default
    x_limit = max(xrange, key=lambda x: len(x))
    x0 = x_limit.iloc[0] - timedelta(days=15)
    x1 = x_limit.iloc[-1] + timedelta(days=15)

    fig.update_layout(
        xaxis=dict(
            tickformat="%b %d",
            nticks=16,
            tickmode="auto",
            range=[x0, x1],
        ),
        yaxis=dict(
            tickformat="$,.0f"
        ),
        width=800, height=600,
        template="simple_white",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="gray",
            font_color="black",
        )
    )
    return fig