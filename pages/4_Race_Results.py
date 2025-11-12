import streamlit as st
import fastf1
import pandas as pd
from datetime import datetime
from utils import local_css
local_css("styles.css")

st.title("F1 Race Results Viewer")


year = st.slider("Select Year", 2020, 2025, 2024)


races = fastf1.get_event_schedule(year)


today = datetime.now()
races = races[
    (races["EventFormat"].isin(["conventional", "sprint"])) &
    (~races["EventName"].str.contains("Test", case=False, na=False)) &
    (pd.to_datetime(races["EventDate"]) <= today)
]


race_names = races['EventName'].tolist()
if not race_names:
    st.warning(f"No races have occurred yet in {year}.")
else:
    selected_race = st.selectbox("Select Race", race_names)

    with st.spinner("Loading race results..."):
        try:
            session = fastf1.get_session(year, selected_race, 'R')
            session.load()

            
            results = session.results[['DriverNumber', 'Abbreviation', 'TeamName', 'Position', 'Points']]

            st.success(f"Results loaded for {selected_race} ({year})")

            
            st.dataframe(
                results,
                height=420,        
                hide_index=True     
            )

            
            st.markdown(
                "<style>.stDataFrame {width: 100% !important;}</style>",
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Error loading race data: {e}")
