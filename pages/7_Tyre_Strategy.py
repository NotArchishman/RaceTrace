import streamlit as st
import pandas as pd
import plotly.express as px
from f1_data import load_race_data, get_lap_data
from utils import local_css
local_css("styles.css")

st.title("Tyre Strategy Breakdown")

year = st.slider("Select Year", 2020, 2025, 2024)
gp = st.text_input("Enter Grand Prix name", "Silverstone")

session = load_race_data(year, gp)
if session:
    laps = get_lap_data(session)
    if "Compound" not in laps.columns:
        st.warning("Tyre compound data not available for this session.")
    else:
        st.subheader(f"{year} {gp} GP — Tyre Usage by Driver")

        tyre_counts = laps.groupby(["Driver", "Compound"]).size().reset_index(name="LapsOnTyre")

        fig = px.bar(
            tyre_counts,
            x="Driver",
            y="LapsOnTyre",
            color="Compound",
            title="Tyre Compound Usage per Driver",
            text="LapsOnTyre",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        st.write("### Detailed Tyre Data")
        st.dataframe(laps[["Driver", "LapNumber", "Compound", "LapTimeSeconds"]])
else:
    st.error("Could not load session data.")
