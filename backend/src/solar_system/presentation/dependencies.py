from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends

from solar_system.application.get_planet_positions import GetPlanetPositions
from solar_system.application.ports import EphemerisProvider
from solar_system.infrastructure.skyfield_provider import SkyfieldEphemerisProvider

# Composition root: the only place in this layer that knows the concrete adapter.
# Loading the kernel is expensive, so the provider is created once and reused.


@lru_cache
def get_provider() -> EphemerisProvider:
    return SkyfieldEphemerisProvider(data_dir=Path("data"))


def get_use_case(
    provider: Annotated[EphemerisProvider, Depends(get_provider)],
) -> GetPlanetPositions:
    return GetPlanetPositions(provider)
