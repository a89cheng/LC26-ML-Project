from weather import fetch_forecast
from database import engine # The variable

import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def run_pipeline():
    # Fetch the forecast data and immediately put it into the database
    forecast_df = await fetch_forecast(latitude= 47.965378, longitude= -81.873536)
    insert_foreasts(forecast_df)


# Instantiates object of scheduling specifically for AsyncIO
# Needs to be at module level so it doesn't get garbage collected
scheduler = AsyncIOScheduler()

async def start_scheduler():
    # Run it every hour; required 'interval'
    scheduler.add_job(run_pipeline, 'interval', hours=1)
    # Start it 
    scheduler.start()

def insert_foreasts(forecast_dataframe):
    # Allows understanding of db tables as python objects
    metadata = MetaData()
    # The forecasts' table name
    table_name = "forecasts"
    # Reflect the target table from the database
    my_table = Table(table_name, metadata, autoload_with=engine)

    # Orienting in records allows for each row to a dict in a list representing the whole table
    forecasts = forecast_dataframe.to_dict(orient='records')

    # Column names 
    column_names = [
        "forecast_hour", "fetched_time", "temperature", "pressure",
        "wind_speed_110", "wind_dir_110", "wind_speed_320", "wind_dir_320", "wind_speed_500",
        "wind_dir_500", "wind_speed_800", "wind_dir_800", "wind_speed_1000", "wind_dir_1000",
        "wind_speed_1500", "wind_dir_1500", "wind_speed_1900", "wind_dir_1900", "wind_speed_3200",
        "wind_dir_3200", "wind_speed_4200", "wind_dir_4200", "wind_speed_5600", "wind_dir_5600",
        "wind_speed_7200", "wind_dir_7200", "wind_speed_9200", "wind_dir_9200", "wind_speed_10400",
        "wind_dir_10400", "wind_speed_11800", "wind_dir_11800", "wind_speed_13500", "wind_dir_13500",
        "wind_speed_15800", "wind_dir_15800", "wind_speed_17700", "wind_dir_17700", "wind_speed_19300",
        "wind_dir_19300", "wind_speed_22000", "wind_dir_22000",
    ]

    # Upsert Statement 
    stmt = insert(my_table).values(forecasts)
    upsert_stmt = stmt.on_conflict_do_update( 
        # The conflict target:
        index_elements=['forecast_hour'],

        # Columns that should be updated (column -> value)
        set_={
            # stmt.excluded is an object, and the column names are object attributes / variables
            # meaning getattr would yield the value of the class variables
            column : getattr(stmt.excluded,column)for column in column_names
        }
    )
       
    # After the statment has been built, execute it!
    with engine.begin() as conn:
        conn.execute(upsert_stmt)