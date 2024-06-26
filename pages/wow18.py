import streamlit as st
from datetime import datetime, timedelta
import menu

menu.side_navigation()

options = {
    "wow18wk01": "Week 01: Looks vs. Personality",
    "wow18wk02": "Week 02: Year to Fiscal Date Running Totals",
    "wow18wk03": "Week 03: Rolling three month sales",
    "wow18wk04": "Week 04: Tables",
    "wow18wk05": "Week 05: Q1 and Q2 compared to other months",
    "wow18wk06": "Week 06: Regional Sales Across the Product Hierarchy",
    "wow18wk07": "Week 07: Min and Max Sales by Month",
    "wow18wk08": "Week 08: Is it a trending baby name?",
    "wow18wk09": "Week 09: Highlighting all points in the year",
    "wow18wk10": "Week 10: Keep an Eye on Sales",
    "wow18wk11": "Week 11: Small Multiple Grids with Text",
    "wow18wk12": "Week 12: Sub-Category Sales Change in the Last Two Periods",
    "wow18wk13": "Week 13: Color and Ordering",
    "wow18wk14": "Week 14: Frequency Matrix",
    "wow18wk15": "Week 15: Total Products by Sub-Category OR Top 5 Sub-Categories by Total Product",
    "wow18wk16": "Week 16: Sales for the last N vs. same time previous year",
}

challenge = st.selectbox(
    "Please select the challenge of the year 2018: ",
    options=options.keys(),
    format_func=lambda idx: options[idx],
    placeholder="Choose a challenge",
)

if challenge == "wow18wk01":
    st.markdown(
        "[Challenge source](https://www.vizwiz.com/2018/01/ww-looks-vs-personality.html): Workout Wednesday: Looks vs. Personality"
    )
elif challenge == "wow18wk02":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/workout-wednesday-2018-week-2-year-to-fiscal-date-running-totals/): Workout Wednesday: Year to Fiscal Date Running Totals"
    )
elif challenge == "wow18wk03":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/week3/): Workout Wednesday: Rolling three month sales"
    )
elif challenge == "wow18wk04":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/workoutwednesday-week4/): Workout Wednesday: Tables"
    )
elif challenge == "wow18wk05":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/workoutwednesday-2018-week-5/): Q1 and Q2 compared to other months"
    )
elif challenge == "wow18wk06":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/workoutwednesday-week-6-regional-sales-across-the-product-hierarchy/): Regional Sales Across the Product Hierarchy"
    )
elif challenge == "wow18wk07":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/min-and-max-sales-by-month/): Min and Max Sales by Month"
    )
elif challenge == "wow18wk08":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/week-8-is-it-a-trending-baby-name/): Is it a trending baby name?"
    )
elif challenge == "wow18wk09":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/week-9-highlighting-all-points-in-the-year/): Highlighting all points in the year"
    )
elif challenge == "wow18wk10":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/week-10/): Keep an Eye on Sales"
    )
elif challenge == "wow18wk11":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/workout-wednesday-week-11/): Small Multiple Grids with Text"
    )
elif challenge == "wow18wk12":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/week-11-sub-category-sales-change-in-the-last-two-periods/): Sub-Category Sales Change in the Last Two Periods"
    )
elif challenge == "wow18wk13":
    st.markdown("""[Challenge source](https://workout-wednesday.com/week-13/): Color and Ordering

Note: The function of Table in plotly is limited. I cannot found any way to merge the column header in level 1.""")
elif challenge == "wow18wk14":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/week-14/): Frequency Matrix"
    )
elif challenge == "wow18wk15":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/week-15/): Total Products by Sub-Category OR Top 5 Sub-Categories by Total Product"
    )
elif challenge == "wow18wk16":
    st.markdown(
        "[Challenge source](https://workout-wednesday.com/week-16/): Sales for the last N vs. same time previous year"
    )


plotly, data = st.tabs(["Chart", "Data"])

