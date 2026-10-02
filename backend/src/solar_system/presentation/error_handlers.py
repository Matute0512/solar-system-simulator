from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from solar_system.domain.errors import EphemerisOutOfRangeError, NaiveDatetimeError
from solar_system.presentation.schemas import ErrorResponse

# One stable code per domain error. Add new errors here.
_ERROR_CODES: dict[type[Exception], str] = {
    EphemerisOutOfRangeError: "date_out_of_range",
    NaiveDatetimeError: "naive_datetime",
}


# The handler signature must accept a generic Exception (Starlette's contract);
# we look the code up by the concrete type of the error.
async def _handle_domain_error(request: Request, exc: Exception) -> JSONResponse:
    error_response = ErrorResponse(
        code=_ERROR_CODES[type(exc)],
        detail=str(exc),
    )
    return JSONResponse(content=error_response.model_dump(), status_code=422)


def register_error_handlers(app: FastAPI) -> None:
    for error_type in _ERROR_CODES:
        app.add_exception_handler(error_type, _handle_domain_error)
