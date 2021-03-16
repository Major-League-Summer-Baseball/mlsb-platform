/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable @typescript-eslint/explicit-function-return-type */
/* eslint-disable no-unused-vars */

/**
 * Deals with the various
 * {@link https://on.cypress.io/plugins-guide|plugins}.
 * Currently uses the following plugins:
 * <ul>
 *  <li>{@link https://github.com/TheBrainFamily/cypress-cucumber-preprocessor|cucumber} </li>
 * </ul>
 * Additionally, the following environment variables:
 * <ul>
 *    <li> CYPRESS_baseUrl ->  the URL to the Möbius instance under test </li>
 * </ul>
 * @module global/plugins
 */
const webpack = require('@cypress/webpack-preprocessor');
const Oauth = require('oauth-1.0a');
const crypto = require('crypto');

/**
 * A cypress tasks the will sign a request.
 * The task name is different than this function name.
 * @param {Object} request - the request data
 * @param {SecretKeyPair} request.key - the oauth key
 * @param {string} request.url - the URL of the request
 * @param {Object} request.parameters - holds all the parameters of the request
 * @return {Object} - the signed request body
 * @example
 * cy.task('oauthSignature', {
 *   key: new SecretKeyPair(),
 *   url: 'http://localhost:8080/some_route',
 *   parameters: {some_parameter: 'hello'}
 * }).then((oauth) =>{
 *   // make the request with oauth as the body
 * })
 */
function signature(request) {
    const oauth = new Oauth({
        consumer: {
            key: request.key._key,
            secret: request.key._secret,
        },
        signature_method: 'HMAC-SHA1',
        hash_function(baseString, key) {
            return crypto.createHmac('sha1', key).update(baseString).digest('base64');
        },
    });
    const data = {
        url: request.url,
        method: 'POST',
        data: request.parameters,
    };
    return oauth.authorize(data, null);
}

module.exports = (on, config) => {
    // `on` is used to hook into various events Cypress emits
    // `config` is the resolved Cypress config
    const options = {
        webpackOptions: require('../../webpack.config.js'),
    };
    on('file:preprocessor', webpack(options));
    on('task', {
        oauthSignature({ key, url, parameters }) {
            return signature({ key: key, url: url, parameters: parameters });
        },
        log(message) {
            console.log(message);

            return '';
        },
        table(message) {
            console.table(message);

            return '';
        },
    });
    on('before:browser:launch', (browser = {}, launchOptions) => {
        if (browser.name === 'chrome') {
            launchOptions.args.push('--disable-dev-shm-usage');
            return launchOptions;
        }
    });
    config.env.PASSWORD = process.env.PASSWORD;
    config.env.ADMIN = process.env.ADMIN;
    return config;
};
