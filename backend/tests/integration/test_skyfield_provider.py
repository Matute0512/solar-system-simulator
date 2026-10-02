import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest
from skyfield.timelib import Timescale

from solar_system.domain.celestial_body import BodyId
from solar_system.domain.errors import EphemerisOutOfRangeError
from solar_system.infrastructure.skyfield_provider import SkyfieldEphemerisProvider

TOLERANCE_AU = 1e-6  # ~150 km, see ADR 0003
FIXTURES = Path(__file__).resolve(
).parents[1] / "fixtures" / "horizons_vectors.json"


def _load_cases() -> list[Any]:
    data = json.loads(FIXTURES.read_text())
    return [
        pytest.param(
            BodyId(item["body"]),
            item["jd_tdb"],
            item["xyz_au"],
            id=f"{item['body']}-{item['jd_tdb']}",
        )
        for item in data["vectors"]
    ]


@pytest.mark.parametrize(("body", "jd_tdb", "xyz_au"), _load_cases())
def test_position_matches_jpl_horizons(
    provider: SkyfieldEphemerisProvider,
    timescale: Timescale,
    body: BodyId,
    jd_tdb: float,
    xyz_au: list[float],
) -> None:
    # Horizons uses TDB while the port takes a UTC datetime, so we convert at
    # the test boundary (this keeps the comparison free of the ~64 s offset).
    moment = timescale.tdb(jd=jd_tdb).utc_datetime()

    position = provider.get_position(body, moment)

    actual = (position.x, position.y, position.z)
    assert actual == pytest.approx(xyz_au, abs=TOLERANCE_AU)


@pytest.mark.parametrize("body", list(BodyId))
def test_every_body_can_be_computed(
    provider: SkyfieldEphemerisProvider, body: BodyId
) -> None:
    # Guards the name mapping: a missing or wrong kernel name fails here.
    moment = datetime(2026, 10, 1, tzinfo=timezone.utc)

    position = provider.get_position(body, moment)

    assert position.distance_from_origin < 31.0  # Neptune is ~30 AU away


def test_sun_is_at_the_origin(provider: SkyfieldEphemerisProvider) -> None:
    moment = datetime(2000, 1, 1, 12, tzinfo=timezone.utc)

    position = provider.get_position(BodyId.SUN, moment)

    assert position.distance_from_origin == pytest.approx(0.0, abs=1e-12)


@pytest.mark.parametrize("year", [1800, 2200])
def test_raises_when_instant_is_outside_ephemeris_range(
    provider: SkyfieldEphemerisProvider, year: int
) -> None:
    moment = datetime(year, 1, 1, tzinfo=timezone.utc)

    with pytest.raises(EphemerisOutOfRangeError):
        provider.get_position(BodyId.EARTH, moment)
