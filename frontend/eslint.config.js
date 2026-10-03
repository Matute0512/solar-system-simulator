import js from '@eslint/js';
import globals from 'globals';
import prettier from 'eslint-config-prettier';

export default [
    { ignores: ['dist/', 'node_modules/', 'coverage/'] },
    js.configs.recommended,
    {
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'module',
            globals: { ...globals.browser },
        },
        rules: {
            eqeqeq: 'error',
            'prefer-const': 'error',
            'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
        },
    },
    {
        // Tests and config files run in Node, not in the browser.
        files: ['tests/**/*.js', '*.config.js'],
        languageOptions: { globals: { ...globals.node } },
    },
    // Must be last: disables the rules that would conflict with Prettier.
    prettier,
];
