import calendar
import numpy as np
import pandas as pd
from datetime import date
from flight_data import FlightData
from sklearn.base import BaseEstimator, TransformerMixin


class CosineEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, max_val):
        self.max_val = max_val

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_rad = X / self.max_val * 2 * np.pi
        return np.cos(X_rad)


def preprocess(flight_data: FlightData) -> np.ndarray:
  days_in_month = {k: calendar.monthrange(flight_data.year, k)[1] for k in range(1, 13)}
  df = pd.DataFrame([flight_data.model_dump()])
  df['scaled_day'] = df.day.map(lambda d: d / days_in_month[flight_data.month])
  df['weekday'] = date(flight_data.year, flight_data.month, flight_data.day).weekday() + 2
  df['carrier'] = df['carrier'].str.upper()
  del df['year']
  return df
