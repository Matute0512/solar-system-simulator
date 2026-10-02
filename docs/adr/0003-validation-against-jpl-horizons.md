# ADR 0003: Validate computed positions against JPL Horizons

- **Status:** Accepted
- **Date:** 2026-10-01

## Context

A test that compares Skyfield output with Skyfield output proves nothing. We
need an independent oracle for the position calculations.

## Decision

- Reference vectors come from JPL Horizons via `astroquery jplhorizons`: center = Sun (body center, `500@10`), reference plane = ecliptic, geometric (no aberrations), units AU, epochs as TDB Julian dates.
- They are stored with their provenance in `backend/tests/fixtures/horizons_vectors.json`; the script that generates them lives in `backend/scripts/fetch_horizons_fixtures.py`.
- Test instants use the TDB time scale (`ts.tdb(jd=...)`) so they match Horizons exactly.
- The tolerance is 1e-6 AU (~150 km). A scratch experiment with the Earth at J2000 showed differences around 1e-8 AU against Horizons, so this leaves margin for DE421 vs. the ephemeris currently used by Horizons.

## Consequences

- Calculation tests are meaningful and tied to a public, citable source.
- Adding a body requires adding its reference vectors first (TDD).
- The fixture file is data, not code: it can be audited and extended without touching the tests.