with plotly:
    if challenge == "wow18wk01":
        from pages.wow_18 import wk01

        st.plotly_chart(wk01.fig, use_container_width=True)
    elif challenge == "wow18wk02":
        from pages.wow_18 import wk02

        st.markdown("# Fiscal Date Running Sum")
        start_month = st.selectbox(
            label="Fiscal Month Start",
            options=range(1, 13),
            key="start_month",
        )
        fig = wk02.plot_fiscal_data(int(start_month))  # type: ignore
        st.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk03":
        from pages.wow_18 import wk03

        plot_region = st.empty()
        param_date = st.slider(
            label="parametric date",
            min_value=datetime(2014, 1, 1),
            max_value=datetime(2017, 12, 31),
            value=datetime(2016, 6, 1),
            step=timedelta(days=31),
            format="MMM-YY",
            label_visibility="collapsed",
        )
        fig = wk03.get_figure(param_date.replace(day=1))
        plot_region.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk04":
        from pages.wow_18 import wk04

        st.plotly_chart(
            wk04.fig,
            use_container_width=True,
            theme=None,
        )
    elif challenge == "wow18wk05":
        from pages.wow_18 import wk05

        draw, widgets = st.columns([8, 2])
        with widgets:
            years = st.multiselect(
                label="Year",
                options=[2014, 2015, 2016, 2017],
                default=[2014, 2015, 2016, 2017],
                placeholder="Choose years",
                key="years",
            )
            start_month = st.slider(
                label="Starting Month",
                min_value=1,
                max_value=12,
                value=6,
                step=1,
                key="start_month",
            )
        with draw:
            fig = wk05.get_figure(years, start_month)
            st.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk06":
        from pages.wow_18 import wk06

        options = ["Consumer", "Corporate", "Home Office"]
        st.header("Regional Sales Product Hierarchy")
        segment = st.multiselect(
            label="Segment",
            options=options,
            default=options,
            placeholder="Choose a segment",
            key="segment",
        )
        fig = wk06.plot_figure(*segment)
        st.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk07":
        from pages.wow_18 import wk07

        col1, col2 = st.columns([1, 1])
        years = col1.multiselect(
            label="Select Year",
            options=[2014, 2015, 2016, 2017],
            default=[2014, 2015, 2016, 2017],
            placeholder="Choose a year",
            key="years",
        )
        category = col2.multiselect(
            label="Select Category",
            options=["Furniture", "Office Supplies", "Technology"],
            default=["Furniture", "Office Supplies", "Technology"],
            placeholder="Choose a category",
            key="category",
        )
        fig = wk07.get_figure(years, category)
        st.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk08":
        from pages.wow_18 import wk08

        st.markdown(
            '<span style="color:#007C7C; font-size: 48px; font-weight: bold">Is it a trending baby name?</span>',
            unsafe_allow_html=True,
        )
        name = st.text_input(
            "Search for:",
            key="name",
            placeholder="Enter a name",
        )
        if not name:
            welcome = "Hello there! You haven't specified a name, so here is Rody."
        else:
            name_found = wk08.transform_data(name)[0]
            if not name_found:
                welcome = "Sorry that we don't have that name in our records, so here's Rody again."
            else:
                welcome = ""
        st.markdown(
            f'<span style="color:#6C797E">{welcome}</span>', unsafe_allow_html=True
        )
        fig = wk08.get_figure(name)
        st.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk09":
        from pages.wow_18 import wk09

        fig = wk09.get_figure()
        st.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk10":
        from pages.wow_18 import wk10

        fig = wk10.get_figure()
        st.plotly_chart(fig, theme=None)
    elif challenge == "wow18wk11":
        from pages.wow_18 import wk11

        fig = wk11.get_figure()
        st.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk12":
        from pages.wow_18 import wk12

        st.markdown("### Sub-Category Sales Change in the Last Two Periods")
        data18w12 = wk12.load_data()
        current_max_date = st.slider(
            label="Set Max Order Date:",
            min_value=data18w12["Order Date"].min(),
            max_value=data18w12["Order Date"].max(),
            value=datetime(2017, 3, 13),
            key="current_max_date",
        )
        end, start = wk12.get_last_two_periods_format(current_max_date)
        st.markdown(
            f"Orders between <span style='color:#8DBFA8;font-weight:bold'>{start}</span> and <span style='color:#26897E;font-weight:bold'>{end}</span>",
            unsafe_allow_html=True,
        )
        fig = wk12.get_figure(current_max_date)
        st.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk13":
        from pages.wow_18 import wk13

        col1, col2 = st.columns([1, 1])
        year = col1.selectbox(
            label="Year:",
            options=[2014, 2015, 2016, 2017],
            key="year",
        )
        measure = col2.selectbox(
            label="Measure:",
            options=["Sales", "% of Total", "% Diff"],
            key="measure",
        )
        fig = wk13.get_figure(year, measure)
        st.plotly_chart(
            fig, use_container_width=True,
        )
    elif challenge == "wow18wk14":
        from pages.wow_18 import wk14
        fig = wk14.get_figure()
        st.plotly_chart(fig, use_container_width=True, theme=None)
    elif challenge == "wow18wk15":
        from pages.wow_18 import wk15
        fig_intermediate = wk15.get_intermediate_figure()
        fig_jedi = wk15.get_jedi_figure()
        st.markdown("##### Intermediate figure:")
        st.plotly_chart(fig_intermediate, theme=None)
        st.divider()
        st.markdown("##### Jedi figure:")
        st.plotly_chart(fig_jedi, theme=None)
    elif challenge == "wow18wk16":
        from pages.wow_18 import wk16
        if "end_date" not in st.session_state:
            st.session_state["end_date"] = datetime(2017, 6, 28)
        if "period_type" not in st.session_state:
            st.session_state["period_type"] = "Month"
        if "period_numbers" not in st.session_state:
            st.session_state["period_numbers"] = 6
            
        st.markdown("#### Sales For the Last Full "
                    f"{st.session_state['period_numbers']} {st.session_state['period_type']}{'s' if st.session_state['period_numbers']>1 else ''} "
                    "vs. Same Time Previous Year")
        start, end = wk16.get_period(
            st.session_state["end_date"],
            st.session_state["period_type"],
            st.session_state["period_numbers"]
        )
        left, center, right = st.columns([1,3,1])
        center.markdown(f"Sales for: {start.strftime('%B %d, %Y')} - {end.strftime('%B %d, %Y')}")
        col1, col2, col3 = st.columns([1,1,1])
        end_date = col1.slider(
            label="Select End Date:",
            min_value=datetime(2017,1,1),
            max_value=datetime(2017,12,30),
            key="end_date",
        )
        period_type = col2.selectbox(
            label="Select Period Type:",
            options=["Day", "Week", "Month"],
            key="period_type",
        )
        period_numbers = col3.slider(
            label="Select Number of Periods:",
            min_value=1,
            max_value=12,
            key="period_numbers"
        )
        fig = wk16.get_figure(end_date, period_type, period_numbers)
        st.plotly_chart(fig, use_container_width=True)

