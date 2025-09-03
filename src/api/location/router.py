from fastapi import APIRouter, Depends, HTTPException

from .controller import LocationController
from .exceptions import LocationAlreadyExistsError, LocationNotFoundError
from .schemas import CreateLocationSchema, LocationSchema, UpdateLocationSchema

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
    models = controller.list_locations()
    return [LocationSchema.from_model(model) for model in models]


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
        return LocationSchema.from_model(model)
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
        return LocationSchema.from_model(model)
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
        return LocationSchema.from_model(model)
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
