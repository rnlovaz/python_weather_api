from fastapi import APIRouter, Depends, HTTPException

from services.logger import get_logger

from .controller import LocationController
from .exceptions import LocationAlreadyExistsError, LocationNotFoundError
from .schemas import CreateLocationSchema, LocationSchema, UpdateLocationSchema

# Initialize a new router
router = APIRouter()

logger = get_logger(__name__)


@router.get(
    "/",
    summary="Retrieves all stored locations",
    response_model=list[LocationSchema],
)
def get_locations(
    controller: LocationController = Depends(),
) -> list[LocationSchema]:
    models = controller.list_locations()
    schemas = [LocationSchema.from_model(model) for model in models]
    logger.debug("get_locations - schemas: %s", schemas)
    return schemas


@router.get(
    "/{slug}",
    summary="Retrieves a specific location",
    response_model=LocationSchema,
)
def get_location(
    slug: str,
    controller: LocationController = Depends(),
) -> LocationSchema:
    try:
        model = controller.get_location(slug)
        schema = LocationSchema.from_model(model)
        logger.debug("get_location - schema: %s", schema)
        return schema
    except LocationNotFoundError:
        raise HTTPException(status_code=404, detail="Location not found")


@router.post(
    "/",
    summary="Creates a new location",
    response_model=LocationSchema,
    status_code=201,
    response_description="Location successfully created",
)
def create_location(
    payload: CreateLocationSchema,
    controller: LocationController = Depends(),
) -> LocationSchema:
    try:
        model = controller.create_location(create_schema=payload)
        schema = LocationSchema.from_model(model)
        logger.debug("create_location - schema: %s", schema)
        return schema
    except LocationAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail=f"Location with slug '{payload.slug}' already exists",
        )


@router.patch(
    "/{slug}",
    summary="Updates a specific location",
    response_model=LocationSchema,
    response_description="Location successfully updated",
)
def update_location(
    slug: str,
    payload: UpdateLocationSchema,
    controller: LocationController = Depends(),
) -> LocationSchema:
    try:
        model = controller.update_location(slug=slug, update_schema=payload)
        schema = LocationSchema.from_model(model)
        logger.debug("update_location - schema: %s", schema)
        return schema
    except LocationNotFoundError:
        raise HTTPException(status_code=404, detail="Location not found")


@router.delete(
    "/{slug}",
    summary="Deletes a specific location",
    response_model=None,
    status_code=204,
    response_description="Location successfully deleted",
)
def delete_location(
    slug: str,
    controller: LocationController = Depends(),
) -> None:
    try:
        controller.delete_location(slug=slug)
    except LocationNotFoundError:
        raise HTTPException(status_code=404, detail="Location not found")
