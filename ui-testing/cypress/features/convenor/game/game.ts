import { When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { generateGame } from "../../global/convenor";
import { Division, League } from "../../../interfaces/league";
import { Team } from "../../../interfaces/team";
import { Game } from "../../../interfaces/game";
import * as path from 'path';

/** Choose a option for new team. */
const chooseNewGame = () => {
    cy.get<League>('@league').then((league: League) => {
        cy.get('#newGames').click();
        cy.get(`#newGame${league.league_id}`).click();
    })
};
When(`choose new game`, chooseNewGame);

/** Choose the wrapped game. */
const chooseGame = () => {
    cy.get<Game>('@game').then((game: Game) => {
        cy.get(`#game${game.game_id}`).click();
    })
};
When(`choose the game`, chooseGame);

/** Select the game template. */
const downloadGameTemplate = () => {
    cy.get('#gameTemplate').click();
};
When(`select game template`, downloadGameTemplate);

/** Fill out game details. */
const fillOutGameDetails = () => {
    const data = generateGame();
    cy.get<Team>('@home_team').then((homeTeam: Team) => {
        cy.get<Team>('@away_team').then((awayTeam: Team) => {
            cy.get<Division>('@division').then((division: Division) => {
                cy.get('#date').type(data.date);
                cy.get('#time').type(data.time);
                cy.get('#field').type(data.field);
                cy.get('#homeTeam').select(`${homeTeam.team_id}`);
                cy.get('#awayTeam').select(`${awayTeam.team_id}`);
                cy.get('#division').select(`${division.division_id}`);
                cy.get('#submitGame').click();
            });
        });
    });
}
When(`I fill out the game details`, fillOutGameDetails);

/** Update game details. */
const updateGameDetails = () => {
    cy.get('#time').clear().type("12:00");
    cy.get('#field').clear().type("WP2");
    cy.get('#submitGame').click();
}
When(`I update the game details`, updateGameDetails);

/** Assert the game template was downloaded. */
const assertGameTemplateDownload = () => {
    const downloadsFolder = Cypress.config("downloadsFolder");
    cy.readFile(path.join(downloadsFolder, "team_template.csv"));
};
Then(`the game template is downloaded`, assertGameTemplateDownload);
