import streamlit as st
from f1_data import load_race_data
import pandas as pd
from pathlib import Path
import fastf1


from utils import local_css
local_css("styles.css")


st.set_page_config(
    page_title="F1 Live Dashboard",
    layout="wide",
)

st.title("Formula 1 RaceTrace")
st.write("Welcome to RaceTrace! Use the sidebar to explore race analytics, driver comparisons, and circuit insights.")



load_race_data()
st.success("FastF1 cache initialized successfully.")


