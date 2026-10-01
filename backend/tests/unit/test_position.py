import math
from dataclasses import FrozenInstanceError

import pytest

from solar_system.domain.position import Position


def test_position_stores_coordinates() -> None:
    position = Position(x=1.0, y=2.0, z=3.0)

    # A value object must never change after creation.
    with pytest.raises(FrozenInstanceError):
        position.x = 5.0


def test_positions_with_same_coordinates_are_equal() -> None:
    # Value objects ara compared by value, not by identity.
    assert Position(1.0, 2.0, 3.0) == Position(1.0, 2.0, 3.0)


def test_distance_from_origin() -> None:
    # 3-4-5 triangle: easy to verify by hand.
    assert Position(3.0, 4.0, 0.0).distance_from_origin == pytest.approx(5.0)


@pytest.mark.parametrize("invalid", [math.nan, math.inf, -math.inf])
def test_position_rejects_non_finite_coordinates(invalid: float) -> None:
    with pytest.raises(ValueError):
        Position(x=invalid, y=0.0, z=0.0)
