from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from solar_system.presentation.error_handlers import register_error_handlers
from solar_system.presentation.lifespan import lifespan
from solar_system.presentation.routers import positions


class HealthResponse(BaseModel):
    status: Literal["ok"]


app = FastAPI(title="Solar System Simulator", lifespan=lifespan)
app.include_router(positions.router)
register_error_handlers(app=app)


@app.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="ok")
