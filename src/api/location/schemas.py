import re
from datetime import datetime
from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, Field


def is_url_safe(slug: str) -> str:
    """
    Validates a given slug is URL safe.
    """
    if not re.match(r"^[a-z0-9-]+$", slug):
        raise ValueError(
            "Slug must only contain non-accented lower case letters, numbers and hyphens"
        )
    else:
        return slug


class LocationSchema(BaseModel):
    id: int
    slug: str
    name: Optional[str]
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime


class GetLocationSchema(BaseModel):
    slug: str


class CreateLocationSchema(BaseModel):
    slug: Annotated[str, AfterValidator(is_url_safe)] = Field(lt=200)
    latitude: float
    longitude: float


class UpdateLocationSchema(BaseModel):
    slug: str
    latitude: Optional[float]
    longitude: Optional[float]


class DeleteLocationSchema(BaseModel):
    slug: str
