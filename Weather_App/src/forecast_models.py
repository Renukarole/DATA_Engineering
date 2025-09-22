# src/forecast_models.py
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from utils_db import get_engine
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def load_temp_series(city):
    engine = get_engine()
    end = datetime.utcnow()
    start = end - timedelta(days=30)
    q = """
    SELECT observed_at AT TIME ZONE 'UTC' as observed_at, temperature_c
    FROM weather_readings
    WHERE city = :city AND observed_at BETWEEN :start AND :end
    ORDER BY observed_at
    """
    df = pd.read_sql_query(q, engine, params={"city": city, "start": start, "end": end})
    df['observed_at'] = pd.to_datetime(df['observed_at'])
    df.set_index('observed_at', inplace=True)
    df = df.resample('H').mean().interpolate()  # ensure uniform hourly series
    return df['temperature_c']

def sarimax_forecast(series, steps=24):
    # Train/test split (last 24 hours as test)
    train = series[:-24]
    test = series[-24:]
    # Simple SARIMAX parameters (p,d,q) tuned for example; adjust in practice
    model = SARIMAX(train, order=(2,0,1), seasonal_order=(1,1,1,24), enforce_stationarity=False, enforce_invertibility=False)
    res = model.fit(disp=False)
    pred = res.get_forecast(steps=24)
    y_pred = pred.predicted_mean
    mse = mean_squared_error(test, y_pred)
    print("SARIMAX MSE:", mse)
    # plot
    plt.figure(figsize=(12,4))
    plt.plot(train.index[-48:], train[-48:], label='train (last 48h)')
    plt.plot(test.index, test, label='actual')
    plt.plot(y_pred.index, y_pred, label='predicted')
    plt.legend()
    plt.title("SARIMAX Forecast (next 24h)")
    plt.savefig("report/sarimax_forecast.png")
    plt.show()
    return res, y_pred

# Optional: simple LSTM example (requires tensorflow)
def lstm_forecast(series, steps=24, epochs=20):
    import numpy as np
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense
    from sklearn.preprocessing import MinMaxScaler

    data = series.values.reshape(-1,1)
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # create sequences
    seq_len = 24
    X, y = [], []
    for i in range(len(data_scaled)-seq_len-steps+1):
        X.append(data_scaled[i:i+seq_len])
        y.append(data_scaled[i+seq_len:i+seq_len+steps, 0])  # multi-step
    X = np.array(X)
    y = np.array(y)

    # train/test split
    split = int(0.9*len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = Sequential()
    model.add(LSTM(64, input_shape=(seq_len,1)))
    model.add(Dense(steps))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=16)

    # predict next steps using last seq
    last_seq = data_scaled[-seq_len:].reshape(1, seq_len, 1)
    pred_scaled = model.predict(last_seq)
    pred = scaler.inverse_transform(pred_scaled.reshape(-1,1)).flatten()
    print("LSTM predicted next temps:", pred[:steps])
    return pred

if __name__ == "__main__":
    city = "Mumbai"
    series = load_temp_series(city)
    if series.empty:
        print("No data found. Run fetch_and_store first.")
    else:
        res, y_pred = sarimax_forecast(series)
        # optionally run LSTM
        # preds = lstm_forecast(series, steps=24, epochs=15)
