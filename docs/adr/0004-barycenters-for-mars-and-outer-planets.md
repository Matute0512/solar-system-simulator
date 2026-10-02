# ADR 0004: Mars and the outer planets are reported as system barycenters

- **Status:** Accepted
- **Date:** 2026-10-02

## Context

The DE421 kernel provides body centers only for the Sun, Mercury, Venus and
the Earth. For Mars, Jupiter, Saturn, Uranus and Neptune it only provides the
barycenter of each planetary system. Comparing Horizons body centers with
barycenters at J2000 gives differences of about 4e-7 AU (Jupiter), 2e-6 AU
(Saturn), 2.4e-6 AU (Uranus) and 7e-7 AU (Neptune), i.e. up to ~350 km.
For the Earth the offset to the Earth-Moon barycenter is ~4800 km, which is
why the Earth uses its body center.

## Decision

- Mars and the outer planets are reported as system barycenters.
- The Earth is reported as its body center.
- Test fixtures for those bodies use the Horizons barycenter IDs (4 to 8).

## Consequences

- The error is irrelevant at Solar System scale (< 3e-6 AU).
- The domain and the API still say "Jupiter", not "Jupiter barycenter";
the distinction lives in the adapter and in this document.
- Adding planetary moons later requires revisiting this decision.
