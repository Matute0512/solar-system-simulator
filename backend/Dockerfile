# Official uv image with Python 3.10 preinstalled (matches requires-python in pyproject.toml).
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

# - COMPILE_BYTECODE: precompile .pyc files, which speeds up container startup.
# - LINK_MODE=copy: avoids the hardlink warning and works across filesystems.
# - PYTHONUNBUFFERED: logs show up immediately in `docker logs`.
# - SOLAR_DATA_DIR: where the app looks for the ephemeris kernel (see config.py).
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    SOLAR_DATA_DIR=/app/data

# Layer 1: third-party dependencies only (cached unless uv.lock changes).
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-install-project --no-dev

# Layer 2: download the ephemeris kernel at build time, so the container needs
# no network at runtime and the app can fail fast if the file is missing.
# It is its own layer: code changes do not trigger a new download.
# Keep the file name in sync with _KERNEL_FILE in skyfield_provider.py.
RUN mkdir -p /app/data \
    && /app/.venv/bin/python -c \
    "from skyfield.api import Loader; Loader('/app/data', verbose=False)('de440s.bsp')"

# Layer 3: our source code (rebuilt on every change, but fast).
COPY src ./src
RUN uv sync --frozen --no-dev

# Put the virtualenv first in PATH so we can call `uvicorn` directly.
ENV PATH="/app/.venv/bin:$PATH"

# Security: never run as root. The kernel stays root-owned and read-only for
# appuser (least privilege: the app cannot modify its own reference data).
RUN useradd --create-home appuser
USER appuser

# Documentation only: it does not publish the port (compose does that).
EXPOSE 8000

# 0.0.0.0 is mandatory: with 127.0.0.1 the app would be unreachable from outside.
CMD ["uvicorn", "solar_system.presentation.main:app", "--host", "0.0.0.0", "--port", "8000"]