#Run with: uvicorn main:app --reload

from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create 3 tables (Simulations, Forecast, Predictions) in Docker based Postgres DB
    create_tables()
    yield

    print("Goodbye")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health():
    return {"status": "ok"}