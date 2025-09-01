from typing import Any

from sqlmodel import Session, select

from .entities import LocationEntity


class LocationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[LocationEntity]:
        return list(self.session.exec(select(LocationEntity)).all())

    def get_one(self, slug: str) -> LocationEntity | None:
        return self.session.exec(
            select(LocationEntity).where(LocationEntity.slug == slug)
        ).one_or_none()

    def create(self, slug: str, lat: float, lon: float) -> LocationEntity:
        new_location = LocationEntity(slug=slug, latitude=lat, longitude=lon)
        self.session.add(new_location)
        self.session.commit()
        self.session.refresh(new_location)
        return new_location

    def update(self, slug: str, update_data: dict[str, Any]) -> LocationEntity | None:
        target_location = self.session.exec(
            select(LocationEntity).where(LocationEntity.slug == slug)
        ).one_or_none()

        if not target_location:
            return None

        # Loop update dict keys/values and update them in stored entity
        for key, value in update_data.items():
            setattr(target_location, key, value)

        self.session.add(target_location)
        self.session.commit()
        self.session.refresh(target_location)
        return target_location

    def delete(self, slug: str) -> LocationEntity | None:
        target_location = self.session.exec(
            select(LocationEntity).where(LocationEntity.slug == slug)
        ).one_or_none()

        if not target_location:
            return None

        self.session.delete(target_location)
        self.session.commit()
        return target_location
