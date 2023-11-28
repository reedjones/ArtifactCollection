/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {
    chainWebpack: (config) => {
        config.module
            .rule("mjs")
            .test(/\.mjs$/)
            .type("javascript/auto")
            .include.add(/node_modules/)
            .end();
    },
};
