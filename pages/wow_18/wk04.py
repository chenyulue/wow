import plotly.graph_objects as go
import pandas as pd
import assets


data18w04 = pd.read_csv(
    assets.DATA_18W04,
    index_col=0,
    parse_dates=["Order Date", "Ship Date"],
    engine="pyarrow",
)

data18w04_grouped = (
    data18w04.loc[:, ["Customer Name", "Sales"]]
    .groupby(by=["Customer Name", data18w04["Order Date"].dt.year])
    .sum()
)

filter_cond = []
four_years = (2014, 2015, 2016, 2017)
for customer in data18w04_grouped.index.get_level_values("Customer Name").unique():
    customer_order = data18w04_grouped.loc[customer, :]
    if tuple(customer_order.index) == four_years:
        reordered_index = customer_order.sort_values(by="Sales").index
        if tuple(reordered_index) == four_years:
            filter_cond.append(customer)

data18w04_filtered = (
    data18w04_grouped.loc[filter_cond, :]
    .unstack()
    .droplevel(level=0, axis=1)
    .sort_values(by=2017, ascending=False)
)

rowEvenColor = "#F5F5F5"
rowOddColor = "white"
cellFillColors = [
    [rowOddColor, rowEvenColor]
    * (data18w04_filtered.shape[0] // 2)
    * (data18w04_filtered.shape[1] + 1)
]

lineColor = "#C9C9C9"

fig = go.Figure()

fig.add_trace(
    go.Table(
        header=dict(
            values=[""] + [f"<b>{x}</b>" for x in data18w04_filtered.columns],
            fill_color="white",
            align=["left", "right"],
            height=25,
        ),
        cells=dict(
            values=[
                [f"<b>{x}</b>" for x in data18w04_filtered.index],
                data18w04_filtered[2014],
                data18w04_filtered[2015],
                data18w04_filtered[2016],
                data18w04_filtered[2017],
            ],
            fill_color=cellFillColors,
            format=["", ",.0f"],
            prefix=["", "$"],
            align=["left", "right"],
            height=25,
        ),
        hoverinfo="x+y+z",
        columnwidth=[1.5, 1],
    )
)

fig.add_hline(
    y=data18w04_filtered.shape[0] / (data18w04_filtered.shape[0] + 1),
    yref="paper",
)

fig.update_layout(
    width=680,
    height=640,
    margin=dict(
        t=40,
        b=10,
        l=10,
        r=10,
    ),
    title=dict(
        text="<b>These Customers just go up and up!</b>",
        x=0.5,
        xref="container",
        xanchor="center",
        y=0.98,
        yref="container",
        yanchor="top",
        font_size=20,
        font_color="#508E48",
    ),
)
