from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Location(SQLModel, table=True):  # type: ignore
    id: int = Field(primary_key=True)
    slug: str = Field(lt=200, unique=True)
    name: Optional[str] = Field(default=None, lt=200)
    latitude: float
    longitude: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
