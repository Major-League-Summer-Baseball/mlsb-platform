import { defineConfig } from "cypress";
import * as webpack from "@cypress/webpack-preprocessor";
import { addCucumberPreprocessorPlugin } from "@badeball/cypress-cucumber-preprocessor";

async function setupNodeEvents(
  on: Cypress.PluginEvents,
  config: Cypress.PluginConfigOptions
): Promise<Cypress.PluginConfigOptions> {
  await addCucumberPreprocessorPlugin(on, config);

  on(
    "file:preprocessor",
    webpack({
      webpackOptions: {
        resolve: {
          extensions: [".ts", ".js"],
          fallback: {
            "path": require.resolve("path-browserify")
          }
        },
        module: {
          rules: [
            {
              test: /\.ts$/,
              exclude: [/node_modules/],
              use: [
                {
                  loader: "ts-loader",
                },
              ],
            },
            {
              test: /\.feature$/,
              use: [
                {
                  loader: "@badeball/cypress-cucumber-preprocessor/webpack",
                  options: config,
                },
              ],
            },
          ],
        },
      },
    })
  );
  // Make sure to return the config object as it might have been modified by the plugin.
  config.env.PASSWORD = process.env.PASSWORD;
  config.env.ADMIN = process.env.ADMIN;
  return config;
}

export default defineConfig({
  e2e: {
    specPattern: "**/*.feature",
    baseUrl: "http://localhost:5000/",
    supportFile: "cypress/support/e2e.ts",
    setupNodeEvents,
    video: true,
    retries: 3
  },
});
