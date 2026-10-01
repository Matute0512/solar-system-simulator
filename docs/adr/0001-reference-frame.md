# ADR 0001: Reference frame, origin and units of the positions API

- **Status:** Accepted
- **Date:** 2026-10-01

## Context

Skyfield returns positions int the ICRS frame by default, whose base plane is the celestial equator. Planets orbit close to the ecliptic, so in ICRS the orbit of the Earth has a large z component (-0.39 AU at J2000, wich matches the 23.44° obliquity). Rendering those values directly would tilt the whole Solar System in the scene.

Skyfield also offers two ways of computing a position: `observe()`, which
applies light-time correction (apparent position), and vector subtraction
(`target - observer`), which gives the geometric position. We measured a
difference of ~8.5e-5 AU between both on the Earth at J2000 (≈ 427 s of
orbital motion).

## Decision

The API returns positions that are:

- **Heliocentric:** origin at the center of the Sun.
- **Ecliptic J2000:** `skyfield.framelib.ecliptic_J2000_frame` (not `ecliptic_frame`, which tracks the ecliptic of date).
- **Geometric**: computed with `(body - sun).at(t)`, with no light-time or aberration correction.
- **In astronomical units (AU)**.

## Consequences

- Planets have z ≈ 0, which is the natural frame for a Solar System view.
- Results are deterministic and reproducible for a given instant, and they can be validated against JPL Horizons vector tables (see ADR 0003).
- Any client other than the 3D scene receives standard astronomical data.
- Apparent (light-time corrected) positions are not available. This is acceptable: the simulator shows where bodies are, not how they are observed from Earth.
