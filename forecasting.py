import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from datetime import datetime
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler

# Load dataset
def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)

    # Debug: Check type before parsing
    print("Before parsing:", df['Date'].dtype)

    # Convert 'Date' column safely
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)  # use utc=True to silence the warning

    # Drop rows where Date couldn't be parsed
    df = df.dropna(subset=['Date'])

    # Debug: Confirm datetime conversion
    print("After parsing:", df['Date'].dtype)
    print("Remaining rows:", len(df))

    df = df.sort_values(by=['Ticker', 'Date'])
    return df



# Analytics: High, Low, Growth
def compute_analytics(df):
    result = []

    for ticker in df['Ticker'].unique():
        sub_df = df[df['Ticker'] == ticker]
        high = sub_df['High'].max()
        low = sub_df['Low'].min()
        open_2020 = sub_df[sub_df['Date'].dt.year == 2020]['Open'].mean()
        close_now = sub_df[sub_df['Date'].dt.year == 2025]['Close'].mean()

        if pd.notnull(open_2020) and pd.notnull(close_now) and open_2020 != 0:
            growth = ((close_now - open_2020) / open_2020) * 100
        else:
            growth = None

        result.append({
            'Ticker': ticker,
            'High': high,
            'Low': low,
            '2020–2025 Growth %': growth
        })

    return pd.DataFrame(result)


def forecast_with_mlp(df, ticker):
    df = df[df['Ticker'] == ticker].copy()
    df = df[['Date', 'Close']].sort_values('Date')
    df['Date'] = pd.to_datetime(df['Date'])

    # Use last 365 days
    recent_df = df.tail(365).copy()

    # Feature Engineering: temporal features
    recent_df['dayofweek'] = recent_df['Date'].dt.dayofweek
    recent_df['month'] = recent_df['Date'].dt.month
    recent_df['quarter'] = recent_df['Date'].dt.quarter
    recent_df['dayofyear'] = recent_df['Date'].dt.dayofyear
    recent_df['weekofyear'] = recent_df['Date'].dt.isocalendar().week.astype(int)

    # Lag and rolling statistics
    recent_df['lag_1'] = recent_df['Close'].shift(1)
    recent_df['lag_2'] = recent_df['Close'].shift(2)
    recent_df['rolling_mean_7'] = recent_df['Close'].rolling(window=7).mean()
    recent_df['rolling_std_7'] = recent_df['Close'].rolling(window=7).std()

    # Drop rows with NaN values created by lag/rolling
    recent_df.dropna(inplace=True)

    # Define features and target
    feature_cols = ['dayofweek', 'month', 'quarter', 'dayofyear', 'weekofyear',
                    'lag_1', 'lag_2', 'rolling_mean_7', 'rolling_std_7']
    X = recent_df[feature_cols].values
    y = recent_df['Close'].values.reshape(-1, 1)

    # Scale features and target
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    X_scaled = scaler_x.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    # Train-test split (last 30 days for testing)
    X_train, X_test = X_scaled[:-30], X_scaled[-30:]
    y_train, y_test = y_scaled[:-30].ravel(), y_scaled[-30:].ravel()

    # Train MLP model
    model = MLPRegressor(hidden_layer_sizes=(128, 64, 32),
                         max_iter=2000,
                         learning_rate='adaptive',
                         early_stopping=True,
                         random_state=42)
    model.fit(X_train, y_train)

    # Predict and inverse scale the output
    y_pred_scaled = model.predict(X_test).reshape(-1, 1)
    y_test_actual = scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten()
    y_pred_actual = scaler_y.inverse_transform(y_pred_scaled).flatten()

    # Compute error
    mse = mean_squared_error(y_test_actual, y_pred_actual)
    rmse = np.sqrt(mse)

    # Prepare forecast DataFrame
    forecast_dates = recent_df['Date'].iloc[-30:].dt.date.values
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'Actual_Close': y_test_actual,
        'Predicted_Close': y_pred_actual
    })

    return forecast_df, mse, rmse


def forecast_january_with_mlp(df, ticker):
    # Filtering the data for the given ticker
    df = df[df['Ticker'] == ticker].copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[['Date', 'Close']].sort_values('Date')

    # Separate training and test sets
    train_df = df[df['Date'] < '2025-01-01'].copy()
    test_df = df[(df['Date'] >= '2025-01-01') & (df['Date'] <= '2025-01-31')].copy()

    # Use last 365 days of training data
    recent_df = train_df.tail(365).copy()

    # Combine with a few days before January 2025 to compute rolling stats
    extended_df = pd.concat([recent_df, test_df.copy()], ignore_index=True)

    # Feature engineering
    extended_df['dayofweek'] = extended_df['Date'].dt.dayofweek
    extended_df['month'] = extended_df['Date'].dt.month
    extended_df['quarter'] = extended_df['Date'].dt.quarter
    extended_df['dayofyear'] = extended_df['Date'].dt.dayofyear
    extended_df['weekofyear'] = extended_df['Date'].dt.isocalendar().week.astype(int)

    extended_df['lag_1'] = extended_df['Close'].shift(1)
    extended_df['lag_2'] = extended_df['Close'].shift(2)
    extended_df['rolling_mean_7'] = extended_df['Close'].rolling(window=7).mean()
    extended_df['rolling_std_7'] = extended_df['Close'].rolling(window=7).std()

    # Drop rows with NaNs
    extended_df.dropna(inplace=True)

    # Split again: training features and target
    train_features = extended_df[extended_df['Date'] < '2025-01-01']
    test_features = extended_df[extended_df['Date'].between('2025-01-01', '2025-01-31')]

    feature_cols = ['dayofweek', 'month', 'quarter', 'dayofyear', 'weekofyear',
                    'lag_1', 'lag_2', 'rolling_mean_7', 'rolling_std_7']
    
    X_train = train_features[feature_cols].values
    y_train = train_features['Close'].values.reshape(-1, 1)

    X_test = test_features[feature_cols].values
    y_test = test_features['Close'].values.reshape(-1, 1)

    # Scale features and target
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    X_train_scaled = scaler_x.fit_transform(X_train)
    y_train_scaled = scaler_y.fit_transform(y_train)

    X_test_scaled = scaler_x.transform(X_test)

    # Train MLP model
    model = MLPRegressor(hidden_layer_sizes=(128, 64, 32),
                         max_iter=2000,
                         learning_rate='adaptive',
                         early_stopping=True,
                         random_state=42)
    model.fit(X_train_scaled, y_train_scaled.ravel())

    # Predict and inverse scale
    y_pred_scaled = model.predict(X_test_scaled).reshape(-1, 1)
    y_pred_actual = scaler_y.inverse_transform(y_pred_scaled).flatten()
    y_test_actual = y_test.flatten()

    # Compute error
    mse = mean_squared_error(y_test_actual, y_pred_actual)
    rmse = np.sqrt(mse)

    # Prepare result DataFrame
    forecast_df = pd.DataFrame({
        'Date': test_features['Date'].dt.date.values,
        'Actual_Close': y_test_actual,
        'Predicted_Close': y_pred_actual
    })

    return forecast_df, mse, rmse
