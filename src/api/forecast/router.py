from datetime import date, datetime

from fastapi import APIRouter, Depends

from .controller import ForecastController
from .schemas import ForecastSchema

router = APIRouter()


@router.get(
    "/{location}",
    summary="Retrieves a forecast for a specific location",
    response_model=list[ForecastSchema],
)
def get_forecast(
    location: str,
    start_date: date,
    end_date: date,
    controller: ForecastController = Depends(),
) -> list[ForecastSchema]:
    if start_date > end_date:
        raise ValueError("start_date must happen before end_date")

    # Parse dates to datetime, so that start has 00:00:00 and end has 23:59:59 timestamps
    parsed_start_date = datetime.combine(start_date, datetime.min.time())
    parsed_end_date = datetime.combine(end_date, datetime.max.time())

    models = controller.get_forecast_by_slug_and_period(
        slug=location,
        from_date=parsed_start_date,
        to_date=parsed_end_date,
    )
    return [ForecastSchema.from_model(model) for model in models]
