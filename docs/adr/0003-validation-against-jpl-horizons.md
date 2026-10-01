# ADR 0003: Validate computed positions against JPL Horizons

- **Status:** Accepted
- **Date:** 2026-10-01

## Context

A test that compares Skyfield output with Skyfield output proves nothing. We
need an independent oracle for the position calculations.

## Decision

- Reference vectors come from the JPL Horizons *Vector Table*: center = Sun (body center), reference plane = ecliptic, epoch J2000, default units (km).
- They are stored with their provenance in `backend/tests/fixtures/horizons_vectors.json` and converted to AU inside the tests (1 AU = 149 597 870.7 km).
- Test instants use the TDB time scale (`ts.tdb(jd=...)`) so they match Horizons exactly.
- The initial tolerance is 1e-5 AU (~1500 km) and will be tightened once the real difference is measured. DE421 (used here) and the ephemeris currently used by Horizons differ slightly.

## Consequences

- Calculation tests are meaningful and tied to a public, citable source.
- Adding a body requires adding its reference vectors first (TDD).
- The fixture file is data, not code: it can be audited and extended without touching the tests.
