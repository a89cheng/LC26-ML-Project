#Run with: uvicorn main:app --reload

from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_tables
from pipeline import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create 3 tables (Simulations, Forecast, Predictions) in Docker based Postgres DB
    create_tables()
    # Pulls the weather every hour from open-meteo
    await start_scheduler()

    yield
    start_scheduler.shutdown()

    print("Goodbye")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health():
    return {"status": "ok"}