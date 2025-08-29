from fastapi import APIRouter

from .schemas import LocationSchema, UpdateLocationSchema

# Initialize a new router
router = APIRouter()


@router.get(
    "/",
    summary="Retrieves all stored locations",
    response_model=list[LocationSchema],
)
def get_locations() -> list[LocationSchema]:
    raise NotImplementedError()


@router.get(
    "/{slug}",
    summary="Retrieves a specific location",
    response_model=list[LocationSchema],
)
def get_location(slug: str) -> LocationSchema:
    raise NotImplementedError()


@router.patch(
    "/",
    summary="Updates a specific location",
    response_model=list[LocationSchema],
)
def update_location(payload: UpdateLocationSchema) -> LocationSchema:
    raise NotImplementedError()


@router.delete(
    "/{slug}",
    summary="Deletes a specific location",
    response_model=list[LocationSchema],
)
def delete_location(slug: str) -> LocationSchema:
    raise NotImplementedError()
