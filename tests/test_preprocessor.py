import numpy as np
from flight_data import FlightData
from preprocessor import preprocess, CosineEncoder

def test_cosine_encoder():
  encoder = CosineEncoder(max_val=12)
  result = encoder.fit_transform(np.arange(1, 13))
  result[-1] == 1.0

def test_preprocess():
  f = FlightData(day=31, month=1, hour=0, year=2013, carrier="AA", distance=1, wind_spd=0)
  df = preprocess(f)
  assert df['scaled_day'][0] == 1.0

def test_preprocess_scaled_day():
  f = FlightData(day=31, month=1, hour=0, year=2013, carrier="AA", distance=1, wind_spd=0)
  df = preprocess(f)
  assert df['scaled_day'][0] == 1.0

def test_preprocess_weekday():
  f = FlightData(day=10, month=12, hour=0, year=2024, carrier="AA", distance=1, wind_spd=0)
  df = preprocess(f)
  assert df['weekday'][0] == 3

def test_preprocess_carrier():
  f = FlightData(day=10, month=12, hour=0, year=2024, carrier="aa", distance=1, wind_spd=0)
  df = preprocess(f)
  assert df['carrier'][0] == 'AA'