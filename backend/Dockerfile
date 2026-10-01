# Official uv image with Python 3.10 preinstalled (matches requires-python in pyproject.toml).
# "slim" keeps the final image small.
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

# All following commands run from here.
WORKDIR /app

# - COMPILE_BYTECODE: precompile .pyc files, which speeds up container startup.
# - LINK_MODE=copy: avoids the hardlink warning and works across filesystems.
# - PYTHONUNBUFFERED: logs show up immediately in `docker logs`.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# Layer 1: install ONLY third-party dependencies.
# These files change rarely, so Docker caches this expensive layer.
# --frozen: use uv.lock exactly as committed (reproducible builds).
# --no-install-project: skip our own package (its source is not copied yet).
# --no-dev: test and lint tools do not belong in a production image.
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-install-project --no-dev

# Layer 2: copy the source code and install our package.
# This layer is rebuilt on every code change, but it is fast.
COPY src ./src
RUN uv sync --frozen --no-dev

# Put the virtualenv first in PATH so we can call `uvicorn` directly.
ENV PATH="/app/.venv/bin:$PATH"

# Security: never run the app as root inside a container.
RUN useradd --create-home appuser
USER appuser

# Documentation only: it does not publish the port (compose does that).
EXPOSE 8000

# 0.0.0.0 is mandatory: with 127.0.0.1 the app would only be reachable
# from INSIDE the container, never from your browser.
CMD ["uvicorn", "solar_system.presentation.main:app", "--host", "0.0.0.0", "--port", "8000"]