// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
import '@testing-library/cypress/add-commands';

/**
 * A custom command that logouts as the admin.
 * @example
 * cy.logout();
 */
 export const logout = (): void => {
    cy.visit({ url: '/admin/logout', method: 'GET' });
};
Cypress.Commands.add('logout', logout);

/**
 * A custom command logins in as the admin.
 * @example
 * cy.login();
 */
export const login = (): void => {
    logout();
    cy.visit({ url: '/admin/login', method: 'GET' });
    cy.get('[data-cy=username]').type(Cypress.env('ADMIN'));
    cy.get('[data-cy=password]').type(Cypress.env('PASSWORD'));
    cy.get('[data-cy=submit]').click();
};
Cypress.Commands.add('login', login);