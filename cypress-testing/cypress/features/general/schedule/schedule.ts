import { Given, Then } from 'cypress-cucumber-preprocessor/steps';
import { getCurrentYear } from '@Common/helper';

/**
 * The URL for the league schedule.
 * @private
 * @TODO: fix this route and steps so more dynamic
 *  navigates to the proper schedule for a given league
 */
const SCHEDULE_PAGE = 'website/schedule/1/';

/**
 * A step to navigate to the schedule page.
 * @example
 * Given I am on the the schedule page
 */
export const navigateToSchedulePage = (): void => {
    cy.visit({ url: SCHEDULE_PAGE + getCurrentYear(), method: 'GET' });
};
Given(`I am on the the schedule page`, navigateToSchedulePage);

/**
 * A step to assert the schedule page properly displayed
 * @example
 * Then I see the schedule for the league
 */
export const assertScheduleDisplayed = (): void => {
    cy.get('td').contains('WP1');
    cy.get('th').contains('Score');
};
Then(`I see the schedule for the league`, assertScheduleDisplayed);
