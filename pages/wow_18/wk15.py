
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import streamlit as st

# Data manipulation
import pandas as pd

# Resources
import assets

@st.cache_data
def load_data():
    return pd.read_csv(
        assets.DATA_18W15,
        index_col=0,
        parse_dates=["Order Date", "Ship Date"],
        engine="pyarrow",
    )


def sort_func(col):
    if pd.api.types.is_object_dtype(col):
        return pd.Series([(col==item).sum() for item in col])
    else:
        return col

@st.cache_data
def transform_data():
    data18w15 = load_data()
    return data18w15.loc[:, ['Sub-Category', 'Product Name', 'Order Date', 'Sales']].groupby(
        by=['Sub-Category', 'Product Name']
    ).agg({'Order Date': 'min', 'Sales': 'sum'}).reset_index().sort_values(
        by=['Sub-Category', 'Order Date'], key=sort_func
    )

# Intermediate
@st.cache_data
def get_intermediate_figure():
    data18w15_transformed = transform_data()
    
    top5 = data18w15_transformed['Sub-Category'].unique()[-5:]
    colors = ['#9E3A26', '#CF4F22', '#F49538']

    fig = make_subplots(
        rows=1, cols=5,
        shared_yaxes=True,
        horizontal_spacing=0.01,
    )

    for i, subcat in enumerate(top5):
        sub_cat = data18w15_transformed.query("`Sub-Category`==@subcat").sort_values(
            by='Sales', ascending=False).reset_index(drop=True)

        group_offset = sub_cat.index // 10 // 10
        sub_cat_with_coords = sub_cat.assign(
            x=sub_cat.index % 10,
            y=sub_cat.index // 10 + group_offset,
            color=[colors[i] for i in group_offset],
        )

        fig.add_trace(go.Scatter(
            mode="markers",
            x=sub_cat_with_coords['x'],
            y=sub_cat_with_coords['y'],
            marker=dict(
                color=sub_cat_with_coords['color'],
                size=8,
            ),
            showlegend=False,
            customdata=sub_cat.loc[:, ["Product Name", "Sales"]],
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]:$,.2f}<extra></extra>",
            hoverlabel=dict(
                bgcolor="white",
                align="left",
            )
        ), row=1, col=5-i)

        fig.update_layout(**{
            f"yaxis{5-i if i < 4 else ''}": dict(
                showgrid=False,
                zeroline=False,
                range=[-1, 32],
                showticklabels=False,
                scaleratio=2,
            ),
            f"xaxis{5-i if i < 4 else ''}": dict(
                showgrid=False,
                zeroline=False,
                range=[-3, 12],
                showticklabels=False,
                showline=True,
                linecolor="black",
            )
        })

        sub_title = sub_cat["Sub-Category"].iloc[0]
        count = len(sub_cat)
        fig.add_annotation(
            text=f"<b>{sub_title}</b><br>({count} products)",
            x=0.5, xref=f"x{5-i if i < 4 else ''} domain", xanchor="center",
            y=0.95, yref=f"y{5-i if i < 4 else ''} domain", yanchor="bottom",
            showarrow=False,
        )

    fig.add_annotation(
        text=("1 dot = 1 product<br><br>"
            f"<span style='color:{colors[0]};font-size:18'>•</span>1st 100 | "
            f"<span style='color:{colors[1]};font-size:18'>•</span>2nd 100 | "
            f"<span style='color:{colors[2]};font-size:18'>•</span>3rd 100"),
        x=0.5, xref="paper", xanchor="center",
        y=1, yref="paper", yanchor="bottom",
        showarrow=False,
        yshift=35,
    )

    fig.update_layout(
        width=850, height=480,
        plot_bgcolor="white",
        margin=dict(
            l=10, r=10, b=40, t=130
        ),
        title=dict(
            text="<b>TOP 5 SUB-CATEGORIES WITH THE MOST PRODUCTS</b>",
            x=0.5, xref="paper", xanchor="center",
            y=1, yref="paper", yanchor="bottom",
            pad_b=90,
        ),
    )

    return fig


