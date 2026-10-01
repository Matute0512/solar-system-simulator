from dataclasses import dataclass
from datetime import datetime, timezone

from solar_system.application.ports import EphemerisProvider
from solar_system.domain.celestial_body import SOLAR_SYSTEM, CelestialBody
from solar_system.domain.errors import NaiveDatetimeError
from solar_system.domain.position import Position


@dataclass(frozen=True, slots=True)
class BodyPosition:
    """A celestial body paired with its positions."""

    body: CelestialBody
    position: Position


@dataclass(frozen=True, slots=True)
class PositionsSnapshot:
    """Positions of every supported body at one instant (UTC)."""

    moment: datetime
    positions: tuple[BodyPosition, ...]


class GetPlanetPositions:
    """Use case: positions of the Sun and the planets for a given instant."""

    def __init__(self, provider: EphemerisProvider) -> None:
        # The use case depends on the port, never on a concrete adapter.
        self._provider = provider

    def execute(self, moment: datetime) -> PositionsSnapshot:
        if moment.utcoffset() is None:
            raise NaiveDatetimeError("Datetime must be timezone-aware")

        utc_moment = moment.astimezone(timezone.utc)

        positions: tuple[BodyPosition, ...] = tuple(
            BodyPosition(
                body=body, position=self._provider.get_position(body.id, utc_moment))
            for body in SOLAR_SYSTEM
        )

        return PositionsSnapshot(moment=utc_moment, positions=positions)
