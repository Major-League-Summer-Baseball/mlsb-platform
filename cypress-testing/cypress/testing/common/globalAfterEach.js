/**
 * Holds a global steps and hooks.
 * @module global/steps
 */

/**
 * A hook that runs once after each test.
 */
const globalAfterEach = () => {
  cy.visit({url: 'admin/logout', method: 'GET'});
};

afterEach(globalAfterEach);
