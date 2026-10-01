from datetime import datetime, timedelta, timezone

import pytest

from solar_system.application.get_planet_positions import GetPlanetPositions
from solar_system.domain.celestial_body import SOLAR_SYSTEM, BodyId
from solar_system.domain.errors import NaiveDatetimeError
from solar_system.domain.position import Position

UTC_NOON = datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc)


class FakeEphemerisProvider:
    """Test double: records calls and returns a predictable position."""

    def __init__(self) -> None:
        self.calls: list[tuple[BodyId, datetime]] = []

    def get_position(self, body: BodyId, moment: datetime) -> Position:
        self.calls.append((body, moment))
        # x equals the call number, so each body gets a distinct value.
        return Position(x=float(len(self.calls)), y=0.0, z=0.0)


def test_returns_one_position_per_body_in_solar_system_order() -> None:
    use_case = GetPlanetPositions(FakeEphemerisProvider())

    snapshot = use_case.execute(UTC_NOON)

    assert [item.body for item in snapshot.positions] == list(SOLAR_SYSTEM)
    assert [item.position.x for item in snapshot.positions] == [
        float(n) for n in range(1, 10)
    ]


def test_rejects_naive_datetime_without_calling_the_provider() -> None:
    provider = FakeEphemerisProvider()
    use_case = GetPlanetPositions(provider)

    with pytest.raises(NaiveDatetimeError):
        use_case.execute(datetime(2000, 1, 1, 12, 0))

    assert provider.calls == []


def test_normalizes_any_timezone_to_utc() -> None:
    provider = FakeEphemerisProvider()
    use_case = GetPlanetPositions(provider)
    buenos_aires_morning = datetime(
        2000, 1, 1, 9, 0, tzinfo=timezone(timedelta(hours=-3))
    )

    snapshot = use_case.execute(buenos_aires_morning)

    # Aware datetimes compare equal across zones, so we check the offset itself.
    assert snapshot.moment.utcoffset() == timedelta(0)
    assert snapshot.moment == UTC_NOON
    assert all(moment.utcoffset() == timedelta(0) for _, moment in provider.calls)
