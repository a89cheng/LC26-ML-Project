from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import Time, DateTime, func
import datetime

# Base; subclass of DeclarativeBase from SQLAlchemy
class Base(DeclarativeBase):
    pass 

# Previous simulation profiles
class Simulations(Base):
    __tablename__ = "simulations"

    id : Mapped[int] = mapped_column(primary_key=True)
    flight_date: Mapped[datetime.date] = mapped_column(nullable=False)
    landing_lat: Mapped[float] = mapped_column(nullable=False)
    landing_lon: Mapped[float] = mapped_column(nullable=False)
    apogee_ft: Mapped[float] = mapped_column(nullable=False)
    distance_nm: Mapped[float] = mapped_column(nullable=False)
    within_safe_zone: Mapped[bool] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    pressure: Mapped[float] = mapped_column(nullable=False)

    wind_speed_110: Mapped[float]
    wind_dir_110: Mapped[float]

    wind_speed_320: Mapped[float]
    wind_dir_320: Mapped[float]

    wind_speed_500: Mapped[float]
    wind_dir_500: Mapped[float]

    wind_speed_800: Mapped[float]
    wind_dir_800: Mapped[float]

    wind_speed_1000: Mapped[float]
    wind_dir_1000: Mapped[float]

    wind_speed_1500: Mapped[float]
    wind_dir_1500: Mapped[float]

    wind_speed_1900: Mapped[float]
    wind_dir_1900: Mapped[float]

    wind_speed_3200: Mapped[float]
    wind_dir_3200: Mapped[float]

    wind_speed_4200: Mapped[float]
    wind_dir_4200: Mapped[float]

    wind_speed_5600: Mapped[float]
    wind_dir_5600: Mapped[float]

    wind_speed_7200: Mapped[float]
    wind_dir_7200: Mapped[float]

    wind_speed_9200: Mapped[float]
    wind_dir_9200: Mapped[float]

    wind_speed_10400: Mapped[float]
    wind_dir_10400: Mapped[float]

    wind_speed_11800: Mapped[float]
    wind_dir_11800: Mapped[float]

    wind_speed_13500: Mapped[float]
    wind_dir_13500: Mapped[float]

    wind_speed_15800: Mapped[float]
    wind_dir_15800: Mapped[float]

    wind_speed_17700: Mapped[float]
    wind_dir_17700: Mapped[float]

    wind_speed_19300: Mapped[float]
    wind_dir_19300: Mapped[float]

    wind_speed_22000: Mapped[float]
    wind_dir_22000: Mapped[float]

# All the forecasted winds at different altitudes in metres
class Forecasts(Base):
    __tablename__ = "forecasts"

    id : Mapped[int] = mapped_column(primary_key=True)
    fetched_time: Mapped[datetime.datetime] = mapped_column(nullable=False)
    forecast_hour: Mapped[datetime.datetime] = mapped_column(nullable=False) #I'm not sure what the difference here is between the one before
    temperature: Mapped[float]
    pressure: Mapped[float]

    wind_speed_110: Mapped[float]
    wind_dir_110: Mapped[float]

    wind_speed_320: Mapped[float]
    wind_dir_320: Mapped[float]

    wind_speed_500: Mapped[float]
    wind_dir_500: Mapped[float]

    wind_speed_800: Mapped[float]
    wind_dir_800: Mapped[float]

    wind_speed_1000: Mapped[float]
    wind_dir_1000: Mapped[float]

    wind_speed_1500: Mapped[float]
    wind_dir_1500: Mapped[float]

    wind_speed_1900: Mapped[float]
    wind_dir_1900: Mapped[float]

    wind_speed_3200: Mapped[float]
    wind_dir_3200: Mapped[float]

    wind_speed_4200: Mapped[float]
    wind_dir_4200: Mapped[float]

    wind_speed_5600: Mapped[float]
    wind_dir_5600: Mapped[float]

    wind_speed_7200: Mapped[float]
    wind_dir_7200: Mapped[float]

    wind_speed_9200: Mapped[float]
    wind_dir_9200: Mapped[float]

    wind_speed_10400: Mapped[float]
    wind_dir_10400: Mapped[float]

    wind_speed_11800: Mapped[float]
    wind_dir_11800: Mapped[float]

    wind_speed_13500: Mapped[float]
    wind_dir_13500: Mapped[float]

    wind_speed_15800: Mapped[float]
    wind_dir_15800: Mapped[float]

    wind_speed_17700: Mapped[float]
    wind_dir_17700: Mapped[float]

    wind_speed_19300: Mapped[float]
    wind_dir_19300: Mapped[float]

    wind_speed_22000: Mapped[float]
    wind_dir_22000: Mapped[float]


class Predictions(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    forecast_id: Mapped[int] = mapped_column(ForeignKey("forecasts.id"))
    predicted_at: Mapped[datetime.datetime] = mapped_column(nullable=False)
    forecast_hour: Mapped[datetime.datetime] = mapped_column(nullable=False)
    scenario: Mapped[str] = mapped_column(nullable=False)

    landing_lat: Mapped[float]
    landing_lon: Mapped[float]
    predicted_dist_nm: Mapped[float]

    # The following 3 metrics are used to draw the prediction ellipses around landings
    ellipse_major_deg: Mapped[float]
    ellipse_minor_deg: Mapped[float]
    ellipse_tilt_deg: Mapped[float]

    # Is from 0 - 1 (%)
    p_safe_launch: Mapped[float]
    go_no_go: Mapped[bool]

    # Altitude with the greatest risk / risk factor
    top_risk_altitude: Mapped[int] 
    top_risk_factor: Mapped[float]