# workspace/train_and_log.py

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

try:
    from autogluon.tabular import TabularPredictor
    use_autogluon = True
except Exception:
    use_autogluon = False

# MLflow
import mlflow

MLFLOW_URI = os.environ.get('MLFLOW_TRACKING_URI', 'http://localhost:5000')
mlflow.set_tracking_uri(MLFLOW_URI)

def generate_time_series(days=200):
    rng = pd.date_range(end=datetime.now(), periods=days, freq='D')
    trend = np.linspace(0, 10, days)
    seasonal = 2 * np.sin(np.linspace(0, 3 * np.pi, days))
    noise = np.random.normal(scale=0.8, size=days)
    series = trend + seasonal + noise
    df = pd.DataFrame({
        'date': rng,
        'value': series
    })
    # add lag features
    for lag in range(1, 8):
        df[f'lag_{lag}'] = df['value'].shift(lag)
    df = df.dropna().reset_index(drop=True)
    return df


def train_and_log():
    df = generate_time_series()
    # create a supervised learning problem: predict next-day value
    df['target'] = df['value'].shift(-1)
    df = df.dropna().reset_index(drop=True)
    X = df.drop(['date', 'target'], axis=1)
    y = df['target']
    # split
    split = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    with mlflow.start_run(run_name='time_series_demo'):
        if use_autogluon:
            print('Using AutoGluon for modeling (if installed)')
            predictor = TabularPredictor(label='target', path='ag_models').fit(pd.concat([X_train, y_train], axis=1))
            preds = predictor.predict(X_test)
            # save model - AutoGluon has its own save, but we save path as artifact
            predictor.save('ag_models')
            mlflow.log_artifact('ag_models')
        else:
            print('AutoGluon not available, using simple sklearn linear model')
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            # save sklearn model
            import joblib
            joblib.dump(model, 'linear_model.joblib')
            mlflow.log_artifact('linear_model.joblib')

        # metrics
        from sklearn.metrics import mean_squared_error
        mse = mean_squared_error(y_test, preds)
        mlflow.log_metric('mse', float(mse))
        print('Logged run to MLflow at', MLFLOW_URI)

if __name__ == '__main__':
    train_and_log()
