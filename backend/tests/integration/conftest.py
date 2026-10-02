from pathlib import Path

import pytest
from skyfield.api import Loader
from skyfield.timelib import Timescale

from solar_system.infrastructure.skyfield_provider import SkyfieldEphemerisProvider

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


@pytest.fixture(scope="session")
def provider() -> SkyfieldEphemerisProvider:
    # Session scope: the kernel is loaded once, not once per test.
    return SkyfieldEphemerisProvider(data_dir=DATA_DIR)


@pytest.fixture(scope="session")
def timescale() -> Timescale:
    return Loader(str(DATA_DIR)).timescale()
