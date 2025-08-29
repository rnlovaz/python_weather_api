from sqlmodel import Session
# from .entities import Location


class LocationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):  # -> list[Location]:
        pass

    def get_one(self, slug: str):  # -> Location:
        pass

    def create(self, slug: str, lat: float, lon: float):  # -> Location:
        pass

    def delete(self, slug: str) -> None:
        pass
