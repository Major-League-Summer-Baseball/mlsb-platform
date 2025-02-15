import { When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { Sponsor } from "../../../interfaces/sponsor";
import { generateTeam } from "../../global/convenor";
import { League } from "../../../interfaces/league";
import { Team } from "../../../interfaces/team";
import { Player } from "../../../interfaces/player";
import * as path from 'path';

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

/** Select the team template. */
const downloadTeamGameTemplate = () => {
    cy.get('#teamTemplate').click();
};
When(`select team template`, downloadTeamGameTemplate);

/**  Fill out teams details using wrapped sponsor and league. */
const fillOutTeamDetails = () => {
    const data = generateTeam();
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy.get<League>('@league').then((league: League) => {
            cy.get('#league').select(`${league.league_id}`);
            cy.get('#sponsor').select(`${sponsor.sponsor_id}`);
            cy.get('#year').clear().type(`${data.year}`);
            cy.get('#color').clear().type(data.color);
            submitTeam();
        });
    });
};
When(`I fill out the team details`, fillOutTeamDetails);

/**  Update out teams details using wrapped sponsor and league. */
const updateTeamDetails = () => {
    const data = generateTeam();
    cy.get('#year').clear().type(`${data.year}`);
    cy.get('#color').clear().type(data.color);
    submitTeam()
};
When(`I update the team details`, updateTeamDetails);

/** Add a team image */
const addTeamImage = () => {
    cy.fixture('test.png', null).as('TestImage');
    cy
        .findByRole('button', { name: /add image/i })
        .click();
    cy
        .get('input[type="file"][name="image"]')
        .selectFile('@TestImage');
    cy
        .findByRole('button', { name: /upload/i })
        .click();
};
When(`I add a team image`, addTeamImage)

/** Submit the change to the team */
const submitTeam = () => {
    cy.findByRole('button', { name: /update/i}).click();
};
When(`I click update`, submitTeam);

/**  Add wrapped player to the team. */
const addPlayerToTeam = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get('#searchPlayer').type(player.player_name);
        cy.get(`#playerList${player.player_id}`).click();
    })
};
When(`I add the player to team`, addPlayerToTeam);

/**  Remove wrapped player from the team. */
const removePlayerFromTeam = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get(`#removePlayer${player.player_id}`).click();
    })
};
When(`I remove the player to team`, removePlayerFromTeam);

/**  Make wrapped player the captain. */
const makePlayerCaptain = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get(`#makePlayerCaptain${player.player_id}`).click();
    })
};
When(`I make them the captain`, makePlayerCaptain);

/** Remove the team. */
const removeTeam = () => {
    cy.get('#removeTeam').click();
};
When(`I remove the team`, removeTeam);

/**  Assert player is on team. */
const assertPlayerOnTeam = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get('.list-group-item').contains(player.email).should('be.visible');
    })
};
Then(`I see them on the team`, assertPlayerOnTeam);

/**  Assert player is not on team. */
const assertPlayerNotOnTeam = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get(`player${player.player_id}`).should('not.exist');
    })
};
Then(`I dont see them on the team`, assertPlayerNotOnTeam);

/**  Assert player is captain of team. */
const assertPlayerCaptain = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get(`#makePlayerCaptain${player.player_id}`).should('not.exist');
    })
};
Then(`I see they the captain`, assertPlayerCaptain);

/** Assert the team template is download. */
const assertTeamTemplateDownload = () => {
    const downloadsFolder = Cypress.config("downloadsFolder");
    cy.readFile(path.join(downloadsFolder, "team_template.csv"));
};
Then(`the team template is downloaded`, assertTeamTemplateDownload);

/** Assert the team has an image. */
const assertTeamImage = () => {
    cy
        .findByRole('img')
        .should('have.attr', 'src')
        .should('include', 'test.png');
};
Then(`I see the added image`, assertTeamImage);