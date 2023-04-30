import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';
import { create_player, generate_player } from '../../global/login';
import { Player } from '../../../interfaces/player';

/** The URL for the events page. */
const EVENTS_PAGE = 'website/event/';


/** Create a player with no team. */
const create_some_player = (): void => {
    create_player(generate_player()).then((player: Player) => {
        expect(player.player_id).to.be.greaterThan(0);
        cy.wrap(player).as('player');
    });
};
Given(`there is some player`, create_some_player);

/**
 * A step to navigate to the events page.
 * @example
 * Given I navigate to the events page
 */
export const navigateToEventsPage = (): void => {
    // using 2016 since guaranteed about its events
    cy.visit({ url: EVENTS_PAGE + new Date().getFullYear() , method: 'GET' });
};
Given(`I navigate to the events page`, navigateToEventsPage);

/**
 * A step to view a given event.
 * @param {string} event - the name of event to view
 * @example
 * When viewing the event "Mystery Bus"
 */
export const viewGivenEvent = (event: string): void => {
    cy.get('a').contains(event).click();
};
When(`viewing the event {string}`, viewGivenEvent);

/**
 * A step to sign up for a event.
 * @param {string} event - the name of event to view
 * @example
 * When viewing the event "Mystery Bus"
 */
 export const signUpEvent = (): void => {
    cy.get('.btn-sign-up').filter(":visible").contains("Sign-up").click();
};
When(`I can sign up`, signUpEvent);

/**
 * A step to assert the event contains the given details.
 * @param {string} expectedDetails - the expected details of the event
 * @example
 * Then I see details relating to "school buses"
 */
export const assertEventDetails = (expectedDetails: string): void => {
    cy.get('p').contains(expectedDetails).should('be.visible');
};
Then(`I see details relating to {string}`, assertEventDetails);

/**
 * A step to assert user is registered for the event
 * @example
 * Then I see I am registered
 */
 export const assertEventRegistration = (): void => {
    cy.get('p').contains("You are registered").should('be.visible');
};
Then(`I see I am registered`, assertEventRegistration);
