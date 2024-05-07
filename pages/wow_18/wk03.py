import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import streamlit as st
import assets


data18w03 = pd.read_csv(
    assets.DATA_18W03,
    index_col=0,
    parse_dates=["Order Date", "Ship Date"],
    engine="pyarrow",
)

filter_cond = (data18w03["Order Date"] >= datetime(2014, 1, 1)) & (
    data18w03["Order Date"] <= datetime(2018, 3, 30)
)
xlim = (datetime(2014, 1, 1), datetime(2018, 3, 30))

data18w03_filtered = data18w03.loc[filter_cond, ["Order Date", "Category", "Sales"]]

data18w03_grouped = (
    data18w03_filtered.assign(
        Year_Month=data18w03_filtered["Order Date"].apply(lambda d: d.replace(day=1))
    )
    .groupby(by=["Category", "Year_Month"])
    .agg({"Order Date": "min", "Sales": "sum"})
)


@st.cache_data
def get_figure(param_date):
    colors = {
        "Technology": "#ADA758",
        "Furniture": "#AA7E93",
        "Office Supplies": "#71A790",
    }

    data_left = []
    data_right = []
    data_text = []
    for cat in data18w03_grouped.index.get_level_values("Category").unique():
        cat_data = (
            data18w03_grouped.loc[(cat,), "Sales"].rolling(3, min_periods=1).sum()
        )

        filter = cat_data.index <= param_date
        data_left.append(
            go.Scatter(
                name=cat,
                x=cat_data.index[filter],
                y=cat_data[filter],
                stackgroup="left",
                line=dict(
                    color=colors[cat],
                ),
            )
        )
        data_left.sort(key=lambda f: f.y[-1])

        not_filter = cat_data.index >= param_date
        data_right.append(
            go.Scatter(
                name=cat,
                x=cat_data.index[not_filter],
                y=cat_data[not_filter],
                stackgroup="right",
                line=dict(
                    color="#838383",
                    width=1,
                ),
                showlegend=False,
            )
        )
        data_right.sort(key=lambda f: f.y[0])

        data_text.append(
            go.Scatter(
                mode="text",
                x=[param_date],
                y=[cat_data[param_date]],
                text=[f" <b>{cat}</b><br> ${cat_data[param_date]/1000:.1f}K"],
                stackgroup="text",
                textposition="middle right",
                # textfont_weight="bold",
                showlegend=False,
            )
        )
        data_text.sort(key=lambda f: f.y[0])

    fig = go.Figure(data=data_left + data_right + data_text)

    fig.add_vline(
        x=param_date,
        line=dict(
            dash="dot",
        ),
    )

    fig.update_layout(
        width=800,
        height=600,
        legend=dict(
            x=0,
            xref="paper",
            y=1,
            yref="paper",
            yanchor="middle",
            orientation="h",
        ),
        plot_bgcolor="white",
        yaxis=dict(
            gridcolor="#A5A5A5",
            tickprefix="$",
        ),
        xaxis=dict(
            ticks="outside",
            tickwidth=1.5,
            tickformat="%b-%y",
            minor_ticks="outside",
            minor_nticks=2,
            minor_tickwidth=1,
            range=xlim,
        ),
        title=dict(
            text="<b>#WorkoutWednesday</b>",
            font_color="#C3BC3F",
            font_size=24,
            x=0.5,
            xref="container",
            xanchor="center",
            y=0.98,
            yref="container",
            yanchor="top",
        ),
    )
    fig.add_annotation(
        text="<i>Rolling three month sales: a retrospective</i>",
        font_size=18,
        showarrow=False,
        x=0.5,
        xref="paper",
        xanchor="center",
        y=1.09,
        yref="paper",
        yanchor="bottom",
    )
    fig.add_annotation(
        text="Categories ordered by sales",
        font_size=10,
        showarrow=False,
        x=0.5,
        xref="paper",
        xanchor="center",
        y=1.09,
        yref="paper",
        yanchor="top",
    )
    fig.add_annotation(
        text="Dataset: Superstore Sample | Designed by: Chenyu Lue",
        font_size=10,
        font_color="gray",
        showarrow=False,
        x=1,
        xref="paper",
        xanchor="right",
        y=-0.08,
        yref="paper",
        yanchor="top",
    )
    return fig
