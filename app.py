import streamlit as st
import menu

st.write("""
# Workout Wednesday Challenge with Python

[Workout Wednesday (WOW)](https://workout-wednesday.com/) is an excellent challenge 
to familiarize myself with the plotting library such as plotly, bokeh, matplotlib, etc. 

This webapp is a collection of my practice of WOW challenge with python. 
For the first version, I mainly re-create the WOW challenge by plotly, which is
flexible enough to customize the drawing according to the WOW challenge, creating
a chart as similar as possible to that in the WOW challenge.

In the future, I will reimplement the challenge with bokeh and matplotlib. But 
for now, let's dive into the [challenge for Tableau](https://workout-wednesday.com/challenge-insights/) 
with plotly!
""")

menu.side_navigation()