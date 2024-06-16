# Plotly
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Data manipulation
import pandas as pd
import numpy as np

# Resources
import assets

@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W14,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )

@st.cache_data
def calculate_data():
    data18w14 = load_data()
    
    data18w14_grouped = data18w14.loc[:, ["Order ID", "Sub-Category", "Sales"]].groupby(
        by=["Sub-Category", "Order ID"],
    ).sum()

    sub_categories = data18w14["Sub-Category"].unique()

    data = []
    for cat1 in sub_categories:
        for cat2 in sub_categories:
            if cat1 == cat2:
                tmp = data18w14_grouped.loc[cat1, :]
                avg = tmp.mean().iloc[0]
                data.append({"sub-cat1": cat1, "sub-cat2": cat2, "count-cat": len(tmp), "avg-cat1": avg, "avg-cat2": avg})
            else:
                tmp1 = data18w14_grouped.loc[cat1, :]
                tmp2 = data18w14_grouped.loc[cat2, :]
                tmp = tmp1.merge(tmp2, how="inner", left_index=True, right_index=True)
                avgs = tmp.mean()
                freq = len(tmp)
                data.append({"sub-cat1": cat1, "sub-cat2": cat2, "count-cat": freq, "avg-cat1": avgs.iloc[0], "avg-cat2": avgs.iloc[1]})

    data18w14_calculated = pd.DataFrame(data).set_index(
        ["sub-cat1", "sub-cat2"],
    )
    return data18w14_calculated.sort_index(
        key=lambda idx: [data18w14_calculated.loc[(r, r), "count-cat"] for r in idx]
    ).reset_index()

@st.cache_data
def get_figure():
    data18w14_calculated = calculate_data()
    
    diag_cond = data18w14_calculated["sub-cat1"]==data18w14_calculated["sub-cat2"]
    non_diag = data18w14_calculated.loc[~diag_cond, :]
    diag = data18w14_calculated.loc[diag_cond, :]

    labelalias = {k: k.upper() for k in diag["sub-cat1"]}

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        x=diag["sub-cat1"],
        y=diag["sub-cat2"],
        z=diag["count-cat"],
        texttemplate="%{z:,.0f}",
        autocolorscale=False,
        colorscale=[[0, "white"],[1, "white"]],
        showscale=False,
        xgap=1.5, ygap=1.5,
        customdata=diag,
        hovertemplate=("<b>%{z:,.0f}</b> unique orders included <b>%{customdata[0]}</b><br><br>"
                    "Average sales per order<br>"
                    "%{customdata[0]}: <b>%{customdata[3]:$,.2f}</b><extra></extra>"
        ),
        hoverlabel=dict(
            bgcolor="white",
            align="left",
        ),
        hoverongaps=False,
    ))

    fig.add_trace(go.Heatmap(
        x=non_diag["sub-cat1"],
        y=non_diag["sub-cat2"],
        z=non_diag["count-cat"],
        colorscale=[[0, "#D9D9D9"], [1, "#B36CC1"]],
        xgap=1.5, ygap=1.5,
        customdata=non_diag,
        hovertemplate=("<b>%{z:,0f}</b> unique orders included <b>%{customdata[0]} & %{customdata[1]}</b><br><br>"
                    "Average sales per order<br>"
                    "%{customdata[0]}: <b>%{customdata[3]:$,.2f}</b><br>"
                    "%{customdata[1]}: <b>%{customdata[4]:$,.2f}</b><extra></extra>"
        ),
        hoverlabel=dict(
            bgcolor="white",
            align="left",
        ),
        showscale=False,
        hoverongaps=False,
    ))

    max_cat1, max_cat2 = non_diag.assign(
        avgTotal=non_diag["avg-cat1"]+non_diag["avg-cat2"]
    ).sort_values(by="avgTotal", ascending=False).iloc[0, [0, 1]]
    fig.add_traces([
        go.Scatter(
            mode="markers",
            x=[max_cat1], y=[max_cat2],
            hovertemplate=("<b>%{customdata[2]:,0f}</b> unique orders included <b>%{customdata[0]} & %{customdata[1]}</b><br><br>"
                    "Average sales per order<br>"
                    "%{customdata[0]}: <b>%{customdata[3]:$,.2f}</b> highest average sales per order<br>"
                    "%{customdata[1]}: <b>%{customdata[4]:$,.2f}</b> highest average sales per order<extra></extra>"
                    ),
        ),
        go.Scatter(
            mode="markers",
            x=[max_cat2], y=[max_cat1],
            hovertemplate=("<b>%{customdata[2]:,0f}</b> unique orders included <b>%{customdata[1]} & %{customdata[0]}</b><br><br>"
                    "Average sales per order<br>"
                    "%{customdata[1]}: <b>%{customdata[4]:$,.2f}</b> highest average sales per order<br>"
                    "%{customdata[0]}: <b>%{customdata[3]:$,.2f}</b> highest average sales per order<extra></extra>"
                    ),
        )
    ])
    fig.update_traces(
        showlegend=False,
        marker_color="black",
        customdata=non_diag.assign(avgTotal=non_diag["avg-cat1"]+non_diag["avg-cat2"]).sort_values(by="avgTotal", ascending=False).iloc[[0],:],
        hoverlabel=dict(
            bgcolor="white",
            align="left",
        ),
        selector=dict(type="scatter")
    )

    fig.add_annotation(
        text="#Workout Wednesday, Week 14, 2018",
        x=0, xref="paper", xanchor="left",
        y=0, yref="paper", yanchor="top",
        showarrow=False,
        font=dict(
            color="#909090",
        )
    )
    fig.add_annotation(
        text="Designed by: Chenyu Lue",
        x=1, xref="paper", xanchor="right",
        y=0, yref="paper", yanchor="top",
        showarrow=False,
        font=dict(
            color="#909090",
        )
    )

    fig.update_layout(
        width=1000, height=900,
        plot_bgcolor="white",
        yaxis=dict(
            labelalias=labelalias,
            showgrid=False,
            ticks="",
        ),
        xaxis=dict(
            labelalias=labelalias,
            autorange="reversed",
            side="top",
            tickangle=-90,
            showgrid=False,
            ticks="",
        ),
        margin=dict(
            r=30, b=30
        )
    )

    return fig