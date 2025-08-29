from fastapi import Depends
from sqlmodel import Session

from database import get_session

# from .entities import Location
from .repository import LocationRepository
from .schemas import CreateLocationSchema, UpdateLocationSchema, DeleteLocationSchema


class LocationController:
    def __init__(self, session: Session = Depends(get_session)):
        # Instantiate the location repo with dependency injection of db session
        self.location_repo = LocationRepository(session)

    def list_locations(self):
        self

    def get_location(self, slug: str):
        pass

    def delete_location(self, schema: DeleteLocationSchema):
        pass

    def update_location(self, schema: UpdateLocationSchema):
        pass

    def create_location(self, schema: CreateLocationSchema):
        pass
