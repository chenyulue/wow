# Plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
# Data manipulation
import pandas as pd
from pandas.tseries.offsets import DateOffset
# Resources
import assets

@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W12,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )

@st.cache_data
def get_last_two_periods(current_max_date):
    data18w12 = load_data()
    most_recent = (data18w12["Order Date"]<=current_max_date) & (data18w12["Order Date"]>=current_max_date.replace(day=1))
    prior_month = current_max_date - DateOffset(months=1)
    prior = (data18w12["Order Date"]<=prior_month) & (data18w12["Order Date"]>=prior_month.replace(day=1))
    return most_recent, prior

@st.cache_data
def get_last_two_periods_format(current_max_date):
    data18w12 = load_data()
    most_recent, prior = get_last_two_periods(current_max_date)
    if most_recent.sum() == 0:
        most_recent_format = ""
    else:
        start, end = data18w12.loc[most_recent, "Order Date"].min(), data18w12.loc[most_recent, "Order Date"].max()
        most_recent_format = start.strftime("%Y/%m/%d")+" - "+end.strftime("%Y/%m/%d")
    if prior.sum() == 0:
        prior_format = ""
    else:
        start_prior, end_prior = data18w12.loc[prior, "Order Date"].min(), data18w12.loc[prior, "Order Date"].max()
        prior_format = start_prior.strftime("%Y/%m/%d")+" - "+end_prior.strftime("%Y/%m/%d")
    return most_recent_format, prior_format 

@st.cache_data
def transform_data(current_max_date):
    data18w12 = load_data()
    most_recent, prior = get_last_two_periods(current_max_date)

    data18w12_most_recent = data18w12.loc[most_recent, ["Sub-Category", "Sales"]]
    data18w12_prior = data18w12.loc[prior, ["Sub-Category", "Sales"]]

    data18w12_transformed = pd.concat([
        data18w12_most_recent.groupby(by="Sub-Category").sum().rename(columns={"Sales": "Most Recent Month"}),
        data18w12_prior.groupby(by="Sub-Category").sum().rename(columns={"Sales": "Prior Month"}),
    ], axis=1)

    return data18w12_transformed.assign(
        Change=(data18w12_transformed['Most Recent Month'] - data18w12_transformed["Prior Month"]) / data18w12_transformed["Prior Month"]
    ).fillna({"Change": 0}).sort_values(by="Change", ascending=False)

@st.cache_data
def get_figure(current_max_date):
    data18w12_transformed = transform_data(current_max_date)
    
    fig = make_subplots(
        rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0,
        column_widths=[1, 3],
    )

    cols = data18w12_transformed.columns
    colors = {"Most Recent Month": "#26897E", "Prior Month": "#8DBFA8"}
    gridColor = "#DBDBDB"
    sepLineColor = "#D4D4D4"
    textPos = 1
    last_two_priods = get_last_two_periods_format(current_max_date)

    fig.add_traces([
        go.Scatter(
        mode="text",
        x=[textPos-0.05] * len(data18w12_transformed),
        y=data18w12_transformed.index,
        text=[f"{x:+.1%}" for x in data18w12_transformed["Change"]],
        textposition="middle left",
        showlegend=False,
        ),
        go.Scatter(
            mode="text",
            x=[0] * len(data18w12_transformed),
            y=data18w12_transformed.index,
            text=data18w12_transformed.index,
            textposition="middle right",
            showlegend=False,
        )
    ], rows=1, cols=1)

    fig.add_annotation(
        text="<b>Sub-Category</b>",
        x=0, xref="x domain", xanchor="left",
        y=0.97, yref="y domain", yanchor="bottom",
        showarrow=False,
    )
    fig.add_annotation(
        text="<b>Change</b>",
        x=0.98, xref="x domain", xanchor="right",
        y=0.97, yref="y domain", yanchor="bottom",
        showarrow=False,
    )

    fig.add_vline(
        x=textPos,
        row=1, col=1,
        line=dict(
            color=sepLineColor,
            width=2,
        )
    )

    for row in data18w12_transformed.index:
        change = (data18w12_transformed.loc[row, cols[0]] - data18w12_transformed.loc[row, cols[1]]) / data18w12_transformed.loc[row, cols[1]]
        if pd.isna(change):
            change = 0
        fig.add_trace(go.Scatter(
            mode="lines",
            name="Change",
            meta=[f"{change:+.1%}"],
            x=data18w12_transformed.loc[row, cols[:2]],
            y=[row, row],
            showlegend=False,
            line=dict(
                color=gridColor,
                width=1.5,
            ),
            hovertemplate="%{meta[0]}",
        ), row=1, col=2)

    for i, col in enumerate(cols[:2]):
        fig.add_trace(go.Scatter(
            mode="markers",
            name="%{meta[0]}",
            meta=[col, last_two_priods[i]],
            x=data18w12_transformed[col],
            y=data18w12_transformed.index,
            marker=dict(
                color=colors[col],
                size=10,
            ),
            hovertemplate="%{x}<extra>%{meta[1]}</extra>",
            selected_marker=dict(color="red"),
        ), row=1, col=2)

    fig.update_layout(
        width=600, height=700,
        plot_bgcolor="white",
        xaxis=dict(
            range=[0, textPos],
            showticklabels=False,
            showgrid=False,
        ),
        yaxis=dict(
            tickson="boundaries",
            gridcolor=gridColor,
            gridwidth=1,
            showticklabels=False,
        ),
        yaxis2=dict(
            tickson="boundaries",
            gridcolor=gridColor,
            gridwidth=1,
            showticklabels=False,
        ),
        xaxis2=dict(
            side="top",
            nticks=8,
            tickformat="$,.0f",
            zeroline=False,
            showgrid=False,
            title=dict(
                text="Sales (Last Two Periods)",
                standoff=5,
            ),
        ),
        legend=dict(
            orientation="h",
            x=0.65, xref="paper", xanchor="center",
            y=0, yref="paper", yanchor="top",
            traceorder="reversed",
        ),
        margin=dict(
            l=20, r=20, b=20,
        ),
        hovermode="y unified",
    )

    return fig