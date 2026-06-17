import openmeteo_requests

import pandas as pd
import numpy as np
import datetime
import requests_cache
from retry_requests import retry

async def fetch_forecast(latitude, longitude):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["wind_speed_1000hPa", "wind_speed_975hPa", "wind_speed_950hPa", "wind_speed_925hPa", "wind_speed_900hPa", 
                   "wind_speed_850hPa", "wind_speed_800hPa", "wind_speed_700hPa", "wind_speed_600hPa", "wind_speed_500hPa", 
                   "wind_speed_400hPa", "wind_speed_300hPa", "wind_speed_250hPa", "wind_speed_200hPa", "wind_speed_50hPa", 
                   "wind_speed_150hPa", "wind_speed_100hPa", "wind_speed_70hPa", "wind_speed_30hPa", 
                   "wind_direction_1000hPa", "wind_direction_975hPa", "wind_direction_950hPa", "wind_direction_700hPa", "wind_direction_600hPa", 
                   "wind_direction_500hPa", "wind_direction_400hPa", "wind_direction_250hPa", "wind_direction_200hPa", "wind_direction_300hPa", 
                   "wind_direction_925hPa", "wind_direction_900hPa", "wind_direction_850hPa", "wind_direction_800hPa", "wind_direction_30hPa", 
                   "wind_direction_50hPa", "wind_direction_70hPa", "wind_direction_100hPa", "wind_direction_150hPa", 
                   "temperature_2m", "surface_pressure"],
        "timezone": "America/New_York",
        "forecast_hours": 168,
    }

    # This is a list of openmeteo_sdk.WeatherApiResponse.WeatherApiResponse objects
    # Each ovject is 1 location; there should only be 1 location here which is Timmins
    responses = openmeteo.weather_api(url, params = params)
    fetched_time = datetime.datetime.now()


    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    hourly = response.Hourly()

    hourly_data = {
        "fetched_time": np.full(params["forecast_hours"],fetched_time),
        "forecast_hour": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end =   pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq =  pd.Timedelta(seconds = hourly.Interval()),
            # Include the left / first or current value
            inclusive = "left"
        ).tz_convert(response.Timezone().decode())
    }

    for idx, parameter in enumerate(params["hourly"]):
        hourly_data[parameter] = hourly.Variables(idx).ValuesAsNumpy()
        

    # hourly_data is a dict of lists / pandas dataframes
    # Hourly dataframe up to 168 hours (7 days) from this instant
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    # Need to change df column names to SQL/ORM names
    hourly_dataframe.rename(columns={
        # wind speeds -> metre-based ORM names
        'wind_speed_1000hPa': 'wind_speed_110',
        'wind_speed_975hPa':  'wind_speed_320',
        'wind_speed_950hPa':  'wind_speed_500',
        'wind_speed_925hPa':  'wind_speed_800',
        'wind_speed_900hPa':  'wind_speed_1000',
        'wind_speed_850hPa':  'wind_speed_1500',
        'wind_speed_800hPa':  'wind_speed_1900',
        'wind_speed_700hPa':  'wind_speed_3200',
        'wind_speed_600hPa':  'wind_speed_4200',
        'wind_speed_500hPa':  'wind_speed_5600',
        'wind_speed_400hPa':  'wind_speed_7200',
        'wind_speed_300hPa':  'wind_speed_9200',
        'wind_speed_250hPa':  'wind_speed_10400',
        'wind_speed_200hPa':  'wind_speed_11800',
        'wind_speed_50hPa':   'wind_speed_13500',
        'wind_speed_150hPa':  'wind_speed_15800',
        'wind_speed_100hPa':  'wind_speed_17700',
        'wind_speed_70hPa':   'wind_speed_19300',
        'wind_speed_30hPa':   'wind_speed_22000',

        # wind directions -> ORM names
        'wind_direction_1000hPa': 'wind_dir_110',
        'wind_direction_975hPa':  'wind_dir_320',
        'wind_direction_950hPa':  'wind_dir_500',
        'wind_direction_925hPa':  'wind_dir_800',
        'wind_direction_900hPa':  'wind_dir_1000',
        'wind_direction_850hPa':  'wind_dir_1500',
        'wind_direction_800hPa':  'wind_dir_1900',
        'wind_direction_700hPa':  'wind_dir_3200',
        'wind_direction_600hPa':  'wind_dir_4200',
        'wind_direction_500hPa':  'wind_dir_5600',
        'wind_direction_400hPa':  'wind_dir_7200',
        'wind_direction_300hPa':  'wind_dir_9200',
        'wind_direction_250hPa':  'wind_dir_10400',
        'wind_direction_200hPa':  'wind_dir_11800',
        'wind_direction_50hPa':   'wind_dir_13500',
        'wind_direction_150hPa':  'wind_dir_15800',
        'wind_direction_100hPa':  'wind_dir_17700',
        'wind_direction_70hPa':   'wind_dir_19300',
        'wind_direction_30hPa':   'wind_dir_22000',

        'temperature_2m': 'temperature',
        'surface_pressure': 'pressure',
    }, inplace=True)

    hourly_dataframe = hourly_dataframe[
        hourly_dataframe['forecast_hour'].dt.hour.between(11, 18)
    ]

    return hourly_dataframe