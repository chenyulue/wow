import streamlit as st
import menu

st.write("""
# Workout Wednesday Challenge with Python

[Workout Wednesday (WOW)](https://workout-wednesday.com/) is an excellent challenge 
to familiarize myself with the plotting library such as plotly, bokeh, matplotlib, etc. 

This webapp is a collection of my practice of WOW challenge with python. 
I mainly re-create the WOW challenge by plotly, which is
flexible enough to customize the drawing according to the WOW challenge, creating
a chart as similar as possible to that in the WOW challenge.

However, I will also recreate the datavis by other packages, such as bokeh, altair, 
matplotlib, etc. Let's dive into the [challenge for Tableau](https://workout-wednesday.com/challenge-insights/) 
with python!
""")

menu.side_navigation()