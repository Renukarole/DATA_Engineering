# src/utils_db.py
from sqlalchemy import create_engine, text
import pandas as pd
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

def get_engine():
    conn_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(conn_str, pool_size=5, max_overflow=10)
    return engine

def insert_weather_dataframe(df: pd.DataFrame, table_name='weather_readings'):
    engine = get_engine()
    # df columns must match table columns
    df.to_sql(table_name, engine, if_exists='append', index=False, method='multi', chunksize=1000)
