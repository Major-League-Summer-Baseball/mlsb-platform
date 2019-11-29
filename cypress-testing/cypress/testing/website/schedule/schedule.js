/* eslint new-cap: [2, {capIsNewExceptions: ["Given", "When", "Then"]}]*/

/**
 * Holds steps related to the schedule feature.
 * @module website/schedule
 */

import {Given, Then} from 'cypress-cucumber-preprocessor/steps';
import {getCurrentYear} from '../../common/helper.js';

/**
 * The URL for the league schedule.
 * @private
 */
const SCHEDULE_PAGE = 'website/schedule/';


/**
 * A step to navigate to the schedule page.
 * @example
 * Given I am on the the schedule page
 */
const navigateToSchedulePage = () => {
  cy.visit({url: SCHEDULE_PAGE + getCurrentYear(), method: 'GET'});
};
Given(`I am on the the schedule page`, navigateToSchedulePage);

/**
 * A step to assert the schedule page properly displayed
 * @example
 * Then I see the schedule for the league
 */
const assertScheduleDisplayed = () => {
  cy.get('td').contains('WP1');
  cy.get('th').contains('Score');
};
Then(`I see the schedule for the league`, assertScheduleDisplayed);
