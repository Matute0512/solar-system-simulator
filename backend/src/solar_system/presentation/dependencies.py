from typing import Annotated

from fastapi import Depends, Request

from solar_system.application.get_planet_positions import GetPlanetPositions
from solar_system.application.ports import EphemerisProvider


def get_provider(request: Request) -> EphemerisProvider:
    provider: EphemerisProvider = request.app.state.provider
    return provider


def get_use_case(
    provider: Annotated[EphemerisProvider, Depends(get_provider)],
) -> GetPlanetPositions:
    return GetPlanetPositions(provider)
