import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """Cartesian position in astronomical units (AU)

    Frame conventions (heliocentric, ecliptic J2000) are defined by
    ADR 0001; this class only guarantees the values are valid numbers.
    """

    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        if not all(math.isfinite(coord) for coord in (self.x, self.y, self.z)):
            raise ValueError("All coordinates must be finite numbers.")

    @property
    def distance_from_origin(self) -> float:
        """Euclidean distance to the origin (the Sun), in AU."""
        return math.hypot(self.x, self.y, self.z)
