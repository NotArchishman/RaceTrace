import streamlit as st
import plotly.express as px
from f1_data import load_race_data, get_lap_data

from utils import local_css
local_css("styles.css")

st.title("Race Overview")

year = st.slider("Select Year", 2020, 2025, 2024)
gp = st.text_input("Enter Grand Prix name (e.g. 'Bahrain', 'Monza')", "Bahrain")

session = load_race_data(year, gp)
if session:
    st.subheader(f"{year} {gp} Grand Prix")
    st.write(f"Track: {session.event['EventName']}")
    st.write(f"Session Date: {session.event['EventDate']}")

    laps = get_lap_data(session)
    if not laps.empty:
        avg_lap = laps.groupby("Driver")["LapTimeSeconds"].mean().reset_index()
        fig = px.bar(avg_lap, x="Driver", y="LapTimeSeconds", title="Average Lap Times by Driver")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No lap data found for this race.")
else:
    st.error("Could not load race data.")
