from fastapi import APIRouter

# Initialize a new router
router = APIRouter()


@router.get("/")
async def get_locations():
    fake_locations = [
        {"name": "Lisbon", "lat": 25, "lon": 30},
        {"name": "Porto", "lat": 25, "lon": 30},
    ]
    return fake_locations
