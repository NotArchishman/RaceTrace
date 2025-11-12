import streamlit as st
import fastf1
import matplotlib.pyplot as plt
from utils import local_css
local_css("styles.css")

st.title("⏱️ Fastest Lap Comparison")


year = st.number_input("Select Year", min_value=2020, max_value=2025, value=2024)

with st.spinner("Loading race list..."):
    try:
        schedule = fastf1.get_event_schedule(year)
        races = schedule.loc[schedule["EventFormat"] == "conventional", "EventName"].tolist()
    except Exception as e:
        st.error(f"Error loading races for {year}: {e}")
        races = []

if races:
    selected_race = st.selectbox("Select Race", races)
else:
    st.stop()

driver1 = st.text_input("Driver 1 Abbreviation", "VER")
driver2 = st.text_input("Driver 2 Abbreviation", "HAM")

if st.button("Compare Fastest Laps"):
    with st.spinner(f"Loading data for {selected_race} {year}..."):
        try:
            session = fastf1.get_session(year, selected_race, 'R')
            session.load()

            lap1 = session.laps.pick_drivers(driver1).pick_fastest()
            lap2 = session.laps.pick_drivers(driver2).pick_fastest()

            tel1 = lap1.get_telemetry()
            tel2 = lap2.get_telemetry()

            fig, ax = plt.subplots()
            ax.plot(tel1['Distance'], tel1['Speed'], label=f"{driver1} - {lap1['LapTime']}")
            ax.plot(tel2['Distance'], tel2['Speed'], label=f"{driver2} - {lap2['LapTime']}")
            ax.set_xlabel("Distance (m)")
            ax.set_ylabel("Speed (km/h)")
            ax.set_title(f"Fastest Lap Comparison - {selected_race} {year}")
            ax.legend()

            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {e}")
