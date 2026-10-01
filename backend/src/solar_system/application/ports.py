from datetime import datetime
from typing import Protocol

from solar_system.domain.celestial_body import BodyId
from solar_system.domain.position import Position


class EphemerisProvider(Protocol):
    """Port: anything able to tell where a body is at a given instant.

    Contract: `moment` is timezone-aware and expressed in UTC; the result is
    heliocentric, geometric, ecliptic J2000, in AU (see ADR 0001).
    """

    def get_position(self, body: BodyId, moment: datetime) -> Position: ...
