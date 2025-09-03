from fastapi import Depends
from sqlmodel import Session

from src.database import get_session

from .exceptions import LocationNotFoundError
from .models import LocationModel
from .repository import LocationRepository
from .schemas import CreateLocationSchema, UpdateLocationSchema


class LocationController:
    def __init__(self, session: Session = Depends(get_session)):
        # Instantiate the location repo with dependency injection of db session
        self.location_repo = LocationRepository(session)

    def list_locations(self) -> list[LocationModel]:
        entities = self.location_repo.get_all()
        models = [LocationModel.from_entity(entity) for entity in entities]
        return models

    def get_location(self, slug: str) -> LocationModel:
        entity = self.location_repo.get_one(slug)
        if not entity:
            raise LocationNotFoundError()
        return LocationModel.from_entity(entity)

    def delete_location(self, slug: str) -> None:
        deleted_entity = self.location_repo.delete(slug)
        # When None is returned, something went wrong with deletion
        if not deleted_entity:
            raise LocationNotFoundError()
        return None

    def update_location(
        self, slug: str, update_schema: UpdateLocationSchema
    ) -> LocationModel:
        updated_entity = self.location_repo.update(
            slug=slug,
            update_data=update_schema.model_dump(exclude_unset=True),
        )
        if not updated_entity:
            raise LocationNotFoundError()
        return LocationModel.from_entity(updated_entity)

    def create_location(self, create_schema: CreateLocationSchema) -> LocationModel:
        new_location = self.location_repo.create(
            slug=create_schema.slug,
            lat=create_schema.latitude,
            lon=create_schema.longitude,
        )
        return LocationModel.from_entity(new_location)
