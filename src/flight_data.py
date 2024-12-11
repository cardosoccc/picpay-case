from pydantic import BaseModel, Field

class FlightData(BaseModel):
    day: int = Field(ge=1, le=31)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=2050)
    hour: int = Field(ge=0, le=23)
    carrier: str = Field(min_length=2, max_length=2)
    distance: float = Field(gt=0)
    wind_spd: float = Field(ge=0)