with data:
    if challenge == "wow18wk01":
        from pages.wow_18 import wk01

        st.dataframe(wk01.data18w01_filtered, use_container_width=True)
    elif challenge == "wow18wk02":
        from pages.wow_18 import wk02

        data = wk02.get_fiscal_data(int(st.session_state["start_month"]))
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk03":
        from pages.wow_18 import wk03

        data = wk03.data18w03_grouped.reset_index().iloc[:, [0, 1, 3]]
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk04":
        from pages.wow_18 import wk04

        st.dataframe(wk04.data18w04_filtered, use_container_width=True)
    elif challenge == "wow18wk05":
        from pages.wow_18 import wk05

        data = wk05.trans_data(
            st.session_state["years"], st.session_state["start_month"]
        )
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk06":
        from pages.wow_18 import wk06

        data = wk06.transform_data(*st.session_state["segment"])
        if len(data):
            data = data.iloc[:, [0, 1, 2, 3]]
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk07":
        from pages.wow_18 import wk07

        data = wk07.transform_data(
            st.session_state["years"], st.session_state["category"]
        )
        data.columns = [
            datetime(year=1900, month=m, day=1).strftime("%B")
            if isinstance(m, int)
            else m
            for m in data.columns
        ]
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk08":
        from pages.wow_18 import wk08

        name_found, data = wk08.transform_data(st.session_state["name"])
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk09":
        from pages.wow_18 import wk09

        data = wk09.load_data()
        st.dataframe(data.iloc[:, [0, 1, 2, 3]], use_container_width=True)
    elif challenge == "wow18wk10":
        from pages.wow_18 import wk10

        data = wk10.transform_data().reset_index()
        st.dataframe(data.iloc[:, [0, 1, 2]], use_container_width=True)
    elif challenge == "wow18wk11":
        from pages.wow_18 import wk11

        data = wk11.transform_data().reset_index()
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk12":
        from pages.wow_18 import wk12

        data = wk12.transform_data(st.session_state["current_max_date"]).reset_index()
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk13":
        from pages.wow_18 import wk13

        data = wk13.transform_data(
            st.session_state["year"], st.session_state["measure"]
        ).reset_index()
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk14":
        from pages.wow_18 import wk14
        data = wk14.calculate_data()
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk15":
        from pages.wow_18 import wk15
        data = wk15.transform_data()
        st.dataframe(data, use_container_width=True)
    elif challenge == "wow18wk16":
        from pages.wow_18 import wk16
        data = wk16.transform_data(
            st.session_state["end_date"],
            st.session_state["period_type"],
            st.session_state["period_numbers"]
        )
        st.dataframe(data, use_container_width=True)

with st.expander("See the complete plotting code"):
    file = f"./pages/wow_18/{challenge[5:]}.py"  # type: ignore
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()
    st.code(code, line_numbers=True)
