from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from solar_system.config import Settings
from solar_system.infrastructure.skyfield_provider import SkyfieldEphemerisProvider


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Composition root: build the heavy dependencies once, at startup.

    Any error here stops the application from starting (fail fast).
    """
    settings = Settings()
    app.state.provider = SkyfieldEphemerisProvider(settings.data_dir)

    yield
