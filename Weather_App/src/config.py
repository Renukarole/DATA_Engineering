# src/config.py
import os
from dotenv import load_dotenv
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "weather_capstone")

# Example for Open-Meteo: no api key needed
WEATHER_API_BASE = "https://api.open-meteo.com/v1/forecast"
