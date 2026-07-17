# Run with: uvicorn main:app --reload
# CORS issue I had: https://stackoverflow.com/questions/43871637/no-access-control-allow-origin-header-is-present-on-the-requested-resource-whe

from datetime import datetime
from fastapi import (FastAPI, Depends)
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
                "RMS": 0.4357668309650903,
                "R2": 98.5289024797363
            },
            "Latitude": {
                "RMS": 0.008949873962128228,
                "R2": 98.73562002863256
            },
            "Longitude": {
                "RMS": 0.016541954777753953,
                "R2": 97.66039100057397
            }
        },
        "DrogueOnly": {
            "Distance": {
                "RMS": 0.2965928984507634,
                "R2": 90.93797306202649
            },
            "Latitude": {
                "RMS": 0.004991054173949448,
                "R2": 95.40817033110088
            },
            "Longitude": {
                "RMS": 0.0063404774255936365,
                "R2": 97.07647530998941
            }
        },
        "Ballistic": {
            "Distance": {
                "RMS": 0.1902049111228166,
                "R2": 98.17142721447376
            },
            "Latitude": {
                "RMS": 0.008381319783534628,
                "R2": 93.37741209035704
            },
            "Longitude": {
                "RMS": 0.0060909243200914,
                "R2": 97.65448201644368
            }
        },
        "Nominal": {
            "Distance": {
                "RMS": 0.284404021884833,
                "R2": 91.32497143653473
            },
            "Latitude": {
                "RMS": 0.004744508413347208,
                "R2": 95.71783744451988
            },
            "Longitude": {
                "RMS": 0.006620665614412779,
                "R2": 96.68732409874212
            }
        }
    }