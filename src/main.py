from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.forecast.router import router as forecast_router
from api.location.router import router as location_router
from services.logger import get_logger
from services.schedulers import start_scheduler

logger = get_logger(__name__)


# Setup the cron to refresh forecasts
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("WeatherAPI app is starting up... 🚀")
    start_scheduler()
    # If we want to perform tasks on FastAPI shutdown
    yield
    # Shutdown logic goes here
    logger.info("WeatherAPI app is shutting down... ⏻")


# FastAPI server initialization
app = FastAPI(
    title="Weather API",
    description="A simple weather API with locations CRUD and forecasting data",
    lifespan=lifespan,
)

# Load routers as modules
app.include_router(router=location_router, prefix="/location", tags=["Location"])
app.include_router(router=forecast_router, prefix="/forecast", tags=["Forecast"])
