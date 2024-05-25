import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import streamlit as st
import assets

@st.cache_data
def load_data() -> pd.DataFrame:
    data18w09 = pd.read_csv(assets.DATA_18W09, parse_dates=["Year"], engine="pyarrow")
    return data18w09.assign(
        Percentage_of_Players=data18w09["% of Players"].str.rstrip("%").astype(float) / 100.0
    )

@st.cache_data
def get_figure() -> go.Figure:
    data18w09 = load_data()
    is_white = data18w09["Ethnicity"] == "White"
    WHITE = "white" #"#D3D3D3"
    COLOR = "#8CD17D"
    FILL_COLOR = "#21252B"
    VLINE_COLOR = "#898989"

    HOVER_TEMPLATE = "%{y:.1%}<br>%{meta[0]}<extra></extra>"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        mode="lines",
        name="White",
        meta=["White"],
        x=data18w09.loc[is_white, "Year"],
        y=data18w09.loc[is_white, "Percentage_of_Players"],
        marker_color=WHITE,
        showlegend=False,
        hovertemplate=HOVER_TEMPLATE,
    ))

    data18w09_color_players = data18w09.loc[~is_white, :].groupby(by="Year").sum(numeric_only=True)

    fig.add_trace(go.Scatter(
        mode="lines",
        name="Players of Color",
        meta=["Players of Color"],
        x=data18w09_color_players.index,
        y=data18w09_color_players["Percentage_of_Players"],
        marker_color=COLOR,
        showlegend=False,
        hovertemplate=HOVER_TEMPLATE,
        fill="tonexty",
        fillcolor=FILL_COLOR,
    ))

    ANNOTATION_X = datetime(2004, 1, 1)
    fig.add_vline(
        x=ANNOTATION_X,
        line=dict(
            color=VLINE_COLOR,
            dash="dot",
        ),
        label=dict(
            text="2004 The percent of<br>Minority Players<br>begins to decline",
            textangle=0,
            textposition="end",
            yanchor="top",
            font_color="white",
            padding=40,
        )
    )

    fig.update_layout(
        width=800, height=500,
        paper_bgcolor="black",
        plot_bgcolor="black",
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(
                color=WHITE,
            ),
            tickformat=".0%",
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="black",
            ticks="outside",
            tickcolor=WHITE,
            tickfont=dict(
                color=WHITE,
            ),
            nticks=20,
        ),
        hovermode="x",
        margin_b=5,
    )

    # Add title and description
    Y_SHIFT, X_SHIFT = 50, -20
    fig.update_layout(
        title=dict(
            text="<b>The MLB Diversity Gap</b>",
            x=0, xref="paper", xanchor="left",
            y=1, yref="paper", yanchor="bottom",
            font=dict(
                color=WHITE,
                size=32,
            ),
            pad=dict(
                b=Y_SHIFT, l=X_SHIFT,
            )
        )
    )
    description = ("Since Jackie Robinson broke the Color Barrir in 1947, the MLB "
                "has grown more diverse. However, in 2016,White Players still<br>"
                "represented 63% of league. Additionally, since 2004, the percentage of "
                f"<span style='color:{COLOR}'>Players of color is declining</span>, "
                "falling from 39% to 36%.")
    fig.add_annotation(
        text=description,
        x=0, xref="paper", xanchor="left",
        y=1, yref="paper", yanchor="bottom",
        showarrow=False,
        font=dict(
            color=WHITE,
        ),
        align="left",
        xshift=X_SHIFT,
        yshift=Y_SHIFT/10,
    )

    return fig