import streamlit as st

def side_navigation():
    st.sidebar.page_link("app.py", label=":house: Home")
    st.sidebar.page_link("pages/wow18.py", label=":bar_chart: WOW 2018")