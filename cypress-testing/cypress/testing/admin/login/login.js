/* eslint new-cap: [2, {capIsNewExceptions: ["Given", "When", "Then"]}]*/

/**
 * Holds steps related to the login feature.
 * @module admin/login
 */

import {Given, When, Then} from 'cypress-cucumber-preprocessor/steps';
import {randomName} from '../../common/helper.js';

/**
 * A step to navigate to the login page.
 * @example
 * When I navigate to the login page
 */
const navigateToLoginPage = () => {
  cy.visit({url: 'admin/login', method: 'GET'});
};
When(`I navigate to the login page`, navigateToLoginPage);

/**
 * A step to enter invalid credentials.
 * @example
 * When I enter invalid credentials
 */
const enterInvalidCredentials = () => {
  cy.get('[data-cy=username]').type(randomName());
  cy.get('[data-cy=password]').type(randomName());
  cy.get('[data-cy=submit]').click();
};
When(`I enter invalid credentials`, enterInvalidCredentials);


/**
 * Assert that was not logged in and see that one was unabel to login.
 * @example
 * Then I see a login error message
 */
const assertLoginFailingMessage = () => {
  cy.get('[data-cy=errors]');
};
Then(`I see a login error message`, assertLoginFailingMessage);

/**
 * Assert that logged in as the given role and that cookies have been set.
 * @param {string} role - the expected role of the logged in user
 * @example
 * Then I am logged in with the role "Student"
 */
const assertSuccessfullyLoggedIn = () => {
  cy.get('[data-cy=homepage]').should('exist');
};
Then(`I am logged in`, assertSuccessfullyLoggedIn);
