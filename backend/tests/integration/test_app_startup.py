from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from solar_system.presentation.main import app

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def test_app_loads_the_real_ephemeris_on_startup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SOLAR_DATA_DIR", str(DATA_DIR))

    # The Horizons reference values (ADR 0003) are for 2000-01-01 12:00 TDB.
    # In UTC that instant is 64.184 s earlier (32 leap seconds + 32.184 s).
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/positions", params={"date": "2000-01-01T11:58:55.816Z"}
        )

    assert response.status_code == 200
    earth = next(b for b in response.json()["bodies"] if b["name"] == "earth")
    # Same reference values as the JPL Horizons fixtures (ADR 0003).
    assert earth["position"]["x"] == pytest.approx(-0.1771351, abs=1e-6)
    assert earth["position"]["y"] == pytest.approx(0.9672417, abs=1e-6)


def test_app_refuses_to_start_when_the_ephemeris_cannot_be_loaded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def failing_provider(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("kernel unavailable")

    monkeypatch.setattr(
        "solar_system.presentation.lifespan.SkyfieldEphemerisProvider",
        failing_provider,
    )

    # Failing fast is better than a server that answers /health but cannot work.
    with pytest.raises(RuntimeError, match="kernel unavailable"):
        with TestClient(app):
            pass
