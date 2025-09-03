from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.forecast.router import router as forecast_router
from api.location.router import router as location_router
from services.schedulers import start_scheduler


# Setup the cron to refresh forecasts
@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    # If we want to perform tasks on FastAPI shutdown
    yield
    # Shutdown logic goes here


# FastAPI server initialization
app = FastAPI(
    title="Weather API",
    description="A simple weather API with locations CRUD and forecasting data",
    lifespan=lifespan,
)

# Load routers as modules
app.include_router(router=location_router, prefix="/location", tags=["Location"])
app.include_router(router=forecast_router, prefix="/forecast", tags=["Forecast"])
