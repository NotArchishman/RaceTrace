import streamlit as st
import plotly.express as px
from f1_data import load_race_data, get_lap_data
from utils import local_css
local_css("styles.css")

st.title("Lap Time Trends")

year = st.slider("Select Year", 2020, 2025, 2024)
gp = st.text_input("Enter Grand Prix name", "Silverstone")

session = load_race_data(year, gp)
if session:
    laps = get_lap_data(session)
    driver = st.selectbox("Select Driver", sorted(laps['Driver'].unique()))
    driver_laps = laps[laps['Driver'] == driver]

    fig = px.line(driver_laps, x="LapNumber", y="LapTimeSeconds", title=f"{driver} Lap Times Over Race")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Unable to load race data.")
