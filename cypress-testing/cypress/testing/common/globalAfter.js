/**
 * Holds a global steps and hooks.
 * @module global/steps
 */

/**
 * A hook that runs once after all tests.
 */
const globalAfter = () => {
  cy.wait(1000);
};

after(globalAfter);
