from datetime import datetime
from typing import Any

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.api.location.entities import LocationEntity

from .entities import ForecastEntity


class ForecastRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_forecast_by_slug_and_period(
        self, slug: str, from_date: datetime, to_date: datetime
    ) -> list[ForecastEntity]:
        statement = (
            select(ForecastEntity)
            .join(LocationEntity)
            .options(selectinload(ForecastEntity.location))  # type: ignore
            .where(
                LocationEntity.slug == slug,
                ForecastEntity.forecast_date >= from_date,
                ForecastEntity.forecast_date <= to_date,
            )
        )

        return list(self.session.exec(statement).all())

    def get_one(self, forecast_id: int) -> ForecastEntity | None:
        return self.session.exec(
            select(ForecastEntity).where(ForecastEntity.forecast_id == forecast_id)
        ).one_or_none()

    def create(
        self, location_id: int, forecast_date: datetime, min_temp: int, max_temp: int
    ) -> ForecastEntity:
        new_forecast = ForecastEntity(
            location_id=location_id,
            forecast_date=forecast_date,
            min_forecasted=min_temp,
            max_forecasted=max_temp,
        )
        self.session.add(new_forecast)
        self.session.commit()
        self.session.refresh(new_forecast)
        return new_forecast

    def update(
        self, forecast_id: int, update_data: dict[str, Any]
    ) -> ForecastEntity | None:
        target_forecast = self.session.exec(
            select(ForecastEntity).where(ForecastEntity.forecast_id == forecast_id)
        ).one_or_none()

        if not target_forecast:
            return None

        # Loop update dict keys/values and update them in stored entity
        for key, value in update_data.items():
            setattr(target_forecast, key, value)

        self.session.add(target_forecast)
        self.session.commit()
        self.session.refresh(target_forecast)
        return target_forecast

    def delete(self, forecast_id: int) -> ForecastEntity | None:
        target_forecast = self.session.exec(
            select(ForecastEntity).where(ForecastEntity.forecast_id == forecast_id)
        ).one_or_none()

        if not target_forecast:
            return None

        self.session.delete(target_forecast)
        self.session.commit()
        return target_forecast
