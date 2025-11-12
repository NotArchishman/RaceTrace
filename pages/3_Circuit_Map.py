import fastf1
import streamlit as st
import plotly.express as px
import pandas as pd

from utils import local_css
local_css("styles.css")


st.title("Circuit Map")

year = st.slider("Select Year", 2020, 2025, 2024)
gp_name = st.text_input("Enter Grand Prix name", "Monaco")

try:
    
    session = fastf1.get_session(year, gp_name, "R")
    session.load()

    
    driver = None
    for drv in session.drivers:
        drv_laps = session.laps.pick_drivers(drv)  
        if not drv_laps.empty:
            lap = drv_laps.pick_fastest()
            telemetry = lap.get_telemetry()
            if {"X", "Y"}.issubset(telemetry.columns):
                driver = drv
                break

    if driver is None:
        st.warning("Telemetry data missing coordinate info for this session.")
    else:
        fig = px.line(
            telemetry,
            x="X",
            y="Y",
            title=f"{gp_name} {year} - Circuit Map ({driver})",
        )
        fig.update_yaxes(scaleanchor="x", scaleratio=1)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading circuit info: {e}")
