import { When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { generateLeagueEvent, generateLeagueEventDate } from "../../global/convenor";
import { LeagueEvent } from "../../../interfaces/league_event";

/** Fill out the league event details for adding a league event. */
const fillOutLeagueEventDetails = () => {
    const leagueEvent = generateLeagueEvent();
    cy.get("#newLeagueEventName").type(leagueEvent.name);
    // unable to fill in ckeditor
    // skipping test for now
};
When(`I fill out the league events details`, fillOutLeagueEventDetails);

/** Update the league event details. */
const updateLeagueEventDetails = () => {
    const updatedEvent = generateLeagueEvent();
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy.get(`#leagueEventName${leagueEvent.league_event_id}`).clear().type(updatedEvent.name);
        leagueEvent.name = updatedEvent.name;
        cy.wrap(leagueEvent).as('leagueEvent');
        cy.get(`#leagueEventSubmit${leagueEvent.league_event_id}`).click()
    });
};
When(`I update the league event details`, updateLeagueEventDetails);

/** Hide the wrapped league event. */
const hideLeagueEvent = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy.get(`#leagueEventHide${leagueEvent.league_event_id}`).click();
    });
};
When(`I hide the league event`, hideLeagueEvent);

/** See league event dates for wrapped league event. */
const seeLeagueEventDates = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy.get(`#leagueEventSeeDates${leagueEvent.league_event_id}`).click();
    });
};
When(`see dates for the league event`, seeLeagueEventDates);

/** Enter league event date. */
const enterLeagueEventDate = () => {
    const eventDate = generateLeagueEventDate();
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy.get(`#newDate`).type(eventDate.date);
        cy.get(`#newTime`).type(eventDate.time);
        cy.get(`#leagueEventDateCreate`).click();
    });
};
When(`I enter a new date`, enterLeagueEventDate);

/** Assert the wrapped league event is hidden. */
const assertLeagueEventHidden = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy.get(`#leagueEventShow${leagueEvent.league_event_id}`).should('be.visible');
    });
};
Then(`I see league event is hidden`, assertLeagueEventHidden);