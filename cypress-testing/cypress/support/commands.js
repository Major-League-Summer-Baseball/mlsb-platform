/**
 * Some custom commands for mobius. See
 * {@link https://docs.cypress.io/api/cypress-api/custom-commands.html | custom commands}
 * for more details on creating custom commands and
 * over riding default commands.
 * Some best practices to follow:
 * <ul>
 *    <li> DO NOT make everything a custom command</li>
 *    <li> DO NOT overcomplicate things</li>
 *    <li> DO NOT do too much in a single command</li>
 *    <li> DO skip the UI as much as possible </li>
 * </ul>
 * @module support/commands
 */


/**
 * A custom command that logouts as the admin.
 * @example
 * cy.logout();
 */
const logout = () => {
  cy.visit({url: '/admin/logout', method: 'GET'});
};
Cypress.Commands.add('logout', logout);

/**
 * A custom command logins in as the admin.
 * @example
 * cy.login();
 */
const login = () => {
  logout();
  cy.visit({url: '/admin/login', method: 'GET'});
  cy.get('[data-cy=username]').type(Cypress.env('ADMIN'));
  cy.get('[data-cy=password]').type(Cypress.env('PASSWORD'));
  cy.get('[data-cy=submit]').click();
};
Cypress.Commands.add('login', login);
