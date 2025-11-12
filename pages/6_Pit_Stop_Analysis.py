import streamlit as st
import pandas as pd
import plotly.express as px
from f1_data import load_race_data
from utils import local_css
local_css("styles.css")

st.title("Pit Stop Analysis")

year = st.slider("Select Year", 2020, 2025, 2024)
gp = st.text_input("Enter Grand Prix name", "Bahrain")

session = load_race_data(year, gp)
if not session:
    st.error("Could not load race session.")
else:
    pit_stops = session.laps[session.laps['PitOutTime'].notna() | session.laps['PitInTime'].notna()]
    if pit_stops.empty:
        st.warning("No pit stop data found.")
    else:
        st.subheader(f"Pit Stop Data — {year} {gp} GP")

        pit_df = pit_stops.groupby("Driver").size().reset_index(name="PitStops")
        fig = px.bar(pit_df, x="Driver", y="PitStops", color="PitStops",
                     title="Number of Pit Stops per Driver")
        st.plotly_chart(fig, use_container_width=True)

        st.write("### Detailed Pit Stop Laps")
        st.dataframe(pit_stops[["Driver", "LapNumber", "PitInTime", "PitOutTime"]].reset_index(drop=True))
