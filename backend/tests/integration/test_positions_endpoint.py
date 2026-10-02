from collections.abc import Iterator
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from solar_system.application.get_planet_positions import (
    GetPlanetPositions,
    PositionsSnapshot,
)
from solar_system.domain.celestial_body import BodyId
from solar_system.domain.errors import EphemerisOutOfRangeError, NaiveDatetimeError
from solar_system.domain.position import Position
from solar_system.presentation.dependencies import get_use_case
from solar_system.presentation.main import app

EXPECTED_ORDER = [
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


class FakeEphemerisProvider:
    """Test double: x is the index of the body (Sun = 0, Mercury = 1, ...)."""

    def get_position(self, body: BodyId, moment: datetime) -> Position:
        return Position(x=float(list(BodyId).index(body)), y=0.0, z=0.0)


@pytest.fixture
def client() -> Iterator[TestClient]:
    # Replace the real provider (and its kernel download) with the fake one.
    app.dependency_overrides[get_use_case] = lambda: GetPlanetPositions(
        FakeEphemerisProvider()
    )
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_positions_follow_the_documented_contract(client: TestClient) -> None:
    response = client.get("/api/v1/positions", params={"date": "2000-01-01T12:00:00Z"})

    assert response.status_code == 200
    body = response.json()
    assert body["date"] == "2000-01-01T12:00:00Z"
    assert body["frame"] == "ecliptic-J2000"
    assert body["origin"] == "sun"
    assert body["unit"] == "AU"
    assert [item["name"] for item in body["bodies"]] == EXPECTED_ORDER
    earth = body["bodies"][3]
    assert earth["position"] == {"x": 3.0, "y": 0.0, "z": 0.0}


def test_any_utc_offset_is_normalized_to_utc(client: TestClient) -> None:
    response = client.get(
        "/api/v1/positions", params={"date": "2000-01-01T09:00:00-03:00"}
    )

    assert response.status_code == 200
    assert response.json()["date"] == "2000-01-01T12:00:00Z"


@pytest.mark.parametrize(
    "invalid_date",
    ["2000-01-01T12:00:00", "2000-01-01", "not-a-date"],
    ids=["naive-datetime", "date-only", "malformed"],
)
def test_invalid_dates_are_rejected_with_422(
    client: TestClient, invalid_date: str
) -> None:
    response = client.get("/api/v1/positions", params={"date": invalid_date})

    assert response.status_code == 422


def test_missing_date_is_rejected_with_422(client: TestClient) -> None:
    assert client.get("/api/v1/positions").status_code == 422


def test_endpoint_is_documented_in_openapi(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]

    assert "/api/v1/positions" in paths


class RaisingUseCase:
    """Test double: a use case that always fails with the given error."""

    def __init__(self, error: Exception) -> None:
        self._error = error

    def execute(self, moment: datetime) -> PositionsSnapshot:
        raise self._error


def test_date_out_of_range_is_translated_to_422(client: TestClient) -> None:
    app.dependency_overrides[get_use_case] = lambda: RaisingUseCase(
        EphemerisOutOfRangeError("No ephemeris data available for 1800-01-01")
    )

    response = client.get("/api/v1/positions", params={"date": "1800-01-01T00:00:00Z"})

    assert response.status_code == 422
    assert response.json() == {
        "code": "date_out_of_range",
        "detail": "No ephemeris data available for 1800-01-01",
    }


def test_naive_datetime_error_is_translated_to_422(client: TestClient) -> None:
    app.dependency_overrides[get_use_case] = lambda: RaisingUseCase(
        NaiveDatetimeError("Datetime must be timezone-aware")
    )

    response = client.get("/api/v1/positions", params={"date": "2000-01-01T12:00:00Z"})

    assert response.status_code == 422
    assert response.json()["code"] == "naive_datetime"


def test_extreme_dates_are_rejected_with_422(client: TestClient) -> None:
    # Converting this instant to UTC would overflow the datetime range.
    response = client.get(
        "/api/v1/positions", params={"date": "9999-12-31T23:59:59-05:00"}
    )

    assert response.status_code == 422
    assert response.json()["code"] == "date_out_of_range"
