from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from solar_system.application.get_planet_positions import PositionsSnapshot
from solar_system.domain.celestial_body import BodyId


class PositionSchema(BaseModel):
    """Cartesian coordinates in astronomical units."""

    model_config = ConfigDict(frozen=True)

    x: float = Field(description="X coordinate, in AU.")
    y: float = Field(description="Y coordinate, in AU.")
    z: float = Field(description="Z coordinate (north of the ecliptic), in AU.")


class BodyPositionSchema(BaseModel):
    name: BodyId = Field(description="Identifier of the celestial body.")
    position: PositionSchema


class PositionsResponse(BaseModel):
    """Positions of the Sun and the planets at one instant."""

    date: AwareDatetime = Field(description="Requested instant, normalized to UTC.")
    frame: Literal["ecliptic-J2000"] = "ecliptic-J2000"
    origin: Literal["sun"] = "sun"
    unit: Literal["AU"] = "AU"
    bodies: list[BodyPositionSchema]

    @classmethod
    def from_snapshot(cls, snapshot: PositionsSnapshot) -> "PositionsResponse":
        return cls(
            date=snapshot.moment,
            bodies=[
                BodyPositionSchema(
                    name=bp.body.id,
                    position=PositionSchema(
                        x=bp.position.x, y=bp.position.y, z=bp.position.z
                    ),
                )
                for bp in snapshot.positions
            ],
        )


class ErrorResponse(BaseModel):
    """Body returned for errors caused by the request."""

    code: str = Field(description="Stable, machine-readable error code.")
    detail: str = Field(description="Human-readable explanation.")
