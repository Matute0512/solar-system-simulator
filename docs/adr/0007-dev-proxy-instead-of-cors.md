# ADR 0007: Use a development proxy instead of CORS

- **Status:** Accepted
- **Date:** 2026-10-02

## Context

The frontend runs on the Vite dev server (port 5173) and the API on port
8000. Browsers block cross-origin requests unless the API explicitly allows
them (CORS).

## Decision

- In development, Vite proxies `/api` to the backend, so the browser only talks to one origin.
- In production-like setups, a reverse proxy (nginx in Docker Compose) will serve the frontend and forward `/api` the same way.
- The backend does not enable CORS.

## Consequences

- No CORS configuration to maintain, and the API is not open to other origins.
- The frontend always calls relative paths (`/api/v1/positions`).
- Opening the built frontend without the proxy will not reach the API.
