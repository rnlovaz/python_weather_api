from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session

from database import engine

from .forecast_refresh_service import ForecastRefreshService
from .seven_timer_client import SevenTimerClient


def start_scheduler() -> None:
    scheduler = BackgroundScheduler()

    # Add a new cron job that runs at 01:00 everyday
    scheduler.add_job(func=refresh_forecasts, trigger="cron", hour=1, minute=0)
    print("Starting forecasts update scheduler...")
    scheduler.start()


def refresh_forecasts():
    # Because this runs out of FastAPI route context, we need to setup a fresh DB connection,
    # instead of using the session getter
    with Session(engine) as session:
        service = ForecastRefreshService(
            session=session, seven_timer_client=SevenTimerClient()
        )
        service.refresh_all_locations_forecast()
