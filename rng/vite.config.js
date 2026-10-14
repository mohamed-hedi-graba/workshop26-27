import { defineConfig } from 'vite';

export default defineConfig({
    root: 'public',
    build: {
        outDir: '../dist'
    },
    server: {
        proxy: {
            '/api': 'http://localhost:3000'
        }
    }
});