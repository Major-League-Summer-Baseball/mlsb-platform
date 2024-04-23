import { Given } from "@badeball/cypress-cucumber-preprocessor";;

/**
 * Navigate to the given convenor page
 * @param category the page category to navigate to
 */
export const convenor_navigate = (category: string): void => {
    cy.visit(`/convenor/${category}`);
};
Given(`I navigate to the {string} page`, convenor_navigate);
