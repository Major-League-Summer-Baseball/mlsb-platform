/**
 * Holds a global steps and hooks.
 * @module global/steps
 */

/**
 * A hook that runs once before all tests.
 */
const globalHook = () => {
  cy.log(
      `This will run once before all tests,
      you can use this to for example start up your server,
      if that's your thing`
  );
};

before(globalHook);
