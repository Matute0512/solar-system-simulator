# ADR 0006: Bundle the kernel in the image and fail fast at startup

- **Status:** Accepted
- **Date:** 2026-10-02

## Context

The API needs the DE440s kernel (ADR 0005). It can reach the container by
downloading it at build time, downloading it at startup, or mounting a
volume. A service that cannot load its ephemeris is useless, but it would
still answer `/health` if it started anyway.

## Decision

- The kernel is downloaded while building the Docker image, in its own layer.
- The directory is owned by root and read-only for the application user.
- The application loads the provider at startup (FastAPI lifespan) and refuses to start if that fails.

## Consequences

- `docker compose up` works on any machine, with no network at runtime.
- A broken deployment is detected at startup by the orchestrator, not by users.
- The image grows by about 32 MB, and the kernel name must be kept in sync between the Dockerfile and `skyfield_provider.py`.
