import {fileURLToPath, URL} from 'node:url'
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
// import { djangoVitePlugin } from 'django-vite-plugin'


// https://vitejs.dev/config/
export default defineConfig({
    base: "/static/",

    css: {
        preprocessorOptions: {
            scss: {
                includePaths: ['node_modules']
            }
        }
    },
    plugins: [
        vue(),
        // djangoVitePlugin([
        //     //{% '<app_name>/<path>/<to>/<css>/styles.css' %}
        //     './src/main.js',
        //     'home/css/style.css',
        // ])
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },

    },
    build: {

        manifest: true,
        outDir: "../assets", // fileURLtoPath
        rollupOptions: {
            input: {
                main: "./src/main.js",
            },
            output: {
                entryFileNames: `assets/[name].js`,
                chunkFileNames: `assets/[name].js`,
                assetFileNames: `assets/[name].[ext]`
            },


        },

    }
})
