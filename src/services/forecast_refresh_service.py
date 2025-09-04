import time
from collections import defaultdict
from datetime import date, datetime, timedelta

from fastapi import Depends
from sqlmodel import Session

from api.forecast.repository import ForecastRepository
from api.location.entities import LocationEntity
from api.location.repository import LocationRepository
from database import get_session
from services.logger import get_logger

from .seven_timer_client import SevenTimerClient, SevenTimerResponseDTO

logger = get_logger(__name__)


class ForecastRefreshService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        seven_timer_client: SevenTimerClient = Depends(),
    ):
        self.location_repo = LocationRepository(session)
        self.forecast_repo = ForecastRepository(session)
        self.seven_timer_client = seven_timer_client

    def _parse_daily_forecast(
        self, forecast_data: SevenTimerResponseDTO
    ) -> dict[date, tuple[int, int]]:
        # Parse forecast start timestamp from API response
        forecast_init_time = datetime.strptime(forecast_data.init, "%Y%m%d%H")

        # Dictionary that holds dates as keys and values as a list of temperatures
        daily_temps: dict[date, list[int]] = defaultdict(
            list
        )  # defaultdict allows to initialize non-existing entries with an empty list

        for forecast_entry in forecast_data.dataseries:
            # Calculate entry timestamp based on timepoint increment
            forecast_time = forecast_init_time + timedelta(
                hours=forecast_entry.timepoint
            )
            # Extract date from forecast datetime object
            forecast_date = forecast_time.date()
            # Append current temperature value to correct daily temps dict entry (key is the day)
            daily_temps[forecast_date].append(forecast_entry.temp2m)

        # Build a dict very similar to daily_temps, but values will contain a tuple with min and max temps
        min_max_per_day_dict = {
            key: (min(value), max(value)) for key, value in daily_temps.items()
        }
        logger.debug(
            "_parse_daily_forecast - min_max_per_day_dict: %s", min_max_per_day_dict
        )

        return min_max_per_day_dict

    def refresh_location_forecast(self, location: LocationEntity) -> None:
        # fetch forecast data from 7timer client
        # Parse response to get max and min temp for available days
        # Update or create forecast entries for the current location
        # If forecast already exists, update it (max and min temp values), otherwise create it
        logger.debug(
            "refresh_location_forecast - Retrieving forecast for Location %s:", location
        )
        forecast_data = self.seven_timer_client.get_forecast(
            lat=location.latitude, lon=location.longitude
        )
        if not forecast_data:
            raise ValueError("No forecast data available")

        parsed_daily_temps = self._parse_daily_forecast(forecast_data)

        # Loop forecast data and upsert DB data
        for forecast_date, (forecast_min, forecast_max) in parsed_daily_temps.items():
            logger.debug(
                "Upserting forecast: Date: %s - Min temp: %s Max temp: %s Location ID: %s (%s)",
                forecast_date,
                forecast_min,
                forecast_max,
                location.location_id,
                location.slug,
            )
            self.forecast_repo.upsert(
                location_id=location.location_id,
                forecast_date=forecast_date,
                min_temp=forecast_min,
                max_temp=forecast_max,
            )

    def refresh_all_locations_forecast(self) -> None:
        # fetch all stored locations
        # for each location, refresh forecast
        stored_locations = self.location_repo.get_all()

        for location in stored_locations:
            self.refresh_location_forecast(location)
            time.sleep(2)  # to prevent sven timer API overload
