class NaiveDatetimeError(ValueError):
    """Raised when a datetime without timezone information is received."""


class EphemerisOutOfRangeError(ValueError):
    """Raised when the requested instant is outside the supported range."""
