import streamlit as st
import plotly.graph_objects as go
from f1_data import load_race_data, get_lap_data
from utils import local_css
local_css("styles.css")

st.title("Driver Comparison")

year = st.slider("Select Year", 2020, 2025, 2024)
gp = st.text_input("Enter Grand Prix name", "Monza")
session = load_race_data(year, gp)

if session:
    laps = get_lap_data(session)
    drivers = sorted(laps['Driver'].unique())
    driver1 = st.selectbox("Select First Driver", drivers)
    driver2 = st.selectbox("Select Second Driver", drivers)

    d1 = laps[laps['Driver'] == driver1]
    d2 = laps[laps['Driver'] == driver2]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d1['LapNumber'], y=d1['LapTimeSeconds'], mode='lines', name=driver1))
    fig.add_trace(go.Scatter(x=d2['LapNumber'], y=d2['LapTimeSeconds'], mode='lines', name=driver2))

    fig.update_layout(title=f"Lap Time Comparison: {driver1} vs {driver2}",
                      xaxis_title="Lap Number",
                      yaxis_title="Lap Time (s)")
    st.plotly_chart(fig, use_container_width=True)
