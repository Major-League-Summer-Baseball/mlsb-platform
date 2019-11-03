/* eslint new-cap: [2, {capIsNewExceptions: ["Given", "When", "Then"]}]*/

/**
 * Holds steps related to the homepage feature.
 * @module homepage/events
 */

import {Given, When, Then} from 'cypress-cucumber-preprocessor/steps';



/**
 * A step to navigate to system homepage.
 * @example
 * When I navigate to the home page
 */
const navigateToHomepage = () => {
  cy.visit({url: '', method: 'GET'});
};
When(`I navigate to the home page`, navigateToHomepage);

/**
 * A step to navigate to system homepage for a specific year.
 * @example
 * When I navigate to 2016 home page
 */
const navigateToSpecificYearHomepage = (year) => {
  cy.visit({url: '/website/' + year, method: 'GET'});
};
When(`I navigate to {string} home page`, navigateToSpecificYearHomepage);


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
