from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .models import ForecastModel


class ForecastSchema(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=False)

    date: date
    min_forecasted: int = Field(alias="min-forecasted")
    max_forecasted: int = Field(alias="max-forecasted")

    @classmethod
    def from_model(cls, model: ForecastModel) -> ForecastSchema:
        return ForecastSchema(
            date=model.forecast_date.date(),
            min_forecasted=model.min_forecasted,  # type: ignore
            max_forecasted=model.max_forecasted,  # type: ignore
        )


class UpdateForecastSchema(BaseModel):
    min_forecasted: Optional[int] = Field(default=None)
    max_forecasted: Optional[int] = Field(default=None)
