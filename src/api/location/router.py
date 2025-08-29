from fastapi import APIRouter, Depends

from .controller import LocationController
from .schemas import LocationSchema, UpdateLocationSchema

# Initialize a new router
router = APIRouter()


@router.get(
    "/",
    summary="Retrieves all stored locations",
    response_model=list[LocationSchema],
)
def get_locations(
    controller: LocationController = Depends(),
) -> list[LocationSchema]:
    raise NotImplementedError()


@router.get(
    "/{slug}",
    summary="Retrieves a specific location",
    response_model=list[LocationSchema],
)
def get_location(
    slug: str,
    controller: LocationController = Depends(),
) -> LocationSchema:
    raise NotImplementedError()


@router.patch(
    "/",
    summary="Updates a specific location",
    response_model=list[LocationSchema],
)
def update_location(
    payload: UpdateLocationSchema,
    controller: LocationController = Depends(),
) -> LocationSchema:
    raise NotImplementedError()


@router.delete(
    "/{slug}",
    summary="Deletes a specific location",
    response_model=list[LocationSchema],
)
def delete_location(
    slug: str,
    controller: LocationController = Depends(),
) -> LocationSchema:
    raise NotImplementedError()
