/* eslint new-cap: [2, {capIsNewExceptions: ["Given", "When", "Then"]}]*/

/**
 * Holds steps related to the homepage feature.
 * @module website/homepage
 */

import {When, Then} from 'cypress-cucumber-preprocessor/steps';


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
 * @param {number} year - the year to navigate to
 * @example
 * When I navigate to 2016 home page
 */
const navigateToSpecificYearHomepage = (year) => {
  cy.visit({url: '/website/' + year, method: 'GET'});
};
When(`I navigate to {string} home page`, navigateToSpecificYearHomepage);

/**
 * A step to view the given news item.
 * @param {string} itemTitle - the title of the news item
 * @example
 * When I click on "Launch" news item
 */
const viewNewsItem = (itemTitle) => {
  cy.get('[data-cy="' + itemTitle + '"]').click();
};
When(`I click on {string} news item`, viewNewsItem);

/**
 * A step to assert the current page contains a list of recent game scores.
 * @example
 * Then there is a list of recent game scores
 */
const assertListOfGameScores = () => {
  cy
      .get('[data-cy="games"]')
      .find('[data-cy="game"]')
      .its('length')
      .should('be.gte', 1);
};
Then(`there is a list of recent game scores`, assertListOfGameScores);

/**
 * A step to assert the current page contains a list of sponsors.
 * @example
 * Then there is a list of sponsors
 */
const assertListOfSponsors = () => {
  cy
      .get('.flickity-slider')
      .find('.sponsor-cell')
      .its('length')
      .should('be.gte', 1);
};
Then(`there is a list of sponsors`, assertListOfSponsors);

/**
 * A step to assert homepage has a list of news items.
 * @example
 * Then there is a list of news items
 */
const assertListOfNewsItems = () => {
  cy
      .get('.flickity-slider')
      .find('[data-cy="sponsor-cell"]')
      .its('length')
      .should('be.gte', 1);
};
Then(`there is a list of news items`, assertListOfNewsItems);


/**
 * Navigate through the list of sponsors.
 * @example
 * Then I can navigate through the list of sponsors
 */
const navigateSponsorsList = () => {
  cy.get('.next').click();
  cy.get('.previous').click();
};
Then(`I can navigate through the list of sponsors`, navigateSponsorsList);

/**
 * Assert that current page is a post about the launch of the website.
 * @example
 * Then I see details about website launch
 */
const assertLaunchNews = () => {
  cy.get('h4').contains('Launch');
};
Then(`I see details about website launch`, assertLaunchNews);
