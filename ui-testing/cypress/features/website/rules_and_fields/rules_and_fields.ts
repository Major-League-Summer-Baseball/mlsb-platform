import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';
import { getCurrentYear } from '../../global/helper';

/**
 * The URL for all the rules and fields page.
 * @private
 */
export const RULES_AND_FIELDS_PAGE = 'website/rulesAndFields/';

/**
 * A step to navigate to the rules and fields page.
 * @example
 * Given I navigate to the rules and fields page
 */
export const navigateToRulesAndFieldsPage = (): void => {
    cy.visit({ url: RULES_AND_FIELDS_PAGE + getCurrentYear(), method: 'GET' });
};
Given(`I navigate to the rules and fields page`, navigateToRulesAndFieldsPage);

/**
 * A step for clicking on the given tab
 * @param {string} tab - the tab to click
 * @example <caption> Click on the fields tab</caption>
 * When I click on "Fields" tab
 * @example <caption> Click on the rules tab</caption>
 * When I click on "Rules" tab
 */
export const clickOnTab = (tab: string): void => {
    cy.get('[data-cy="' + tab + 'Tab').click();
};
When(`I click on {string} tab`, clickOnTab);

/**
 * A step for asserting the rules were displayed
 * @example
 * Then I see information about the rules
 */
export const assertRulesInformation = (): void => {
    cy.get('li').contains('No Drinking on the Baseball');
};
Then(`I see information about the rules`, assertRulesInformation);

/**
 * A step for asserting the fields were displayed
 * @example
 * Then I see information about the fields
 */
export const assertFieldsInformation = (): void => {
    cy.get('p').contains('Waterloo Park');
};
Then(`I see information about the fields`, assertFieldsInformation);
