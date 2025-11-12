import fastf1
import pandas as pd
from functools import lru_cache


fastf1.Cache.enable_cache("cache")

@lru_cache(maxsize=10)
def load_race_data(year=2024, gp='Bahrain'):
   
    try:
        session = fastf1.get_session(year, gp, 'R')
        session.load()
        return session
    except Exception as e:
        print(f"Error loading session: {e}")
        return None

def get_lap_data(session):
    if not session:
        return pd.DataFrame()
    laps = session.laps
    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
    return laps
