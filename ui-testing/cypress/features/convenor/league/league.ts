import { When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { generateLeague, generateDivision } from "../../global/convenor";
import { LeagueEvent } from "../../../interfaces/league_event";
import { Division, League } from "../../../interfaces/league";

/** Fill out the league details for adding a league. */
const fillOutLeagueDetails = () => {
    const league = generateLeague();
    cy.get("#leagueName").type(league.league_name);
};
When(`I fill out the league details`, fillOutLeagueDetails);

/** Fill out the division details for adding a division. */
const fillOutDivisionDetails = () => {
    const division = generateDivision();
    cy.get("#divisionName").type(division.division_name);
};
When(`I fill out the division details`, fillOutDivisionDetails);

/** Update the league details. */
const updateLeagueDetails = () => {
    const updatedLeague = generateLeague();
    cy.get<League>('@league').then((league: League) => {
        cy.get(`#leagueName${league.league_id}`).clear().type(updatedLeague.league_name);
        league.league_name = updatedLeague.league_name;
        cy.wrap(league).as('league');
        cy.get(`#leagueSubmit${league.league_id}`).click()
    });
};
When(`I update the league details`, updateLeagueDetails);

/** Update the division details. */
const updateDivisionDetails = () => {
    const updatedDivision = generateDivision();
    cy.get<Division>('@division').then((division: Division) => {
        cy.get(`#divisionName${division.division_id}`).clear().type(updatedDivision.division_name);
        division.division_name = updatedDivision.division_name;
        cy.wrap(division).as('division');
        cy.get(`#divisionSubmit${division.division_id}`).click()
    });
};
When(`I update the division details`, updateDivisionDetails);

/** Submit league. */
const submitLeague = () => {
    cy.get("#leagueCreate").click();
};
When(`I submit league`, submitLeague);

/** Submit division. */
const submitDivision = () => {
    cy.get("#divisionCreate").click();
};
When(`I submit division`, submitDivision);

/** Assert the wrapped league event is hidden. */
const assertLeagueEventHidden = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy.get(`#leagueEventShow${leagueEvent.league_event_id}`).should('be.visible');
    });
};
Then(`I see league event is hidden`, assertLeagueEventHidden);