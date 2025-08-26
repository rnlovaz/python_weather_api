from fastapi import FastAPI

from src.api.location.router import router as location_router

# FastAPI server initialization
app = FastAPI()

# Load routers as modules
app.include_router(location_router, prefix="/location", tags=["Location"])
