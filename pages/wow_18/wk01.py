import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import assets


data18w01 = pd.read_csv(assets.DATA_18W01)

filter_cond = data18w01["Measure"].str.contains("Ranked personality higher than looks")
data18w01_filtered = (
    data18w01.loc[filter_cond, :]
    .pivot(index="Nationality", columns="Gender", values="Value")
    .sort_values(by=["Women", "Men"])
)

fig = go.Figure()

# Bar background
bar_fg = "#D5D6D8"
data = [
    go.Bar(
        x=[10] * len(data18w01_filtered),
        y=data18w01_filtered.index,
        orientation="h",
        marker=dict(
            color=bar_fg,
            line_width=2,
            line_color="white",
        ),
        showlegend=False,
        hoverinfo="none",
    )
    for _ in range(10)
]
fig.add_traces(data)

# Line trace
fig.add_trace(
    go.Scatter(
        x=[55, 83, None, 52, 79, None, 46, 64],
        y=[
            "Egyptian",
            "Egyptian",
            None,
            "Saudi Arabian",
            "Saudi Arabian",
            None,
            "Vietnamese",
            "Vietnamese",
        ],
        mode="lines",
        showlegend=False,
        hoverinfo="none",
        marker=dict(
            color="black",
        ),
    )
)

# Dot trace
marker_fg = marker_fg = "#449EA0"
marker_size = 16
for sex in data18w01_filtered.columns:
    fig.add_trace(
        go.Scatter(
            x=data18w01_filtered[sex],
            y=data18w01_filtered.index,
            mode="markers",
            name=sex,
            meta=[sex],
            marker=dict(
                color=marker_fg,
                size=marker_size,
                line_width=3,
                line_color=marker_fg,
            ),
            hovertemplate="<b>%{y}</b><br>%{meta[0]}: <b>%{x}%</b><extra></extra>",
        )
    )

fig.update_traces(
    selector=dict(type="scatter", name="Women"),
    marker=dict(
        color="white",
    ),
)

fig.add_vline(
    x=0,
    xref="x domain",
    line_width=2,
)
fig.add_vline(
    x=1,
    xref="x domain",
    line_width=2,
)
fig.add_vline(
    x=0.5,
    xref="x domain",
    line=dict(
        width=1.5,
        dash="dash",
    ),
)

fig.add_annotation(
    text=(
        '<span style="color: red; font-size: 16">You</span>'
        '<span style="color: #B4B4B4; font-size: 16">Gov | </span>'
        '<span style="color: #BDBDBD;">yougov.com</span>'
    ),
    x=-0.22,
    xanchor="left",
    xref="paper",
    y=-0.05,
    yanchor="bottom",
    yref="paper",
    showarrow=False,
)
fig.add_annotation(
    text=('<span style="color: #BDBDBD;">July 23 - August 30, 2017</span>'),
    x=1.02,
    xanchor="right",
    xref="paper",
    y=-0.05,
    yanchor="bottom",
    yref="paper",
    showarrow=False,
)

fig.add_annotation(
    text=(
        "The biggest differences<br>"
        "in opinion between a<br>"
        "nation's men and women<br>"
        "were in Egypt and<br>"
        "Saudi Arabia (both 28%)"
    ),
    ax=45,
    xanchor="right",
    axref="x",
    ay=8,
    yanchor="middle",
    ayref="y",
    x=65,
    xref="x",
    y=10,
    yref="y",
    align="left",
    arrowhead=3,
    bgcolor="white",
    bordercolor="black",
    standoff=10,
)
fig.add_annotation(
    text="",
    ax=45,
    xanchor="right",
    axref="x",
    ay=8,
    yanchor="middle",
    ayref="y",
    x=65,
    xref="x",
    y=6,
    yref="y",
    arrowhead=3,
    standoff=10,
)

fig.add_annotation(
    text=(
        "Vietnamese men<br>"
        "werethe only group<br>"
        "who weremore likely<br>"
        "to value a partner's<br>"
        "looks more than their<br>"
        "personality"
    ),
    ax=40,
    xanchor="right",
    axref="x",
    ay=2,
    yanchor="middle",
    ayref="y",
    x=55,
    xref="x",
    y=1,
    yref="y",
    standoff=10,
    align="left",
    arrowhead=3,
    bgcolor="white",
    bordercolor="black",
)

fig.add_annotation(
    text=(
        "% of people who ranked a romantic partner having a personality <br>"
        "they liked as more important than them being good looking"
    ),
    x=0,
    xref="paper",
    y=1,
    yref="paper",
    yanchor="bottom",
    showarrow=False,
    font_size=16,
    align="left",
    yshift=60,
    xshift=-40,
)

fig.update_layout(
    width=600,
    height=700,
    xaxis=dict(
        range=[0, 100],
        showgrid=False,
        title_text="",
        side="top",
        tickfont_size=14,
        tickmode="array",
        tickvals=[0, 50, 100],
        ticktext=["0", "50%", "100%"],
    ),
    yaxis=dict(
        range=[-0.5, len(data18w01_filtered) - 0.5],
        title_text="",
        tickfont_size=14,
        ticksuffix="  ",
    ),
    barmode="stack",
    plot_bgcolor="white",
    legend=dict(
        orientation="h",
        title_text="",
        x=0.5,
        xanchor="right",
        xref="paper",
        y=1.05,
        yanchor="bottom",
        yref="paper",
    ),
    title=dict(
        text=(
            "<b>Across the world women are more likely than men to value "
            "personality over looks</b><br>"
        ),
        x=0, xref="paper", xanchor="left",
        y=1, yref="paper", yanchor="bottom",
        pad=dict(
            b=115, l=-40,
        )
    ),
    margin=dict(
        t=160,
        b=35,
        l=5,
        r=5,
    ),
    hoverlabel=dict(
        bgcolor="white",
    ),
)
