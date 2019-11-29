/**
 * Deals with the various
 * {@link https://on.cypress.io/plugins-guide|plugins}.
 * Currently uses the following plugins:
 * <ul>
 *  <li>{@link https://github.com/TheBrainFamily/cypress-cucumber-preprocessor|cucumber} </li>
 * </ul>
 * Additionally, the following environment variables:
 * <ul>
 *    <li> ADMIN -> the admin username used for admin console</li>
 *    <li> PASSWORD -> the admin password used for admin console</li>
 * </ul>
 * @module global/plugins
 */
const cucumber = require('cypress-cucumber-preprocessor').default;


module.exports = (on, config) => {
  // `on` is used to hook into various events Cypress emits
  // `config` is the resolved Cypress config
  on('file:preprocessor', cucumber());
  config.env.PASSWORD = process.env.PASSWORD;
  config.env.ADMIN = process.env.ADMIN;
  return config;
};
