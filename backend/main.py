#Run with: uvicorn main:app --reload
from datetime import datetime
from fastapi import (FastAPI, Depends)
from contextlib import asynccontextmanager
from sqlalchemy import select, func 
# Func is for aggregate functions!

from database import create_tables, get_db
from pipeline import (start_scheduler, scheduler)
from models import (Simulations, Forecasts, Predictions)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create 3 tables (Simulations, Forecast, Predictions) in Docker based Postgres DB
    create_tables()
    # Pulls the weather every hour from open-meteo
    await start_scheduler()

    yield
    scheduler.shutdown()

    print("Gone Fishing")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/predictions")
def get_predictions(session = Depends(get_db)): # Depends closes the yield statement!
    recent_fetched_time = select(func.max(Forecasts.fetched_time)).scalar_subquery()

    stmt = (
        select(Forecasts, Predictions)
        .join(Predictions, Forecasts.id == Predictions.forecast_id)
        .where(Forecasts.fetched_time == recent_fetched_time)
        .order_by(Forecasts.forecast_hour.asc())
    )

    results = session.execute(stmt).all()

    data = []
    pred_cols = ["forecast_hour", "scenario", "landing_lat", "landing_lon", "predicted_dist_nm", "p_safe_launch" , "go_no_go"]
    # Groups of 3 rows, same forecast data but different prediction
    # Constraint of 3 * 56 = 168 predictions for a 7 day span
    for prediction_row in results:
        row = {}
        for column in pred_cols:
            row[column] = getattr(prediction_row[1], column)
        data.append(row)

    return data


@app.get("/predictions/{forecast_hour}")
def get_a_prediction(forecast_hour:datetime, session = Depends(get_db)):
    recent_fetched_time = select(func.max(Forecasts.fetched_time)).scalar_subquery()

    stmt = (
        select(Forecasts, Predictions)
        .join(Predictions, Forecasts.id == Predictions.forecast_id)
        .where(Forecasts.fetched_time == recent_fetched_time, Forecasts.forecast_hour == forecast_hour)
    )

    # There should be 3 predictions per hour
    results = session.execute(stmt).all()

    data = []
    pred_cols = ["forecast_hour", "scenario", "landing_lat", "landing_lon", "predicted_dist_nm", "p_safe_launch" , "go_no_go"]
    # Groups of 3 rows, same forecast data but different prediction
    # Constraint of 3 * 56 = 168 predictions for a 7 day span
    for prediction_row in results:
        row = {}
        for column in pred_cols:
            row[column] = getattr(prediction_row[1], column)
        data.append(row)

    return data

@app.get("/forecasts")
def get_all_forecasts(session = Depends(get_db)):
    recent_fetched_time = select(func.max(Forecasts.fetched_time)).scalar_subquery()

    stmt = (
        select(Forecasts)
        .where(Forecasts.fetched_time == recent_fetched_time)
        .order_by(Forecasts.forecast_hour.asc())
    )

    results = session.scalars(stmt).all()

    return results

@app.get("/forecasts/{forecast_hour}")
def get_a_forecast(forecast_hour:datetime, session = Depends(get_db)):
    recent_fetched_time = select(func.max(Forecasts.fetched_time)).scalar_subquery()

    stmt = (
        select(Forecasts)
        .where(Forecasts.fetched_time == recent_fetched_time, Forecasts.forecast_hour == forecast_hour)
    )

    results = session.scalars(stmt).one_or_none()

    return results

@app.get("/model-information")
def get_model_information():
    return {
        "MainAtApogee": {
            "Distance": {
                "RMS": 0.6292149284861311,
                "R2": 88.42361239411833
            },
            "Latitude": {
                "RMS": 0.013263654077880981,
                "R2": 96.44592203781477
            },
            "Longitude": {
                "RMS": 0.011005687243833478,
                "R2": 97.74570594044413
            }
        },
        "DrogueOnly": {
            "Distance": {
                "RMS": 0.31583345165701154,
                "R2": 91.10914591704421
            },
            "Latitude": {
                "RMS": 0.005348296643518714,
                "R2": 91.6608899390373
            },
            "Longitude": {
                "RMS": 0.008065801204894939,
                "R2": 93.89437241174486
            }
        },
        "Ballistic": {
            "Distance": {
                "RMS": 0.22822758342949032,
                "R2": 97.61126992637005
            },
            "Latitude": {
                "RMS": 0.005529809295388513,
                "R2": 94.60441293165442
            },
            "Longitude": {
                "RMS": 0.00618174126394509,
                "R2": 97.41129142289616
            }
        }
    }