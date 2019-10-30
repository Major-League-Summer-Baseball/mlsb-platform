/* eslint new-cap: [2, {capIsNewExceptions: ["Given"]}]*/

/**
 * Holds a global steps and hooks.
 * @module global/steps
 */

/**
 * A global step that creates a random user for the given roll and then
 * logins by making a POST request.
 * @param {string} role - the role of the user to log in as.
 * @example
 * Given I am logged in as administrator
 */
const login = () => {
  cy.login();
};
Given(`I am logged in as an admin`, login);
