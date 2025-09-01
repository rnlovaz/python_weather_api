from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .entities import LocationEntity


class LocationModel(BaseModel):
    location_id: Optional[int]
    slug: str
    name: Optional[str]
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: LocationEntity) -> LocationModel:
        return LocationModel(
            location_id=entity.location_id,
            slug=entity.slug,
            name=entity.name,
            latitude=entity.latitude,
            longitude=entity.longitude,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
