#Run with: uvicorn main:app --reload

from fastapi import (FastAPI, Depends)
from contextlib import asynccontextmanager
from sqlalchemy import select

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


    print("Goodbye")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/predictions")
def get_predictions(session = Depends(get_db)): # Depends closes the yield statement!
    stmt = (
        select(Forecasts, Predictions)
        .join(Predictions, Forecasts.id == Predictions.forecast_id)
        #.where(Predictions.fetched_time == recent_fetched_time)
        .group_by(Predictions.forecast_hour, Predictions.scenario)
    )
    results = session.scalars(stmt).all()

    return results

@app.get("/predictions/{forecast_hour}")
def get_a_prediction():
    pass

@app.get("/forecasts")
def get_all_forecasts():
    pass

@app.get("/forecasts/{forecast_hour}")
def get_a_forecast():
    pass 

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