from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, Field

from .models import LocationModel


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
    location_id: Optional[int]
    slug: str
    name: Optional[str]
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, model: LocationModel) -> LocationSchema:
        return LocationSchema(
            location_id=model.location_id,
            slug=model.slug,
            name=model.name,
            latitude=model.latitude,
            longitude=model.longitude,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class CreateLocationSchema(BaseModel):
    slug: Annotated[str, AfterValidator(is_url_safe)] = Field(max_length=200)
    latitude: float
    longitude: float


class UpdateLocationSchema(BaseModel):
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
