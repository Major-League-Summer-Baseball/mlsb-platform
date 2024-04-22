import { When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { Sponsor } from "../../../interfaces/sponsor";
import { generateTeam } from "../../global/convenor";
import { League } from "../../../interfaces/league";
import { Team } from "../../../interfaces/team";
import { Player } from "../../../interfaces/player";


/** Choose a option for new team. */
const chooseNewTeam = () => {
    cy.get('#newTeam').click();
}
When(`choose new team`, chooseNewTeam);

/** Choose a option for new team. */
const chooseWrappedTeam = () => {
    cy.get<Team>('@team').then((team: Team) => {
        cy.get(`#editTeam${team.team_id}`).click();
    });
}
When(`choose the team`, chooseWrappedTeam);

/**  Fill out teams details using wrapped sponsor and league. */
const fillOutTeamDetails = () => {
    const data = generateTeam();
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy.get<League>('@league').then((league: League) => {
            cy.get('#league').select(`${league.league_id}`);
            cy.get('#sponsor').select(`${sponsor.sponsor_id}`);
            cy.get('#year').clear().type(`${data.year}`);
            cy.get('#color').clear().type(data.color);
            cy.get('#submitGame').click();
        });
    });
};
When(`I fill out the team details`, fillOutTeamDetails);

/**  Update out teams details using wrapped sponsor and league. */
const updateTeamDetails = () => {
    const data = generateTeam();
    cy.get('#year').clear().type(`${data.year}`);
    cy.get('#color').clear().type(data.color);
    cy.get('#submitGame').click();
};
When(`I update the team details`, updateTeamDetails);

/**  Add wrapped player to the team. */
const addPlayerToTeam = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get('#searchPlayer').type(player.player_name);
        cy.get(`#playerList${player.player_id}`).click();
    })
};
When(`I add the player to team`, addPlayerToTeam);


/**  Assert player is on team. */
const asserPlayerOnTeam = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get('.list-group-item').contains(player.email).should('be.visible');
    })
};
When(`I see them on the team`, asserPlayerOnTeam);

