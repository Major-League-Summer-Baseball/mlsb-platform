import { When, Then } from '@badeball/cypress-cucumber-preprocessor';
import { getCurrentYear } from '../../global/helper';

/** The URL for the current season leaders page. */
const LEADERS_PAGE = 'website/leaders/';

/** The URL for the all-time leaders page. */
const ALL_TIME_LEADERS_PAGE = 'website/hall-of-fame/';

/**
 * A function to assert the given list is in descending order
 * @param {string} selector - a selector for the given list of elements
 */
const assertDescendingOrder = (selector: string): void => {
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
export const navigateToLeagueLeaderPage = (): void => {
    cy.visit({ url: LEADERS_PAGE + getCurrentYear(), method: 'GET' });
};
When(`I navigate to the league leaders page`, navigateToLeagueLeaderPage);

/**
 * A step to navigate to all-time leader page.
 * @example
 * When I navigate to the all-time leader page
 */
export const navigateToAllTimeLeaderPage = (): void => {
    cy.visit({ url: ALL_TIME_LEADERS_PAGE + getCurrentYear(), method: 'GET' });
};
When(`I navigate to the hall-of-fame page`, navigateToAllTimeLeaderPage);

/**
 * A step to assert that the homeruns are in descending order.
 * @example
 * Then there is a descending ordered list of players for homeruns
 */
export const assertHomerunsHasDescendingOrder = (): void => {
    assertDescendingOrder('[data-cy="currentSeasonHomeruns"]');
};
Then(`there is a descending ordered list of players for homeruns`, assertHomerunsHasDescendingOrder);

/**
 * A step to assert that the singles are in descending order.
 * @example
 * Then there is a descending ordered list of players for singles
 */
export const assertSinglesHasDescendingOrder = (): void => {
    assertDescendingOrder('[data-cy="currentSeasonSingles"]');
};
Then(`there is a descending ordered list of players for singles`, assertSinglesHasDescendingOrder);

/**
 * A step to assert that the homeruns are in descending order.
 * @example
 * Then there is a descending ordered list of players for all-time homeruns
 */
export const assertAllTimeHomerunsHasDescendingOrder = (): void => {
    assertDescendingOrder('[data-cy="allTimeCareerHomeruns"]');
    assertDescendingOrder('[data-cy="allTimeSingleSeasonHomeruns"]');
};
Then(`there is a descending ordered list of players for all-time homeruns`, assertAllTimeHomerunsHasDescendingOrder);

/**
 * A step to assert that the singles are in descending order.
 * @example
 * Then there is a descending ordered list of players for all-time singles
 */
export const assertAllTimeSinglesHasDescendingOrder = (): void => {
    assertDescendingOrder('[data-cy="allTimeSingleSeasonSingles"]');
    assertDescendingOrder('[data-cy="allTimeCareerSingles"]');
};
Then(`there is a descending ordered list of players for all-time singles`, assertAllTimeSinglesHasDescendingOrder);
