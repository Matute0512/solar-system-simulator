from dataclasses import dataclass
from enum import Enum


class BodyId(str, Enum):
    """Stable identifiers of the supported bodies.

    The values are also the identifiers used in the public API.
    Declaration order matters: it goes from the Sun outwards.
    """

    SUN = "sun"
    MERCURY = "mercury"
    VENUS = "venus"
    EARTH = "earth"
    MARS = "mars"
    JUPITER = "jupiter"
    SATURN = "saturn"
    URANUS = "uranus"
    NEPTUNE = "neptune"


@dataclass(frozen=True, slots=True)
class CelestialBody:
    """A body of the Solar System, as known by the domain."""

    id: BodyId
    name: str


SOLAR_SYSTEM: tuple[CelestialBody, ...] = tuple(
    CelestialBody(id=body, name=body.value.capitalize()) for body in BodyId
)
