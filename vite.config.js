import {fileURLToPath, URL} from 'node:url';

const {resolve} = require('path');

import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig(() => {

    return {
        root: resolve('./assets'),
        base: "/static/",
        outDir: '../static/dist',
        plugins: [vue()],
        resolve: {
            alias: {
                '@': fileURLToPath(new URL('./assets/src', import.meta.url))
            },
            extensions: ['.js', '.json'],
        },
        rollupOptions: {
            assetsDir: '',
            manifest: true,
            emptyOutDir: true,


            input: {
              main: resolve('./assets/src/main.js')

            },
        },
    };
});
