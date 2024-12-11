import pytest
from flight_data import FlightData
from pydantic_core import ValidationError

def test_bad_day():
  with pytest.raises(ValidationError):
    FlightData(day=0, month=1, year=2000, hour=1, carrier="AA", distance=1, wind_spd=1)
    

def test_bad_hour():
  with pytest.raises(ValidationError):
    FlightData(day=1, month=1, year=2000, hour=24, carrier="AA", distance=1, wind_spd=1)

def test_bad_month():
  with pytest.raises(ValidationError):
    FlightData(day=1, month=0, year=2000, hour=0, carrier="AA", distance=1, wind_spd=1)

def test_bad_year():
  with pytest.raises(ValidationError):
    FlightData(day=1, month=1, year=2051, hour=0, carrier="AA", distance=1, wind_spd=1)

def test_bad_carrier():
  with pytest.raises(ValidationError):
    FlightData(day=1, month=1, year=2050, hour=0, carrier="A", distance=1, wind_spd=1)

def test_bad_distance():
  with pytest.raises(ValidationError):
    FlightData(day=1, month=1, year=2050, hour=0, carrier="UA", distance=0, wind_spd=1)

def test_bad_wind_spd():
  with pytest.raises(ValidationError):
    FlightData(day=1, month=1, year=2050, hour=0, carrier="UA", distance=1, wind_spd=-1)

def test_valid_flight_data():
  f = FlightData(day=1, month=1, year=2050, hour=0, carrier="ua", distance=1, wind_spd=1)
  assert f.year == 2050
  assert f.carrier == "ua"