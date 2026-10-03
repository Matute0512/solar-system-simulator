import { defineConfig } from 'vitest/config';

// `defineConfig` from vitest/config lets one file configure Vite and Vitest.
export default defineConfig({
    server: {
        // In development the browser talks only to Vite, which forwards /api to the
        // backend. The browser sees one origin, so CORS is never needed (ADR 0007).
        proxy: {
            '/api': 'http://localhost:8000',
        },
    },
    test: {
        environment: 'node',
        include: ['tests/**/*.test.js'],
        // No tests exist yet at this stage; remove once the first one is added.
        passWithNoTests: true,
    },
});
