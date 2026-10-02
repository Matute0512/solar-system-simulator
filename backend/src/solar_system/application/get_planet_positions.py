from dataclasses import dataclass
from datetime import datetime, timezone

from solar_system.application.ports import EphemerisProvider
from solar_system.domain.celestial_body import SOLAR_SYSTEM, CelestialBody
from solar_system.domain.errors import EphemerisOutOfRangeError, NaiveDatetimeError
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
            raise NaiveDatetimeError(f"Datetime must be timezone-aware, got {moment!r}")

        try:
            utc_moment = moment.astimezone(timezone.utc)
        except OverflowError as error:
            # Instants like 9999-12-31T23:59:59-05:00 fall outside the datetime
            # range once converted to UTC.
            raise EphemerisOutOfRangeError(
                f"Instant {moment.isoformat()} cannot be represented in UTC"
            ) from error

        positions: tuple[BodyPosition, ...] = tuple(
            BodyPosition(
                body=body, position=self._provider.get_position(body.id, utc_moment)
            )
            for body in SOLAR_SYSTEM
        )

        return PositionsSnapshot(moment=utc_moment, positions=positions)
