import { AU_TO_SCENE } from '../config.js';

/**
 * @typedef {{ x: number, y: number, z: number}} Vec3
 */

/**
 * Converts a position from the API frame (heliocentric, ecliptic J2000, Z up,
 * in AU) to scene coordinates (Three.js: Y up, right-handed). See ADR 0002.
 *
 * @param {Vec3} position Position in AU, as returned by the API.
 * @param {number} [scale=AU_TO_SCENE] Scene units per AU.
 * @returns {Vec3} Position in scene units.
 */
export function eclipticToScene(position, scale = AU_TO_SCENE) {
    return {
        x: position.x * scale,
        y: position.z * scale,
        z: -position.y * scale,
    };
}
