from weather import fetch_forecast
from database import (engine, SessionLocal) # The variable
from predict import run_predictions
from models import (Forecasts, Predictions) # Import the table object itself!

import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import MetaData, Table
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Instantiates object of scheduling specifically for AsyncIO
# Needs to be at module level so it doesn't get garbage collected
scheduler = AsyncIOScheduler()

async def start_scheduler():
    # Run it every hour; required 'interval' | if the job is missed, log an error and force it to run now
    scheduler.add_job(run_pipeline, 'interval', minutes=1,next_run_time=datetime.now(), misfire_grace_time=None)
    # Start it 
    scheduler.start()


async def run_pipeline():
    # Fetch the forecast API data and immediately put it into the database
    forecast_df = await fetch_forecast(latitude= 47.965378, longitude= -81.873536)
    print(forecast_df.shape[0])
    insert_forecasts(forecast_df)
    print('forecasts inserted')
    
    # Taking the most recent timestamp of when the data was fetched
    most_recent_fetch_time = forecast_df['fetched_time'].iloc[0]
    
    db = SessionLocal()
    try:
        # In the format of each row being an index of the table object
        forecasts = db.execute(extract_predictive_forecasts(most_recent_fetch_time)).scalars().all()
        print(f"Queried {len(forecasts)} forecast rows from DB")
    finally:
        db.close()

    try:
        # returns a dict in the format: Name of model : [[prediction column] , [RMS, R^2], timestamp] 
        metadata_df, predictions = run_predictions(forecasts)
        print(f"Prediction keys: {predictions.keys()}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return

    predictions_df = predictions_to_dataframe(metadata_df, predictions)
    predictions_df['p_safe_launch'] = ((1 - predictions_df['predicted_dist_nm']) / 10).clip(lower=0) # minimum threshold
    predictions_df['go_no_go'] = predictions_df['predicted_dist_nm'] < 10
    predictions_df['predicted_at'] = datetime.now()
    print(f"Predictions DataFrame shape: {predictions_df.shape}")

    insert_predictions(predictions_df)
    print('Predictions inserted')

def insert_forecasts(forecast_dataframe):
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


def extract_predictive_forecasts(most_recent_fetch_time):
    predictive_columns = [
        "id", "forecast_hour", "temperature", "pressure",
        "wind_speed_110", "wind_dir_110", "wind_speed_320", "wind_dir_320", "wind_speed_500",
        "wind_dir_500", "wind_speed_800", "wind_dir_800", "wind_speed_1000", "wind_dir_1000",
        "wind_speed_1500", "wind_dir_1500", "wind_speed_1900", "wind_dir_1900", "wind_speed_3200",
        "wind_dir_3200", "wind_speed_4200", "wind_dir_4200", "wind_speed_5600", "wind_dir_5600",
        "wind_speed_7200", "wind_dir_7200", "wind_speed_9200", "wind_dir_9200", "wind_speed_10400",
        "wind_dir_10400", "wind_speed_11800", "wind_dir_11800", "wind_speed_13500", "wind_dir_13500",
        "wind_speed_15800", "wind_dir_15800", "wind_speed_17700", "wind_dir_17700", "wind_speed_19300",
        "wind_dir_19300", "wind_speed_22000", "wind_dir_22000",
    ]
    stmt = (
        # Forecasts instead of forecasts since the class name maps to the table accordingly
        select(Forecasts)
        .where(Forecasts.fetched_time == most_recent_fetch_time)
        .order_by(Forecasts.forecast_hour)
    )

    return stmt


def predictions_to_dataframe(metadata_df, predictions):
    # Format of predictions: Name of model : [[prediction column] , [RMS, R^2], timestamp] 
    prediction_dfs = []

    for scenario, columns in predictions.items():
        predicted_columns = columns
        predicted_columns['scenario'] = np.full(len(next(iter(columns.values()))),scenario)
        group_df = pd.DataFrame(predicted_columns)
        full_group_df = pd.concat([metadata_df, group_df], axis=1)
        prediction_dfs.append(full_group_df)

    all_predictions_df = pd.concat(prediction_dfs)
    all_predictions_df = all_predictions_df.rename(columns={'id': 'forecast_id'})

    return all_predictions_df


def insert_predictions(predictions_df):
    # Clean predictions df
    predictions_df = predictions_df[["forecast_id", "predicted_at", "forecast_hour", 
                                     "scenario", "landing_lat", "landing_lon", "predicted_dist_nm", 
                                     "p_safe_launch", "go_no_go"]]
    # Allows understanding of db tables as python objects
    metadata = MetaData()
    # The forecasts' table name
    table_name = "predictions"
    # Reflect the target table from the database
    my_table = Table(table_name, metadata, autoload_with=engine)

    # Orienting in records allows for each row to a dict in a list representing the whole table
    predictions = predictions_df.to_dict(orient='records')

    stmt = insert(my_table).values(predictions)

    with engine.begin() as conn:
        conn.execute(stmt)