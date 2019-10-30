/* eslint new-cap: [2, {capIsNewExceptions: ["Given", "When", "Then"]}]*/

/**
 * Holds steps related to the login feature.
 * @module website/events
 */

import {Given, When, Then} from 'cypress-cucumber-preprocessor/steps';


/**
 * A step to navigate to the events page.
 * @example
 * Given I navigate to the events page
 */
const navigateToEventsPage = () => {
  cy.visit({url: 'website/event/2016', method: 'GET'});
};
Given(`I navigate to the events page`, navigateToEventsPage);

/**
 * A step to view a given event.
 * @param {string} event - the name of event to view
 * @example
 * When viewing the event "Mystery Bus"
 */
const viewGivenEvent = (event) => {
  cy.get('a').contains(event).click();
};
When(`viewing the event {string}`, viewGivenEvent);


/**
 * A step to assert the event contains the given details.
 * @param {string} expectedDetails - the expected details of the event
 * @example
 * Then I see details relating to "school buses"
 */
const assertEventDetails = (expectedDetails) => {
  cy.get('p').contains(expectedDetails).should('be.visible');
};
Then(`I see details relating to {string}`, assertEventDetails);
