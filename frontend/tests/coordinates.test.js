import { describe, expect, it } from 'vitest';
import { AU_TO_SCENE } from '../src/config.js';
import { eclipticToScene } from '../src/adapters/coordinates.js';

// toBeCloseTo is used instead of toEqual because -y can produce -0, and
// Vitest treats 0 and -0 as different values.
function expectVectorCloseTo(actual, expected) {
    expect(actual.x).toBeCloseTo(expected.x, 9);
    expect(actual.y).toBeCloseTo(expected.y, 9);
    expect(actual.z).toBeCloseTo(expected.z, 9);
}

const cross = (a, b) => ({
    x: a.y * b.z - a.z * b.y,
    y: a.z * b.x - a.x * b.z,
    z: a.x * b.y - a.y * b.x,
});

const X = { x: 1, y: 0, z: 0 };
const Y = { x: 0, y: 1, z: 0 };
const Z = { x: 0, y: 0, z: 1 };

describe('eclipticToScene', () => {
    it('maps the ecliptic unit vectors to the Three.js axes', () => {
        expectVectorCloseTo(eclipticToScene(X, 1), { x: 1, y: 0, z: 0 });
        expectVectorCloseTo(eclipticToScene(Y, 1), { x: 0, y: 0, z: -1 });
        // North of the ecliptic (Z) points up in the scene (Y).
        expectVectorCloseTo(eclipticToScene(Z, 1), { x: 0, y: 1, z: 0 });
    });

    it('preserves handedness: mapped X cross mapped Y equals mapped Z', () => {
        const mappedX = eclipticToScene(X, 1);
        const mappedY = eclipticToScene(Y, 1);

        expectVectorCloseTo(cross(mappedX, mappedY), eclipticToScene(Z, 1));
    });

    it('multiplies every component by the scale', () => {
        expectVectorCloseTo(eclipticToScene({ x: 1, y: 2, z: 3 }, 10), {
            x: 10,
            y: 30,
            z: -20,
        });
    });

    it('uses the configured scale by default', () => {
        expect(eclipticToScene(X).x).toBeCloseTo(AU_TO_SCENE, 9);
    });

    it('maps the Earth at J2000 as returned by the API', () => {
        // Values from the documented API example (Horizons reference, ADR 0003).
        const earth = { x: -0.177135, y: 0.967242, z: -0.000004 };

        expectVectorCloseTo(eclipticToScene(earth, 1), {
            x: -0.177135,
            y: -0.000004,
            z: -0.967242,
        });
    });
});
