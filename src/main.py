from fastapi import FastAPI

from api.forecast.router import router as forecast_router
from api.location.router import router as location_router

# FastAPI server initialization
app = FastAPI(
    title="Weather API",
    description="A simple weather API with locations CRUD and forecasting data",
)

# Load routers as modules
app.include_router(router=location_router, prefix="/location", tags=["Location"])
app.include_router(router=forecast_router, prefix="/forecast", tags=["Forecast"])
