-- create DB (run as postgres or a superuser)
CREATE DATABASE weather_capstone;

-- Connect to weather_capstone and create tables (run inside that DB)
-- Table to store hourly/daily records
CREATE TABLE IF NOT EXISTS weather_readings (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    observed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    temperature_c DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    pressure_hpa DOUBLE PRECISION,
    windspeed_ms DOUBLE PRECISION,
    weather_code INTEGER,
    source TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- Add index for queries by city and date
CREATE INDEX IF NOT EXISTS idx_weather_city_time ON weather_readings (city, observed_at);
