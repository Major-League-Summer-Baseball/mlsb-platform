import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';
import { Team } from '../../../interfaces/team';
import { Game } from '../../../interfaces/game';
import { Player } from '../../../interfaces/player';
import { create_player } from '../../global/login'

/** The URL for the captain app page. */
const CAPTAIN_SELECTION_PAGE = 'captain/games/';
const CAPTAIN_SUBMIT_SCORE = 'captain/api/submit_score';
const YEAR = new Date().getFullYear();

/** Hook for the score app. */
const scoreappHook = (): void => {
    cy.intercept({
        url: '/captain/api/submit_score/**',
        method: 'POST',
    }).as('scoreSubmission');
};
beforeEach(scoreappHook);

/** Login as a captain of some team. */
const captainLogin = (): void => {
    cy.request('GET', 'testing/api/get_current_team', {}).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const team: Team = response.body;
        const captain: Player = team.captain as Player;
        cy.wrap(team).as('team');
        create_player(captain);
        cy.wrap(captain).as('captain');
    })
};
Given(`I am captain of a team`, captainLogin);


/** Ensure team has game today. */
const teamHasGame = (): Cypress.Chainable<Game> => {
    cy.get<Team>('@team').then((team: Team) => {
        cy.request('POST', `/testing/api/team/${team.team_id}/game_without_score`).then((response) => {
            expect(response.isOkStatusCode).to.be.true;
            const game: Game = response.body;
            cy.wrap(game).as('game');
        })
    });
    return cy.get<Game>('@game');
};
Given(`my team had a game`, teamHasGame);


/** Submit score for today's game */
const submitScore = (): void => {
    cy.get<Game>('@game').then((game: Game) => {
        cy.get<Team>('@team').then((team: Team) => {
            cy.request("POST", `${CAPTAIN_SUBMIT_SCORE}/${team.team_id}`, {
                'game_id': game.game_id,
                'score': 0,
                'hr': [],
                'ss': []
            }).then((response) => {
                console.log(response);
            });
        });
    });
}
Given(`my score has been submitted`, submitScore);

/** Navigate to score app for some team. */
const navigateToScoreApp = (): void => {
    cy.get<Team>('@team').then((team: Team) => {
        cy.visit(`${CAPTAIN_SELECTION_PAGE}/${YEAR}`);
    })
};
When(`I view the list of Games`, navigateToScoreApp);

/** Assert that game is eligible for submitting scores or batting app. */
const assertGameEligible = (): void => {
    cy.get<Game>('@game').then((game: Game) => {
        cy.get(`#game-${game.game_id}-score`);
        cy.get(`#game-${game.game_id}-batting`);
    })
};
Then(`the game is elible for submission`, assertGameEligible);

/** Click the game score button and moves to score app */
const clickGameScoreButton = (): void => {
    cy.get<Game>('@game').then((game: Game) => {
        cy.get(`#game-${game.game_id}-score`).click();
        cy.get('#submitButton').should("be.visible");
    })
};
Then('I can begin to submit my score', clickGameScoreButton);

/** Click the game batting button and moves to batting app. */
const clickBattingButton = (): void => {
    cy.get<Game>('@game').then((game: Game) => {
        cy.get(`#game-${game.game_id}-batting`).click();
        cy.get('#gameOverButton').should("be.visible");
    })
};
Then('I can start the batting app', clickBattingButton);

/** Click the game resubmit button. */
const clickResubmitButton = (): void => {
    cy.get<Game>('@game').then((game: Game) => {
        cy.get(`#game-${game.game_id}`).find(`#game-${game.game_id}-resubmit`).click();
    })
};
Then('I click resubmit', clickResubmitButton);