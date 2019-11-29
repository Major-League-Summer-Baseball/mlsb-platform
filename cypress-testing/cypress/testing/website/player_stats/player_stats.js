/* eslint new-cap: [2, {capIsNewExceptions: ["Given", "When", "Then"]}]*/

/**
 * Holds steps related to the player stats feature.
 * @module website/player_stats
 */

import {Given, When, Then} from 'cypress-cucumber-preprocessor/steps';
import {getCurrentYear} from '../../common/helper.js';

/**
 * The URL for all the player and their statistics.
 * @private
 */
const PLAYER_STATS_PAGE = 'website/stats/';

/**
 * A function to check whether the given name is before the other name
 * @param {string} nameOne - the name that is expected to be before the other
 * @param {string} nameTwo - the name that is expected to be after the other
 * @return {boolean} true if nameOne before nameTwo otherwise false
 */
function nameBefore(nameOne, nameTwo) {
  return (nameOne.localeCompare(nameTwo) <= 0) ? true: false;
}

/**
 * A function to check whether the given number is before the other number
 * @param {string} numberOne -
 *    the number that is expected to be before the other
 * @param {string} numberTwo -
 *    the number that is expected to be after the other
 * @return {boolean} true if numberOne before numberTwo otherwise false
 */
function numberBefore(numberOne, numberTwo) {
  if (typeof numberOne === 'string' || numberOne instanceof String){
    numberOne = parseInt(numberOne.trim());
  }
  if (typeof numberTwo === 'string' || numberTwo instanceof String){
    numberTwo = parseInt(numberTwo.trim());
  }
  return (numberOne <= numberTwo) ? true : false;
}

/**
 * A step to navigate to the player stats page.
 * @example
 * Given I am on the player stats page
 */
const navigateToPlayerStatsPage = () => {
  cy.visit({url: PLAYER_STATS_PAGE + getCurrentYear(), method: 'GET'});
};
Given(`I am on the player stats page`, navigateToPlayerStatsPage);

/**
 * A step for sorting by the given column heading
 * @param {string} heading - the heading to sort by
 * @example <caption> Sort by special singles</caption>
 * When I sort by "ss"
 * @example <caption> Sort by player name</caption>
 * When I sort by "name"
 */
const sortByHeading = (heading) => {
  cy.get('[data-cy="' + heading + 'Heading"]').click();
  cy
      .get('[data-cy="' + heading + 'Heading"]')
      .should('have.class', 'sorting_asc');
};
When(`I sort by {string}`, sortByHeading);

/**
 * A step for clicking on some player.
 * @example
 * When I click on some player name
 */
const clickOnPlayer = () => {
  cy.get('[data-cy="nameCell"]').first().click();
};
When(`I click on some player name`, clickOnPlayer);

/**
 * A step for sorting by the given column heading
 * @param {string} name - the name to search for
 * @example <caption>Search for player named Captain</caption>
 * When I search for "Captain"
 */
const searchPlayers = (name) => {
  cy.get('input[type="search"]').type(name);
};
When(`I search for {string}`, searchPlayers);

/**
 * A step to just assert that the player stats are shown properly.
 * @example
 * Then I see their career stats
 */
const assertIndividualPlayerStats = () => {
  cy.get('[data-cy="abCell"]').each(($el, index, $list) => {
    expect(parseFloat($el.text().trim())).to.be.a('number');
  });
};
Then(`I see their career stats`, assertIndividualPlayerStats);

/**
 * A step to assert the player stats are sorted by the given heading
 * @param {string} typeOfSort - whether it is numerically or alphabeticalls
 * @param {string} heading - the heading that players should be sorted by
 * @example <caption> Players sorted by name</caption?
 * Then the players are sorted "alphabetically" by "name"
 * @example <caption> Players sorted by homeruns</caption?
 * Then the players are sorted "numerically" by "hr"
 */
const assertSortedByHeading = (typeOfSort, heading) => {
  const compareFunction = (typeOfSort === 'alphabetically')
      ? nameBefore : numberBefore;
  let previousValue = (typeOfSort === 'alphabetically')
      ? '' : 0;
  let currentValue;
  cy.log(compareFunction);
  cy.get('[data-cy="' + heading + 'Cell"]').each(($el, index, $list) => {
    currentValue = $el.text();
    expect(compareFunction(previousValue, currentValue)).to.be.true;
    previousValue = currentValue;
  });
};
Then(`the players are sorted {string} by {string}`, assertSortedByHeading);


/**
 * A step to assert that all player names contain some substring
 * @param {string} expectedSubstring
 *    - the sub string that all player names should contain
 * @example <caption>Only see players name Donald</caption>
 * Then all current players name contain "Donald"
 */
const assertNameContain = (expectedSubstring) => {
  cy.get('[data-cy="nameCell"]').each(($el, index, $list) => {
    expect($el.text().trim()).to.have.string(expectedSubstring);
  });
};
Then(`players name contain {string}`, assertNameContain);

/**
 * A step to assert that no matching records were found
 * @example
 * Then no matching records were found
 */
const assertNoMatchingRecords = () => {
  cy.get('.dataTables_empty');
};
Then(`no matching records were found`, assertNoMatchingRecords);
