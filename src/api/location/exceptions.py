class LocationNotFoundError(Exception):
    """Raised when a Location is not found."""

    pass


class LocationAlreadyExistsError(Exception):
    """Raised when a Location already exists."""

    pass
