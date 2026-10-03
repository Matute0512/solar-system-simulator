// Scene units per astronomical unit (ADR 0002). Override at build time with
// VITE_AU_TO_SCENE; the default keeps Neptune (~30 AU) within a workable range.
const DEFAULT_AU_TO_SCENE = 10;

export const AU_TO_SCENE = Number(import.meta.env.VITE_AU_TO_SCENE) || DEFAULT_AU_TO_SCENE;

export const POSITIONS_PATH = '/api/v1/positions';
