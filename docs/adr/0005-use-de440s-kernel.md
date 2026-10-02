# ADR 0005: Use the DE440s ephemeris kernel

- **Status:** Accepted
- **Date:** 2026-10-02

## Context

Against the JPL Horizons reference vectors, the DE421 kernel showed maximum
differences of 3.7e-6 AU (Neptune), 2.5e-6 AU (Uranus) and 4.1e-7 AU
(Jupiter). The DE440 kernel matched them to about 1e-13 AU. Horizons uses a
recent planetary ephemeris, so comparing it with an older kernel mixes the
error of our code with the error of the kernel.

## Decision

Use `de440s.bsp` (about 32 MB, covering 1849 to 2150): same solution as
DE440 over a shorter span, with a much smaller download.

## Consequences

- The oracle and the implementation use the same ephemeris generation.
- The supported range is 1849 to 2150 (it was ~1900 to 2050 with DE421).
- CI and Docker must cache or bundle the kernel (cache key tied to its name).
