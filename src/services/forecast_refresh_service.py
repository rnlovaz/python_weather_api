import time
from datetime import date, datetime

from fastapi import Depends
from sqlmodel import Session

from api.forecast.repository import ForecastRepository
from api.forecast.schemas import UpdateForecastSchema
from api.location.entities import LocationEntity
from api.location.repository import LocationRepository
from database import get_session

from .seven_timer_client import SevenTimerClient, SevenTimerResponseDTO


class ForecastRefreshService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        seven_timer_client: SevenTimerClient = Depends(),
    ):
        self.location_repo = LocationRepository(session)
        self.forecast_repo = ForecastRepository(session)
        self.seven_timer_client = seven_timer_client

    def _get_min_max_temp(
        self, forecast_data: SevenTimerResponseDTO
    ) -> tuple[int, int]:
        """
        Extract min and max temperatures for a 7timer API response. Returned tuple consists on (min, max).
        """
        daily_temps = [data.temp2m for data in forecast_data.dataseries]
        return min(daily_temps), max(daily_temps)

    def refresh_daily_forecast(self, location: LocationEntity) -> None:
        # fetch daily forecast data from 7timer client
        # Find out max and min temp from response
        # Check if we already have a stored forecast for the current location
        # If forecast already exists, update it (max and min temp values), otherwise create it
        forecast_data = self.seven_timer_client.get_forecast(
            lat=location.latitude, lon=location.longitude
        )
        if not forecast_data:
            raise ValueError("No forecast data available")

        min_temp, max_temp = self._get_min_max_temp(forecast_data)

        today_min_date = datetime.combine(date.today(), datetime.min.time())
        today_max_date = datetime.combine(date.today(), datetime.max.time())

        stored_forecast = self.forecast_repo.get_forecast_by_slug_and_period(
            slug=location.slug, from_date=today_min_date, to_date=today_max_date
        )

        # If a forecast is not available, create one
        if not stored_forecast:
            assert location.location_id is not None
            self.forecast_repo.create(
                location_id=location.location_id,
                forecast_date=today_min_date,
                min_temp=min_temp,
                max_temp=max_temp,
            )
        # Otherwise, update it
        else:
            update_schema = UpdateForecastSchema(
                min_forecasted=min_temp,
                max_forecasted=max_temp,
            )
            assert stored_forecast[0].forecast_id is not None
            self.forecast_repo.update(
                forecast_id=stored_forecast[0].forecast_id,
                update_data=update_schema.model_dump(exclude_unset=True),
            )

    def refresh_all_locations_forecast(self) -> None:
        # fetch all stored locations
        # for each location, refresh daily forecast
        stored_locations = self.location_repo.get_all()

        for location in stored_locations:
            self.refresh_daily_forecast(location)
            time.sleep(2)  # to prevent sven timer API overload
