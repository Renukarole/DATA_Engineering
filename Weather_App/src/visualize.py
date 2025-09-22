# src/visualize.py
import pandas as pd
import matplotlib.pyplot as plt
from utils_db import get_engine
from datetime import datetime, timedelta

def load_city_last_30_days(city, engine=None):
    if engine is None:
        engine = get_engine()
    end = datetime.utcnow()
    start = end - timedelta(days=30)
    q = f"""
        SELECT observed_at AT TIME ZONE 'UTC' as observed_at, temperature_c, humidity, pressure_hpa, windspeed_ms
        FROM weather_readings
        WHERE city = :city
          AND observed_at BETWEEN :start AND :end
        ORDER BY observed_at
    """
    df = pd.read_sql_query(q, engine, params={"city": city, "start": start, "end": end})
    if not df.empty:
        df['observed_at'] = pd.to_datetime(df['observed_at'])
        df.set_index('observed_at', inplace=True)
    return df

def plot_temperature(df, city):
    plt.figure(figsize=(14,5))
    plt.plot(df.index, df['temperature_c'])
    plt.title(f"{city} — Temperature (last 30 days)")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"report/{city}_temperature_last30.png")
    plt.show()

def plot_multi(df, city):
    plt.figure(figsize=(14,6))
    df[['temperature_c','humidity']].plot(subplots=True, layout=(2,1), figsize=(14,8))
    plt.suptitle(f"{city} — Temp & Humidity (last 30 days)")
    plt.savefig(f"report/{city}_temp_humidity_last30.png")
    plt.show()

if __name__ == "__main__":
    city = "Mumbai"
    df = load_city_last_30_days(city)
    if df.empty:
        print("No data found. Run fetch_and_store first.")
    else:
        plot_temperature(df, city)
        plot_multi(df, city)
