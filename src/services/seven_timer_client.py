import requests
from pydantic import BaseModel


class SevenTimerWindDTO(BaseModel):
    direction: str
    speed: int


class SevenTimerDataSeriesDTO(BaseModel):
    timepoint: int
    cloudcover: int
    seeing: int
    transparency: int
    lifted_index: int
    rh2m: int
    wind10m: SevenTimerWindDTO
    temp2m: int
    prec_type: str


class SevenTimerResponseDTO(BaseModel):
    product: str
    init: str
    dataseries: list[SevenTimerDataSeriesDTO]


class SevenTimerClient:
    BASE_URL = "https://www.7timer.info/bin/astro.php"

    def get_forecast(self, lat: float, lon: float) -> SevenTimerResponseDTO:
        """
        Retrieves forecast data using the 'Astro' product of 7timer.
        """

        # Parameters required to fetch 7timer data
        payload = {
            "lon": str(lon),
            "lat": str(lat),
            "ac": "0",
            "unit": "metric",
            "output": "json",
            "tz_shift": "0",
        }

        response = requests.get(
            url=self.BASE_URL,
            params=payload,
        )
        response_json = response.json()
        return SevenTimerResponseDTO(**response_json)
