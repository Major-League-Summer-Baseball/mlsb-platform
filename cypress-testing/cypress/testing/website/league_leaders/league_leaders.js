/* eslint new-cap: [2, {capIsNewExceptions: ["Given", "When", "Then"]}]*/

/**
 * Holds steps related to the league leaders feature.
 * @module website/league_leaders
 */

import {Given, When, Then} from 'cypress-cucumber-preprocessor/steps';
import {getCurrentYear} from '../../common/helper.js';

/**
 * The URL for the current season leaders page.
 * @private
 */
const LEADERS_PAGE = 'website/leaders/';

/**
 * The URL for the all-time leaders page.
 * @private
 */
const ALL_TIME_LEADERS_PAGE = LEADERS_PAGE + 'alltime/';

/**
 * A function to assert the given list is in descending order
 * @param {string} selector- a selector for the given list of elements
 * @private
 */
const assertDescendingOrder = (selector) => {
  let previousValue = Number.MAX_SAFE_INTEGER;
  let currentValue;
  cy.get(selector).each(($el, index, $list) => {
    currentValue = parseInt($el.text());
    expect(previousValue).to.be.at.least(currentValue);
    previousValue = currentValue;
  });
};

/**
 * A step to navigate to league leaders page.
 * @example
 * When I navigate to league leaders page
 */
const navigateToLeagueLeaderPage = () => {
  cy.visit({url: LEADERS_PAGE + getCurrentYear(), method: 'GET'});
};
When(`I navigate to the league leaders page`, navigateToLeagueLeaderPage);

/**
 * A step to navigate to all-time leader page.
 * @example
 * When I navigate to the all-time leader page
 */
const navigateToAllTimeLeaderPage = () => {
  cy.visit({url: ALL_TIME_LEADERS_PAGE + getCurrentYear(), method: 'GET'});
};
When(`I navigate to the all-time leaders page`, navigateToAllTimeLeaderPage);

/**
 * A step to assert that the homeruns are in descending order.
 * @example
 * Then there is a descending ordered list of players for homeruns
 */
const assertHomerunsHasDescendingOrder = () => {
  assertDescendingOrder('[data-cy="currentSeasonHomeruns"]');
};
Then(`there is a descending ordered list of players for homeruns`,
  assertHomerunsHasDescendingOrder);

/**
 * A step to assert that the singles are in descending order.
 * @example
 * Then there is a descending ordered list of players for singles
 */
const assertSinglesHasDescendingOrder = () => {
  assertDescendingOrder('[data-cy="currentSeasonSingles"]');
};
Then(`there is a descending ordered list of players for singles`,
  assertSinglesHasDescendingOrder);

/**
 * A step to assert that the homeruns are in descending order.
 * @example
 * Then there is a descending ordered list of players for all-time homeruns
 */
const assertAllTimeHomerunsHasDescendingOrder = () => {
  assertDescendingOrder('[data-cy="allTimeCareerHomeruns"]');
  assertDescendingOrder('[data-cy="allTimeSingleSeasonHomeruns"]');
};
Then(`there is a descending ordered list of players for all-time homeruns`,
  assertAllTimeHomerunsHasDescendingOrder);

/**
 * A step to assert that the singles are in descending order.
 * @example
 * Then there is a descending ordered list of players for all-time singles
 */
const assertAllTimeSinglesHasDescendingOrder = () => {
  assertDescendingOrder('[data-cy="allTimeSingleSeasonSingles"]');
  assertDescendingOrder('[data-cy="allTimeCareerSingles"]');
};
Then(`there is a descending ordered list of players for all-time singles`,
  assertAllTimeSinglesHasDescendingOrder);

