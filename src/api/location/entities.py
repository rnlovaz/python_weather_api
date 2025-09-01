from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class LocationEntity(SQLModel, table=True):  # type: ignore
    __tablename__ = "locations"

    location_id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(max_length=200, unique=True)
    name: Optional[str] = Field(default=None, max_length=200)
    latitude: float
    longitude: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
