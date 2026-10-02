from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import AwareDatetime

from solar_system.application.get_planet_positions import GetPlanetPositions
from solar_system.presentation.dependencies import get_use_case
from solar_system.presentation.schemas import PositionsResponse

router = APIRouter(prefix="/api/v1", tags=["positions"])


# Plain `def` on purpose: the calculation is synchronous and CPU-bound,
# so FastAPI runs it in a worker thread instead of blocking the event loop.
@router.get(
    "/positions",
    response_model=PositionsResponse,
    summary="Heliocentric positions of the Sun and the planets",
)
def get_positions(
    date: Annotated[
        AwareDatetime,
        Query(description="ISO-8601 instant with timezone, e.g. 2000-01-01T12:00:00Z."),
    ],
    use_case: Annotated[GetPlanetPositions, Depends(get_use_case)],
) -> PositionsResponse:
    snapshot = use_case.execute(date)
    return PositionsResponse.from_snapshot(snapshot=snapshot)
