from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

# Import types for relationship attributes
# (TYPE_CHECKING is to prevent circular imports)
if TYPE_CHECKING:
    from src.api.location.entities import LocationEntity


class ForecastEntity(SQLModel, table=True):  # type: ignore
    __tablename__ = "forecasts"
    # Table args accepts a tuple
    __table_args__ = (
        UniqueConstraint(
            "location_id", "forecast_date", name="unique_location_date_constraint"
        ),
    )

    forecast_id: Optional[int] = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key="locations.location_id", ondelete="CASCADE")
    forecast_date: datetime
    min_forecasted: int
    max_forecasted: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    # We could use "back_populates" with the relationship field on LocationEntity to have a list of forecasts
    # For now, we don't want any relationship back populate
    location: "LocationEntity" = Relationship(back_populates=None)
