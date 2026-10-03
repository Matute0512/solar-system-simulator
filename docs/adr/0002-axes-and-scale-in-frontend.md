# ADR 0002: Axis mapping and scene scale belong to the frontend

- **Status:** Accepted
- **Date:** 2026-10-01

## Context

The API returns ecliptic coordinates (Z axis pointing north of the ecliptic).
Three.js uses a Y-up convention, and real distances in AU are unusable as scene
units (planets would be invisible dots).

Both the axis convention and the scale are rendering concerns, not
astronomical ones.

## Decision

- The backend never knows how the data is rendered. It documents its frame (ADR 0001) and nothing else.
- The frontend has a single adapter module that maps API coordinates to scene coordinates (axis remapping preserving handedness).
- The AU-to-scene-unit factor is a configurable constant of the frontend.
- The mapping is (x, y, z) → (x, z, −y): ecliptic north (Z) becomes the vertical axis (Y) and the determinant stays +1, so handedness is preserved. The scale is linear (no compression of distances).

## Consequences

- The API stays reusable for other clients (Python scripts, Unity, notebooks).
- Backend tests compare against standard references with no axis tricks.
- Changing the visual style (scale, axes) never requires a backend deployment.
- The adapter must be unit tested in the frontend (Milestone 3).
