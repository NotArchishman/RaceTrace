import streamlit as st
import fastf1
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import difflib
from utils import local_css
local_css("styles.css")


TEAM_COLORS = {
    'Red Bull Racing': '#1E41FF',
    'Ferrari': '#DC0000',
    'Mercedes': '#00D2BE',
    'McLaren': '#FF8700',
    'Aston Martin': '#006F62',
    'Alpine': '#0090FF',
    'Williams': '#005AFF',
    'RB': '#6692FF',           
    'Haas F1 Team': '#B6BABD',
    'Sauber': '#52E252',       
    'AlphaTauri': '#2B4562',
    'Alfa Romeo': '#900000'
}


st.set_page_config(page_title="F1 Circular Race Replay", layout="wide")
st.title("🏁 F1 Circular Race Replay")


st.sidebar.header("🏆 Race Selection")
year = st.sidebar.selectbox("Select Year", list(range(2020, 2025))[::-1], index=1)


schedule = fastf1.get_event_schedule(year)
race_events = schedule[schedule['EventFormat'] == 'conventional'][['RoundNumber', 'EventName']]

if race_events.empty:
    st.warning("No race data found for this year yet.")
    st.stop()


race_name = st.sidebar.selectbox("Select Race", race_events['EventName'].tolist())


matched = difflib.get_close_matches(race_name, race_events['EventName'].tolist(), n=1)
if not matched:
    st.error("Could not find this race in the schedule.")
    st.stop()

race_name_matched = matched[0]
round_number = int(race_events.loc[race_events['EventName'] == race_name_matched, 'RoundNumber'])

st.success(f"Loaded {race_name_matched} ({year}) successfully!")


try:
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
except Exception as e:
    st.error(f"Error loading session: {e}")
    st.stop()


drivers = session.drivers
laps = session.laps

if laps.empty:
    st.warning("No lap data available for this race.")
    st.stop()

num_drivers = len(drivers)
base_angles = np.linspace(0, 2 * np.pi, num_drivers, endpoint=False)
driver_angles = {drv: ang for drv, ang in zip(drivers, base_angles)}


lap_data = []
for drv in drivers:
    drv_laps = laps.pick_drivers(drv)
    total_laps = len(drv_laps)
    if total_laps == 0:
        continue
    for i, lap in enumerate(drv_laps.itertuples(), 1):
        progress = i / total_laps
        lap_data.append((drv, i, progress))

lap_df = pd.DataFrame(lap_data, columns=["Driver", "LapNumber", "Progress"])

fastest = laps.pick_fastest()
fastest_driver = fastest["Driver"]


if "running" not in st.session_state:
    st.session_state.running = False
if "lap" not in st.session_state:
    st.session_state.lap = 1


col1, col2 = st.columns([1, 3])
with col1:
    if st.button("🎬 Start Replay"):
        st.session_state.running = True
with col2:
    auto_play = st.checkbox("▶ Auto-play animation", value=False)

lap_slider = st.slider(
    "🟢 Lap Number",
    1,
    int(laps["LapNumber"].max()),
    st.session_state.lap,
    key="lap_slider",
)


def get_positions(lap_num):
    df_display = lap_df[lap_df["LapNumber"] <= lap_num].groupby("Driver").last().reset_index()
    df_display["Angle"] = df_display["Driver"].map(driver_angles)
    df_display["Angle"] = df_display["Angle"] + df_display["Progress"] * 2 * np.pi
    df_display["x"] = np.cos(df_display["Angle"])
    df_display["y"] = np.sin(df_display["Angle"])
    df_display["Team"] = [session.get_driver(d)["TeamName"] for d in df_display["Driver"]]
    df_display["Color"] = [TEAM_COLORS.get(team, "#999999") for team in df_display["Team"]]
    return df_display


def make_plot(df_display, lap_num):
    fig = go.Figure()

    for drv in df_display["Driver"]:
        drv_data = lap_df[lap_df["Driver"] == drv].tail(5)
        drv_data["Angle"] = driver_angles[drv] + drv_data["Progress"] * 2 * np.pi
        drv_data["x"] = np.cos(drv_data["Angle"])
        drv_data["y"] = np.sin(drv_data["Angle"])
        team = session.get_driver(drv)["TeamName"]
        color = TEAM_COLORS.get(team, "#999999")

        fig.add_trace(go.Scatter(
            x=drv_data["x"], y=drv_data["y"],
            mode="lines", line=dict(color=color, width=2),
            showlegend=False
        ))

    for _, row in df_display.iterrows():
        size = 18 if row["Driver"] == fastest_driver else 12
        fig.add_trace(go.Scatter(
            x=[row["x"]], y=[row["y"]],
            mode="markers+text",
            text=row["Driver"],
            textposition="top center",
            marker=dict(color=row["Color"], size=size, line=dict(color="white", width=1)),
            name=row["Driver"]
        ))

    fig.update_layout(
        title=f"{race_name_matched} {year} – Lap {lap_num} Replay",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        showlegend=False, width=700, height=700,
        plot_bgcolor="black", paper_bgcolor="black",
        title_font=dict(color="white", size=22)
    )
    fig.update_traces(textfont=dict(color="white"))
    return fig



placeholder = st.empty()

def render_plot(lap_num):
    df_display = get_positions(lap_num)
    fig = make_plot(df_display, lap_num)
    placeholder.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


if st.session_state.running and auto_play:
    for lap_num in range(st.session_state.lap, int(laps["LapNumber"].max()) + 1):
        st.session_state.lap = lap_num
        render_plot(lap_num)
        time.sleep(0.4)
    st.session_state.running = False
else:
    render_plot(st.session_state.lap)