# Jedi
@st.cache_data
def get_jedi_figure():
    data18w15_transformed = transform_data()
    sub_cats = data18w15_transformed['Sub-Category'].unique()[::-1]
    colors = {2014: '#4E9F50', 2015: '#87D180', 2016: '#F7D42A', 2017: '#EF8A0C'}
    icons = {
        "Paper": "📝",
        "Binders": "📒",
        "Phones": "📞",
        "Furnishings": "📻",
        "Art": "🎨",
        "Accessories": "📫",
        "Storage": "📦",
        "Appliances": "💻",
        "Chairs": "💺",
        "Labels": "🔖",
        "Machines": "⏰",
        "Tables": "🔷",
        "Bookcases": "📚",
        "Envelopes": "✉️",
        "Supplies": "✂️",
        "Fasteners": "📌",
        "Copiers": "📠",
    }

    fig = make_subplots(
        rows=4, cols=5,
        shared_yaxes=True,
        horizontal_spacing=0.01,
        vertical_spacing=0.02,
    )

    for i, subcat in enumerate(sub_cats):
        sub_cat = data18w15_transformed.query("`Sub-Category`==@subcat").reset_index(drop=True)

        group_offset = sub_cat.index // 10 // 10
        sub_cat_with_coords = sub_cat.assign(
            x=sub_cat.index % 10,
            y=sub_cat.index // 10 + group_offset,
            color=[colors[key.year] for key in sub_cat["Order Date"]],
        )

        row = i // 5 + 1
        col = i % 5 + 1
        fig.add_trace(go.Scatter(
            mode="markers",
            x=sub_cat_with_coords['x'],
            y=sub_cat_with_coords['y'],
            marker=dict(
                color=sub_cat_with_coords['color'],
                size=5,
            ),
            showlegend=False,
            customdata=sub_cat.loc[:, ["Product Name", "Order Date"]],
            hovertemplate="<b>%{customdata[0]}</b><br>Introduced on %{customdata[1]|%Y/%m/%d}<extra></extra>",
            hoverlabel=dict(
                bgcolor="white",
                align="left",
            )
        ), row=row, col=col)

        fig.update_layout(**{
            f"yaxis{i+1 if i>0 else ''}": dict(
                showgrid=False,
                zeroline=False,
                range=[-1, 40],
                showticklabels=False,
                scaleratio=2,
            ),
            f"xaxis{i+1 if i>0 else ''}": dict(
                showgrid=False,
                zeroline=False,
                range=[-3, 12],
                showticklabels=False,
                showline=True,
                linecolor="black",
            )
        })

        sub_title = sub_cat["Sub-Category"].iloc[0]
        count = len(sub_cat)
        ymax = sub_cat_with_coords["y"].max()
        fig.add_annotation(
            text=f"<b>{sub_title}</b> {icons[sub_title]}<br>{count} products",
            x=0.5, xref=f"x{i+1 if i>0 else ''} domain", xanchor="center",
            y=ymax, yref=f"y{i+1 if i>0 else ''}", yanchor="bottom",
            showarrow=False, yshift=10,
        )


    fig.add_annotation(
        text=("1 dot = 1 product<br><br>Year of Introduction<br>"
            f"<span style='color:{colors[2014]};font-size:18'>•</span>2014 | "
            f"<span style='color:{colors[2015]};font-size:18'>•</span>2015 | "
            f"<span style='color:{colors[2016]};font-size:18'>•</span>2016 | "
            f"<span style='color:{colors[2017]};font-size:18'>•</span>2017"),
        x=0.5, xref="paper", xanchor="center",
        y=1, yref="paper", yanchor="bottom",
        showarrow=False,
        yshift=5,
    )

    fig.update_layout(
        width=550, height=1200,
        plot_bgcolor="white",
        margin=dict(
            l=10, r=10, b=10,
        ),
        title=dict(
            text="<b>TOTAL PRODUCTS BY SUB-CATEGORY</b>",
            x=0.5, xref="paper", xanchor="center",
            y=1, yref="paper", yanchor="bottom",
            pad_b=75,
        ),
    )

    return fig