from sqlmodel import Session, select

from .entities import Location


class LocationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Location]:
        return list(self.session.exec(select(Location)).all())

    def get_one(self, slug: str) -> Location | None:
        return self.session.exec(
            select(Location).where(Location.slug == slug)
        ).one_or_none()

    def create(self, slug: str, lat: float, lon: float) -> Location:
        new_location = Location(slug=slug, latitude=lat, longitude=lon)
        self.session.add(new_location)
        self.session.commit()
        self.session.refresh(new_location)
        return new_location

    # def update(self, slug: str, lat: Optional[float], lon: Optional[float]) -> Location:
    #     pass

    def delete(self, slug: str) -> None:
        pass
