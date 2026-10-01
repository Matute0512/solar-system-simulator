from dataclasses import FrozenInstanceError

import pytest

from solar_system.domain.celestial_body import SOLAR_SYSTEM, BodyId


def test_body_id_is_created_from_api_string() -> None:
    # The public API uses lowercase strings; the enum must parse them.
    assert BodyId("earth") is BodyId.EARTH


def test_unknown_body_id_is_rejected() -> None:
    # The endpoint will rely on this to validate user input.
    with pytest.raises(ValueError):
        BodyId("pluto")


def test_solar_system_has_sun_and_eight_planets() -> None:
    assert len(SOLAR_SYSTEM) == 9
    assert SOLAR_SYSTEM[0].id is BodyId.SUN


def test_every_body_id_appears_exactly_once() -> None:
    ids = [body.id for body in SOLAR_SYSTEM]

    assert len(ids) == len(set(ids))
    assert set(ids) == set(BodyId)


def test_bodies_are_ordered_from_the_sun_outwards() -> None:
    ids = [body.id.value for body in SOLAR_SYSTEM]

    assert ids == [
        "sun",
        "mercury",
        "venus",
        "earth",
        "mars",
        "jupiter",
        "saturn",
        "uranus",
        "neptune",
    ]


def test_celestial_body_is_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        SOLAR_SYSTEM[0].name = "Star"
