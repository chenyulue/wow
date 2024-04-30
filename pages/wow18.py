import streamlit as st
import menu
import assets

menu.side_navigation()

options = {
    "wow18wk01": "Week 01: Looks vs. Personality",
    "wow18wk02": "Week 02: Year to Fiscal Date Running Totals",
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

plotly, data = st.tabs(["Chart by Plotly", "Data"])

with plotly:
    if challenge == "wow18wk01":
        from pages.wow_18 import wk01
        st.plotly_chart(wk01.fig)
    elif challenge == "wow18wk02":
        from pages.wow_18 import wk02
        st.markdown("# Fiscal Date Running Sum")
        start_month = st.selectbox(
            label="Fiscal Month Start",
            options=range(1, 13),
            key="start_month",
        )
        fig = wk02.plot_fiscal_data(int(start_month))
        st.plotly_chart(fig,)

with data:
    if challenge == "wow18wk01":
        from pages.wow_18 import wk01
        st.dataframe(wk01.data18w01_filtered, use_container_width=True)
    elif challenge == "wow18wk02":
        from pages.wow_18 import wk02
        data = wk02.get_fiscal_data(int(st.session_state["start_month"]))
        st.dataframe(data, use_container_width=True)

with st.expander("See the complete plotting code"):
    if challenge == "wow18wk01":
        with open("./pages/wow_18/wk01.py", "r", encoding="utf-8") as f:
            code = f.read()
        st.code(code, line_numbers=True)
    elif challenge == "wow18wk02":
        with open("./pages/wow_18/wk02.py", "r", encoding="utf-8") as f:
            code = f.read()
        st.code(code, line_numbers=True)
