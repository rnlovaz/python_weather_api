from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .entities import ForecastEntity


class ForecastModel(BaseModel):
    forecast_id: Optional[int]
    location_id: int
    forecast_date: datetime
    min_forecasted: int
    max_forecasted: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: ForecastEntity) -> ForecastModel:
        return ForecastModel(
            forecast_id=entity.forecast_id,
            location_id=entity.location_id,
            forecast_date=entity.forecast_date,
            min_forecasted=entity.min_forecasted,
            max_forecasted=entity.max_forecasted,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
