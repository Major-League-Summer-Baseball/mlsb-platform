// @ts-nocheck

// eslint-disable-next-line @typescript-eslint/no-var-requires
const path = require('path');
const NodePolyfillPlugin = require('node-polyfill-webpack-plugin')

module.exports = {
    mode: 'development',
    // make sure the source maps work
    devtool: 'eval-source-map',
    plugins: [
        new NodePolyfillPlugin()
    ],
    resolve: {
        extensions: ['.ts', '.tsx', '.js'],
        alias: {
            '@Interfaces': path.resolve(__dirname, 'cypress/interfaces'),
            '@Pages': path.resolve(__dirname, 'cypress/pages'),
            '@Support': path.resolve(__dirname, 'cypress/support'),
            '@Common': path.resolve(__dirname, 'cypress/features/common'),
        },
        fallback: {
            path: require.resolve("path-browserify"),
            fs: false,
            child_process: false,
            readline: false,
        }
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                exclude: [/node_modules/],
                use: [
                    {
                        loader: 'ts-loader',
                        options: {
                            // skip typechecking for speed
                            transpileOnly: true,
                        },
                    },
                ],
            },
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                },
            },
            {
                test: /\.feature$/,
                use: [
                    {
                        loader: 'cypress-cucumber-preprocessor/loader',
                    },
                ],
            },
            {
                test: /\.features$/,
                use: [
                    {
                        loader: 'cypress-cucumber-preprocessor/lib/featuresLoader',
                    },
                ],
            },
        ],
    },
};
