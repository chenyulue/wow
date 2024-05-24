import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta
import streamlit as st
import assets


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(assets.DATA_18W08, parse_dates=["year"], engine="pyarrow")


@st.cache_data
def transform_data(name: str) -> tuple[bool, pd.DataFrame]:
    data18w08 = load_data()
    filter_name = data18w08["name"] == name.title()
    name_found = any(filter_name)
    if not name_found:
        filter_name = data18w08["name"] == "Rody"
        name = "Rody"

    return name_found, data18w08.loc[filter_name, ["year", "sex", "name", "n"]]


@st.cache_data
def get_figure(name: str) -> go.Figure:
    name_found, data18w08_filtered = transform_data(name)
    if not name_found:
        name = "Rody"
    sexMap = {"M": ("Male", "#F3D744"), "F": ("Female", "#87D6BD")}

    fig = go.Figure()

    sexNumOrder = (
        data18w08_filtered.groupby(by="sex")
        .sum(numeric_only=True)
        .sort_values(by="n", ascending=False)
        .index
    )
    for sex in sexNumOrder:
        dataBySex = data18w08_filtered.query("sex==@sex")
        maxNameNum = dataBySex["n"].max()
        dataMaxBySex = dataBySex.query("n==@maxNameNum")

        tmpdf = pd.DataFrame(
            {
                "n": 0,
                "year": pd.date_range(
                    start=dataBySex["year"].min(),
                    end=dataBySex["year"].max(),
                    freq="YS",
                ),
            }
        )
        plotData = tmpdf.merge(dataBySex, how="left", on="year").fillna(0)

        fig.add_traces(
            [
                go.Scatter(
                    mode="text",
                    name=f"{sex}_name",
                    x=dataMaxBySex["year"],
                    y=dataMaxBySex["n"],
                    text=f"<b>{sexMap[sex][0]}</b><br>Peaked in {dataMaxBySex['year'].dt.year.iloc[0]}",
                    textposition="top center",
                    showlegend=False,
                    cliponaxis=False,
                    hoverinfo="none",
                ),
                go.Scatter(
                    mode="lines",
                    name=f"{sexMap[sex][0]}",
                    x=plotData["year"],
                    y=plotData["n_y"],
                    fill="tozeroy",
                    marker_color=sexMap[sex][1],
                    meta=[f"{sexMap[sex][0]}"],
                    hovertemplate="<b>%{x|%Y}</b><br>%{meta[0]}: %{y:,.0f}<extra></extra>",
                ),
            ]
        )

    title = dict(
        text=f"Births by year in U.S.<br><b><span style='font-size: 20px'>{name.title()}</span></b>",
        x=0.5,
        xref="paper",
        xanchor="center",
        y=1,
        yref="paper",
        yanchor="bottom",
        pad_b=70,
    )

    fig.update_layout(
        width=600,
        height=500,
        title=title,
        plot_bgcolor="white",
        xaxis=dict(
            range=[
                data18w08_filtered["year"].min() - timedelta(days=2000),
                data18w08_filtered["year"].max() + timedelta(days=1500),
            ],
            gridcolor="#E5EDF5",
            linecolor="black",
            ticks="outside",
        ),
        yaxis=dict(
            gridcolor="#E5EDF5",
            ticksuffix="  ",
        ),
        legend=dict(
            orientation="h",
            x=0.5,
            xref="paper",
            xanchor="center",
            y=1.04,
            yref="paper",
            yanchor="bottom",
            entrywidth=100,
            traceorder="reversed",
        ),
        hovermode="x",
        margin=dict(
            b=10,
            l=10,
            r=10,
        ),
    )

    return fig
