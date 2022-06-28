import { When, Then } from '@badeball/cypress-cucumber-preprocessor';
import { randomName } from '../../global/helper';
import "../../global/login";

/**
 * A step to navigate to the login page.
 * @example
 * When I navigate to the login page
 */
export const navigateToLoginPage = (): void => {
    cy.visit({ url: 'admin/login', method: 'GET' });
};
When(`I navigate to the login page`, navigateToLoginPage);

/**
 * A step to enter invalid credentials.
 * @example
 * When I enter invalid credentials
 */
export const enterInvalidCredentials = (): void => {
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
export const assertLoginFailingMessage = (): void => {
    cy.get('[data-cy=errors]');
};
Then(`I see a login error message`, assertLoginFailingMessage);

/**
 * Assert that logged in as the given role and that cookies have been set.
 * @param {string} role - the expected role of the logged in user
 * @example
 * Then I am logged in with the role "Student"
 */
export const assertSuccessfullyLoggedIn = (): void => {
    cy.get('[data-cy=homepage]').should('exist');
};
Then(`I am logged in`, assertSuccessfullyLoggedIn);
