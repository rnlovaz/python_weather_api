from datetime import datetime

from fastapi import Depends
from sqlmodel import Session

from database import get_session
from services.forecast_refresh_service import ForecastRefreshService
from services.logger import get_logger

from .models import ForecastModel
from .repository import ForecastRepository

logger = get_logger(__name__)


class ForecastController:
    def __init__(
        self,
        session: Session = Depends(get_session),
        forecast_refresh_service: ForecastRefreshService = Depends(),
    ):
        self.forecast_repo = ForecastRepository(session)
        self.forecast_refresh_service = forecast_refresh_service

    def get_forecast_by_slug_and_period(
        self, slug: str, from_date: datetime, to_date: datetime
    ) -> list[ForecastModel]:
        entities = self.forecast_repo.get_forecast_by_slug_and_period(
            slug=slug, from_date=from_date, to_date=to_date
        )
        logger.debug("get_forecast_by_slug_and_period - entities: %s", entities)

        models = [ForecastModel.from_entity(entity) for entity in entities]
        logger.debug("get_forecast_by_slug_and_period - models: %s", models)

        return models

    def refresh_daily_forecasts(self) -> None:
        self.forecast_refresh_service.refresh_all_locations_forecast()
