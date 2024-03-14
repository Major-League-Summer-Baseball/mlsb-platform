import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';
import { Team } from '../../../interfaces/team';
import { Game } from '../../../interfaces/game';
import { Player } from '../../../interfaces/player';
import { create_player } from '../../global/login'

/** The URL for the captain app page. */
const CAPTAIN_APP_PAGE = 'captain/game';
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

/**  Navigate to score app for some team and game. */
const navigateToScoreAppForGame = (): void => {
    cy.get<Team>('@team').then((team: Team) => {
        teamHasGame().then((game: Game) => {
            cy.visit(`${CAPTAIN_APP_PAGE}/${YEAR}/${game.game_id}/${team.team_id}`);
        });
    });
    
};
Given(`submitting a score for a game`, navigateToScoreAppForGame);

/**
 * Set the score the game.
 * @param score the score to set
 */
const setScore = (score: number): void => {
    cy.get('#scoreInput').clear();
    cy.get('#scoreInput').type(String(score), {force: true}).should('have.value', score);
    cy.wrap(score).as('score');
};
When(`score is {int}`, setScore);

/** Set that I got one home run. */
const gotHomerun = (): void => {
    cy.get<Player>('@captain').then((player: Player) => {
        cy.get(`#plus-hr-${player.player_id}`).click();
    });
};
When(`I got a homerun`, gotHomerun);

/** Submit the score. */
const submitScore = (): void => {
    cy.get('#submitButton').should('not.be.disabled');
    cy.get('#submitButton').click();
};
When(`I am able to submit`, submitScore);

/** Assert that expected game is visible. */
const assertGameVisible = (): void => {
    cy.get<Game>('@game').then((game: Game) => {
        cy.get(`#game-${game.game_id}`).should('be.visible');
    });
};
Then(`I see the game`, assertGameVisible);

/** Assert that expected game is visible. */
const assertGameCanBeResubmitted = (): void => {
    
    cy.get<Game>('@game').then((game: Game) => {
        cy.get(`#game-${game.game_id}-resubmit`).should("exist");
    });
};
Then(`I see the game can be resubmitted`, assertGameCanBeResubmitted);

/** Assert the submission is blocked. */
const assertSubmissionBlocked = (): void => {
    cy.get('#submitButton').should('be.disabled');
};
Then(`I am unable to submit score`, assertSubmissionBlocked);

/**
 * Assert that there is an error message.
 * @param message the error message expected
 */
const assertErrorMessage = (message: string): void => {
    if (message == 'negative score') {
        cy.get('#negativeScoreError').should('be.visible');
    } else if (message == 'homerun') {
        cy.get('#homerunError').should('be.visible');
    }
};
Then(`see prompt about {string}`, assertErrorMessage);

/** Assert the score was submitted as expected */
const assertScoreSubmission = (): void => {
    cy.get<Game>('@game').then((game: Game) => {
        cy.get<Team>('@team').then((team: Team) => {
            cy.get<number>('@score').then((score: number) => {
                cy.wait('@scoreSubmission').then((interception) => {
                    // expecting 200
                    expect(interception.response?.statusCode).to.be.eq(200);

                    // check the submission makes sense
                    const submission = interception.request.body;
                    expect(submission.game_id).to.be.eq(game.game_id);
                    expect(submission.player_id).to.be.eq(team.captain?.player_id);
                    expect(submission.team_id).to.be.eq(team.team_id)
                    expect(parseInt(submission.score)).to.be.eq(score);

                    // ensure got a success response body
                    const success: boolean = interception.response?.body as boolean;
                    expect(success).to.be.true;                    
                });
            });
        });
    });
};
Then(`the score is submitted`, assertScoreSubmission);

