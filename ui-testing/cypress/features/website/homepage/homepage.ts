import { When, Then } from '@badeball/cypress-cucumber-preprocessor';

/**
 * A step to navigate to system homepage.
 * @example
 * When I navigate to the home page
 */
export const navigateToHomepage = (): void => {
    cy.visit({ url: '', method: 'GET' });
};
When(`I navigate to the home page`, navigateToHomepage);

/**
 * A step to navigate to system homepage for a specific year.
 * @param {number} year - the year to navigate to
 * @example
 * When I navigate to 2016 home page
 */
export const navigateToSpecificYearHomepage = (year: number): void => {
    cy.visit({ url: '/website/' + year, method: 'GET' });
};
When(`I navigate to {string} home page`, navigateToSpecificYearHomepage);

/**
 * A step to view the given news item.
 * @param {string} itemTitle - the title of the news item
 * @example
 * When I click on "Launch" news item
 */
export const viewNewsItem = (itemTitle: string): void => {
    cy.get('[data-cy="' + itemTitle + '"]').click();
};
When(`I click on {string} news item`, viewNewsItem);

/**
 * A step to assert the current page contains a list of recent game scores.
 * @example
 * Then there is a list of recent game scores
 */
export const assertListOfGameScores = (): void => {
    cy.get('[data-cy="games"]').find('[data-cy="game"]').its('length').should('be.gte', 1);
};
Then(`there is a list of recent game scores`, assertListOfGameScores);

/**
 * A step to assert the current page contains a list of sponsors.
 * @example
 * Then there is a list of sponsors
 */
export const assertListOfSponsors = (): void => {
    cy.get('.flickity-slider').find('.sponsor-cell').its('length').should('be.gte', 1);
};
Then(`there is a list of sponsors`, assertListOfSponsors);

/**
 * A step to assert homepage has a list of news items.
 * @example
 * Then there is a list of news items
 */
export const assertListOfNewsItems = (): void => {
    cy.get('.flickity-slider').find('[data-cy="sponsor-cell"]').its('length').should('be.gte', 1);
};
Then(`there is a list of news items`, assertListOfNewsItems);

/**
 * Navigate through the list of sponsors.
 * @example
 * Then I can navigate through the list of sponsors
 */
export const navigateSponsorsList = (): void => {
    cy.get('.next').click();
    cy.get('.previous').click();
};
Then(`I can navigate through the list of sponsors`, navigateSponsorsList);

/**
 * Assert that current page is a post about the launch of the website.
 * @example
 * Then I see details about website launch
 */
export const assertLaunchNews = (): void => {
    cy.findByRole('heading', { name: 'Launch'});
};
Then(`I see details about website launch`, assertLaunchNews);
