from fastapi import Depends
from sqlmodel import Session

from database import get_session
from services.forecast_refresh_service import ForecastRefreshService
from services.logger import get_logger

from .exceptions import LocationAlreadyExistsError, LocationNotFoundError
from .models import LocationModel
from .repository import LocationRepository
from .schemas import CreateLocationSchema, UpdateLocationSchema

logger = get_logger(__name__)


class LocationController:
    def __init__(
        self,
        session: Session = Depends(get_session),
        forecast_refresh_service: ForecastRefreshService = Depends(),
    ):
        # Instantiate the location repo with dependency injection of db session
        self.location_repo = LocationRepository(session)
        self.forecast_refresh_service = forecast_refresh_service

    def list_locations(self) -> list[LocationModel]:
        entities = self.location_repo.get_all()
        logger.debug("list_locations - entities: %s", entities)

        models = [LocationModel.from_entity(entity) for entity in entities]
        logger.debug("list_locations - models: %s", models)

        return models

    def get_location(self, slug: str) -> LocationModel:
        entity = self.location_repo.get_one(slug)
        logger.debug("get_location - entity: %s", entity)
        if not entity:
            raise LocationNotFoundError()

        model = LocationModel.from_entity(entity)
        logger.debug("get_location - model: %s", model)

        return model

    def delete_location(self, slug: str) -> None:
        deleted_entity = self.location_repo.delete(slug)
        logger.debug("delete_location - deleted_entity: %s", deleted_entity)
        # When None is returned, something went wrong with deletion
        if not deleted_entity:
            raise LocationNotFoundError()

    def update_location(
        self, slug: str, update_schema: UpdateLocationSchema
    ) -> LocationModel:
        logger.debug("update_location - update_schema: %s", update_schema)

        update_dict = update_schema.model_dump(exclude_unset=True)
        logger.debug("update_location - update_dict: %s", update_dict)

        updated_entity = self.location_repo.update(
            slug=slug,
            update_data=update_dict,
        )
        logger.debug("update_location - updated_entity: %s", updated_entity)

        if not updated_entity:
            raise LocationNotFoundError()

        updated_model = LocationModel.from_entity(updated_entity)
        logger.debug("update_location - updated_model: %s", updated_model)

        return updated_model

    def create_location(self, create_schema: CreateLocationSchema) -> LocationModel:
        existing_location_entity = self.location_repo.get_one(create_schema.slug)
        logger.debug(
            "create_location - existing_location_entity: %s", existing_location_entity
        )

        # Check if slug is not taken
        if existing_location_entity:
            raise LocationAlreadyExistsError()

        logger.debug("create_location - create_schema: %s", create_schema)

        new_location_entity = self.location_repo.create(
            slug=create_schema.slug,
            lat=create_schema.latitude,
            lon=create_schema.longitude,
        )
        logger.debug("create_location - new_location_entity: %s", new_location_entity)

        # Update forecast for newly created location
        self.forecast_refresh_service.refresh_location_forecast(new_location_entity)

        model = LocationModel.from_entity(new_location_entity)
        logger.debug("create_location - model: %s", model)

        return model
