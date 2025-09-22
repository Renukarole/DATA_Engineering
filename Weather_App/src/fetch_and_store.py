# src/fetch_and_store.py
import requests
import pandas as pd
from datetime import datetime, timedelta
from utils_db import insert_weather_dataframe
from config import WEATHER_API_BASE

# A small city->lat/lon map. Add more as needed.
CITY_COORDS = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Bengaluru": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707)
}

def fetch_last_30_days(lat, lon):
    end = datetime.utcnow().date()
    start = end - timedelta(days=30)
    # Open-Meteo daily/hourly API for historical: hourly variables can include temperature_2m,etc
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "hourly": "temperature_2m,relativehumidity_2m,pressure_msl,windspeed_10m,weathercode",
        "timezone": "UTC"
    }
    r = requests.get(WEATHER_API_BASE, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def transform_to_df(json_resp, city, lat, lon):
    hourly = json_resp.get("hourly", {})
    times = hourly.get("time", [])
    if not times:
        return pd.DataFrame()
    df = pd.DataFrame({
        "observed_at": pd.to_datetime(times),
        "temperature_c": hourly.get("temperature_2m"),
        "humidity": hourly.get("relativehumidity_2m"),
        "pressure_hpa": hourly.get("pressure_msl"),
        "windspeed_ms": hourly.get("windspeed_10m"),
        "weather_code": hourly.get("weathercode")
    })
    df["city"] = city
    df["latitude"] = lat
    df["longitude"] = lon
    df["source"] = "open-meteo"
    # reorder
    df = df[["city","latitude","longitude","observed_at","temperature_c","humidity","pressure_hpa","windspeed_ms","weather_code","source"]]
    return df

def fetch_and_store_for_city(city):
    if city not in CITY_COORDS:
        raise ValueError("Unknown city, add to CITY_COORDS or use geocoding.")
    lat, lon = CITY_COORDS[city]
    j = fetch_last_30_days(lat, lon)
    df = transform_to_df(j, city, lat, lon)
    if df.empty:
        print("No data returned.")
        return
    insert_weather_dataframe(df)
    print(f"Inserted {len(df)} rows for {city}")

if __name__ == "__main__":
    # Example: fetch for one city. For multiple cities call multiple times (cron or scheduler)
    fetch_and_store_for_city("Mumbai")
