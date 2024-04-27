import streamlit as st
import menu
import assets

menu.side_navigation()

options = {"wow18wk01": "Week 01: Looks vs. Personality"}

challenge = st.selectbox(
    "Please select the challenge of the year 2018: ",
    options=options.keys(),
    format_func=lambda idx: options[idx],
    placeholder="Choose a challenge",
)

if challenge == "wow18wk01":
    st.markdown("[Challenge source](https://www.vizwiz.com/2018/01/ww-looks-vs-personality.html): Workout Wednesday: Looks vs. Personality")

plotly, data = st.tabs(["Chart by Plotly", "Data"])

with plotly:
    if challenge == "wow18wk01":
        from pages.wow_18 import wk01
        st.plotly_chart(wk01.fig)

with data:
    if challenge == "wow18wk01":
        from pages.wow_18 import wk01
        st.dataframe(wk01.data18w01_filtered, use_container_width=True)

with st.expander("See the complete plotting code"):
    if challenge == "wow18wk01":
        with open("./pages/wow_18/wk01.py", "r", encoding="utf-8") as f:
            code = f.read()
        st.code(code, line_numbers=True)
