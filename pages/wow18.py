import streamlit as st
from datetime import datetime, timedelta
import menu

menu.side_navigation()

options = {
    "wow18wk01": "Week 01: Looks vs. Personality",
    "wow18wk02": "Week 02: Year to Fiscal Date Running Totals",
    "wow18wk03": "Week 03: Rolling three month sales",
    "wow18wk04": "Week 04: Tables"
}

challenge = st.selectbox(
    "Please select the challenge of the year 2018: ",
    options=options.keys(),
    format_func=lambda idx: options[idx],
    placeholder="Choose a challenge",
)

if challenge == "wow18wk01":
    st.markdown("[Challenge source](https://www.vizwiz.com/2018/01/ww-looks-vs-personality.html): Workout Wednesday: Looks vs. Personality")
elif challenge == "wow18wk02":
    st.markdown("[Challenge source](https://workout-wednesday.com/workout-wednesday-2018-week-2-year-to-fiscal-date-running-totals/): Workout Wednesday: Year to Fiscal Date Running Totals")
elif challenge == "wow18wk03":
    st.markdown("[Challenge source](https://workout-wednesday.com/week3/): Workout Wednesday: Rolling three month sales")
elif challenge == "wow18wk04":
    st.markdown("[Challenge source](https://workout-wednesday.com/workoutwednesday-week4/): Workout Wednesday: Tables")


plotly, data = st.tabs(["Chart", "Data"])

with plotly:
    if challenge == "wow18wk01":
        from pages.wow_18 import wk01
        st.plotly_chart(wk01.fig,)
    elif challenge == "wow18wk02":
        from pages.wow_18 import wk02
        st.markdown("# Fiscal Date Running Sum")
        start_month = st.selectbox(
            label="Fiscal Month Start",
            options=range(1, 13),
            key="start_month",
        )
        fig = wk02.plot_fiscal_data(int(start_month)) # type: ignore
        st.plotly_chart(fig,)
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
            label_visibility="collapsed"
        )
        fig = wk03.get_figure(param_date.replace(day=1))
        plot_region.plotly_chart(fig, use_container_width=True)
    elif challenge == "wow18wk04":
        from pages.wow_18 import wk04
        st.plotly_chart(wk04.fig, use_container_width=True, theme=None,)

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

with st.expander("See the complete plotting code"):
    file = f"./pages/wow_18/{challenge[5:]}.py" # type: ignore
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()
    st.code(code, line_numbers=True)
    # if challenge == "wow18wk01":
    #     with open("./pages/wow_18/wk01.py", "r", encoding="utf-8") as f:
    #         code = f.read()
    #     st.code(code, line_numbers=True)
    # elif challenge == "wow18wk02":
    #     with open("./pages/wow_18/wk02.py", "r", encoding="utf-8") as f:
    #         code = f.read()
    #     st.code(code, line_numbers=True)
    # elif challenge == "wow18wk03":
    #     with open("./pages/wow_18/wk03.py", "r", encoding="utf-8") as f:
    #         code = f.read()
    #     st.code(code, line_numbers=True)
