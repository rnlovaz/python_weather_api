from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint


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
