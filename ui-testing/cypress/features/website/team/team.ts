import { Given, Then, When } from '@badeball/cypress-cucumber-preprocessor';
import { getCurrentYear } from '../../global/helper';
import { generate_player } from '../../global/login';
import { Pagination } from '../../../interfaces/pagination';
import { Team } from '../../../interfaces/team';

/** The current year. */
const YEAR = (new Date()).getFullYear();

/** Create a team. */
const find_team = (): void => {
    cy.request('POST', `/rest/teamlookup`, {year: getCurrentYear()}).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const teams: Team[] = response.body;
        expect(teams).length.to.greaterThan(0);
        cy.wrap(teams[0]).as('team');
    })
};
Given(`some team exists`, find_team);

/** Navigate to the team page. */
const NavigateToTeam = (): void => {
    cy.get<Team>('@team').then((team) => {
        cy.visit(`/website/teams/${getCurrentYear()}/${team.team_id}`);
    });
};
When(`I navigate to the team page`, NavigateToTeam);

/** Assert that currently on the team page for some team. */
const assert_team_page = (): void => {
    cy.get<Team>('@team').then((team: Team) => {
        cy.get('#MainHeader').contains(team.team_name as string);
    })
};
Then(`I see the team page`, assert_team_page);

/** Click the button to join team. */
const request_to_join = (): void => {
    cy.get<Team>('@team').then((team: Team) => {
        cy.get('#join_team').click();
    });
};
Then(`I can make a request to join`, request_to_join);

/** Fill out the new player details. */
const fill_out_details = (): void => {
    const player = generate_player();
    cy.get("#joinTeamRequestInputName").type(player.player_name);
    cy.get("#joinTeamRequestInputEmail").type(player.email);
    cy.get("#joinTeamRequestSubmit").click();
    
};
Then(`I fill out my details`, fill_out_details);

/** Assert the request was submitted. */
const assert_pending_request = (): void => {
    cy.get('#message').contains("Submitted request to join");
};
Then(`I see my request is pending`, assert_pending_request);
