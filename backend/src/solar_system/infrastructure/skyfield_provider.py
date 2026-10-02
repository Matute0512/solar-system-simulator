from datetime import datetime
from pathlib import Path

from skyfield.api import Loader
from skyfield.errors import EphemerisRangeError
from skyfield.framelib import ecliptic_J2000_frame

from solar_system.domain.celestial_body import BodyId
from solar_system.domain.errors import EphemerisOutOfRangeError
from solar_system.domain.position import Position

_KERNEL_FILE = "de421.bsp"

# DE421 provides body centers only for the Sun, Mercury, Venus and the Earth.
# For Mars and the outer planets it only has system barycenters (ADR 0004).
_KERNEL_NAMES: dict[BodyId, str] = {
    BodyId.SUN: "sun",
    BodyId.MERCURY: "mercury",
    BodyId.VENUS: "venus",
    BodyId.EARTH: "earth",
    BodyId.MARS: "mars barycenter",
    BodyId.JUPITER: "jupiter barycenter",
    BodyId.SATURN: "saturn barycenter",
    BodyId.URANUS: "uranus barycenter",
    BodyId.NEPTUNE: "neptune barycenter",
}


class SkyfieldEphemerisProvider:
    """Adapter: computes positions with Skyfield and the JPL DE421 kernel."""

    def __init__(self, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        # The loader downloads the kernel the first time it is needed.
        loader = Loader(str(data_dir), verbose=False)
        self._ephemeris = loader(_KERNEL_FILE)
        self._timescale = loader.timescale()
        self._sun = self._ephemeris["sun"]

    def get_position(self, body: BodyId, moment: datetime) -> Position:
        t = self._timescale.from_datetime(moment)

        target = self._ephemeris[_KERNEL_NAMES[body]]

        try:
            vector = (target - self._sun).at(t)
            x, y, z = vector.frame_xyz(ecliptic_J2000_frame).au

        except EphemerisRangeError as error:
            # Translate the library error into our domain error.
            raise EphemerisOutOfRangeError(
                f"No ephemeris data available for {moment.isoformat()}"
            ) from error

        return Position(x=float(x), y=float(y), z=float(z))
