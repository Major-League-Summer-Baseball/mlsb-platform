import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';
import { Team } from '../../../interfaces/team';
import { Game } from '../../../interfaces/game';
import { Player } from '../../../interfaces/player';
import { CaptainGames } from '../../../interfaces/captain_games';
import { create_player } from '../../global/login'

/** The URL for the captain app page. */
const CAPTAIN_BATTING_PAGE = 'captain/batting_app/';
const YEAR = new Date().getFullYear();

/** Hook for the score app. */
const scoreappHook = (): void => {
    cy.intercept({
        url: '/captain/api/submit_batting/**',
        method: 'POST',
    }).as('batsSubmission');
};
beforeEach(scoreappHook);

/** Login as a captain of some team with three players. */
const captainLogin = (): void => {
    cy.request('GET', 'testing/api/get_current_team', {}).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const team: Team = response.body;
        const captain: Player = team.captain as Player;
        cy.wrap(team).as('team');
        
        cy.wrap(captain).as('captain');
    });
};
Given(`I am captain of a team`, captainLogin);

/** Ensure team has game today. */
const teamHasGame = (): Cypress.Chainable<Game> => {
    cy.get<Team>('@team').then((team: Team) => {
        cy.request('POST', `/testing/api/team/${team.team_id}/game_without_score`).then((response) => {
            expect(response.isOkStatusCode).to.be.true;
            const game: Game = response.body;
            cy.wrap(game).as('game');
        });
    });
    return cy.get<Game>('@game');
};
Given(`my team had a game`, teamHasGame);

/**  Navigate to score app for some team and game. */
const navigateToBattingAppForGame = (): void => {
    
    cy.get<Player>('@captain').then((captain: Player) => {
        create_player(captain);
        cy.get<Team>('@team').then((team: Team) => {
            cy.get<Game>("@game").then((game: Game) => {
                cy.visit(`${CAPTAIN_BATTING_PAGE}/${YEAR}/${game.game_id}/${team.team_id}`);
            });
        });
    });
};
Given(`using the batting app for the game`, navigateToBattingAppForGame);

/** Batter has an at bat with some result. */
const batterHasAnAtBat = (bat_classification: string): void => {
    cy.get(".actions__bat").contains(` ${bat_classification} `, {matchCase: false}).click();
};
When(`the batter hits a {string}`, batterHasAnAtBat);
When(`the batter gets out by {string}`, batterHasAnAtBat);

/** Load up the bases. */
const loadUpBases = (): void => {
    batterHasAnAtBat("S");
    batterHasAnAtBat("S");
    batterHasAnAtBat("S");
};
When(`the bases are loaded`, loadUpBases);

/** Find the elgible batter for sapporos. */
const findEligbleBatter = (): void => {
    const femaleMatcher = new RegExp('female', 'i');
    cy.get('#player-lineup li div').contains(femaleMatcher).parent('div').invoke('attr', 'id').then((id) => {
        const player_id = id.split("-")[1];
        console.log(id);
        cy.wrap(player_id).as('female_player');
    });
    cy.get<string>('@female_player').then((player_id: string) => {
        // click a handful of times so they are at the top
        cy.get(`#rosterUp-${player_id}`).click();
        cy.get(`#rosterUp-${player_id}`).click();
        cy.get(`#rosterUp-${player_id}`).click();
        cy.get(`#rosterUp-${player_id}`).click();
        cy.get(`#rosterUp-${player_id}`).click();
    });
};
When(`the batter is eligible`, findEligbleBatter);

/** Find a batter who is not elgible sapporos. */
const findNotEligbleBatter = (): void => {
    const maleMatcher = new RegExp(/^(?!.*female).*male/, 'i');
    cy.get('#player-lineup li div').contains(maleMatcher).parent('div').invoke('attr', 'id').then((id) => {
        const player_id = id.split("-")[1];
        console.log(id);
        cy.wrap(player_id).as('male_player');
    });
    cy.get<string>('@male_player').then((player_id: string) => {
        // click a handful of times so they are at the top
        cy.get(`#rosterUp-${player_id}`).click();
        cy.get(`#rosterUp-${player_id}`).click();
        cy.get(`#rosterUp-${player_id}`).click();
        cy.get(`#rosterUp-${player_id}`).click();
        cy.get(`#rosterUp-${player_id}`).click();
    });
};
When(`the batter is not eligible`, findNotEligbleBatter)

/** Undo the previous hit. */
const undoHit = (): void => {
    cy.get(".actions__bat").contains("Undo", {matchCase: false}).click();
};
When(`I undo the hit`, undoHit);

/** Remove a player from the lineup */
const removePlayerFromLineup = (): void => {
    cy.get<Player>('@captain').then((player: Player) => {
        cy.get(`#rosterRemove-${player.player_id}`).click();
    });
};
When(`I remove a player from the lineup`, removePlayerFromLineup);

/** Move a player from bottom to top of lineup. */
const movePlayerTopOfLineup = (): void => {
    cy.get("#player-lineup li").last().invoke('attr', 'id').then((id) => {
        const player_id = id.split("-")[2];
        console.log(id);
        cy.wrap(player_id).as('last_player');
    })
    cy.get<string>('@last_player').then((player_id: string) => {
        cy.get(`#rosterUp-${player_id}`).click();
        cy.get(`#rosterUp-${player_id}`).click();
    });
};
When("I move a player to the top of the lineup", movePlayerTopOfLineup);

/** Move a player from top to bottom of lineup. */
const movePlayerBottomOfLineup = (): void => {
    cy.get("#player-lineup li").last().invoke('attr', 'id').then((id) => {
        const player_id = id.split("-")[2];
        cy.wrap(player_id).as('first_player');
    })
    cy.get<string>('@first_player').then((player_id: string) => {
        cy.get(`#rosterDown-${player_id}`).click();
        cy.get(`#rosterDown-${player_id}`).click();
    });
};
When("I move a player to the bottom of the lineup", movePlayerBottomOfLineup);

/** Restart the game. */
const restartTheGame = (): void => {
    cy.get("#restartButton").click();
};
When(`restart the game`, restartTheGame);

/** Submit the game. */
const submitTheGame = (): void => {
    cy.get("#gameOverButton").click();
};
When(`submit the game`, submitTheGame);

/** Assert batter is given on the base. */
const isBatterOnBase = (base: string): void => {
    cy.get(`#${base}Base`).should('have.class', 'bases__base--runner');
};
Then(`the batter advances to {string}`, isBatterOnBase);

/** Assert the batting option is not available. */
const assertHitNotAvailable = (bat_classification: string): void => {
    cy.get(".actions__bat").contains(` ${bat_classification} `, {matchCase: false}).should("not.exist");
};
Then(`they cannot hit a {string}`, assertHitNotAvailable);

/** Assert the inning of the game. */
const assertInning = (inning: number): void => {
    cy.get("#gameInning").contains(inning, {matchCase: false});
};
Then(`it is the {int} inning`, assertInning);

/** Assert the number of outs. */
const assertNumberOfOuts = (outs: number): void => {
    cy.get("#gameOuts").contains(outs, {matchCase: false});
};
Then(`there is {int} out`, assertNumberOfOuts);
Then(`there are {int} outs`, assertNumberOfOuts);

/** Assert the score of the game. */
const assertGameScore = (score: number): void => {
    cy.get("#gameScore").contains(score, {matchCase: false});
};
Then(`the score is {int}`, assertGameScore);

/** Assert the player is not in the lineup. */
const assertNotInLineup = (): void => {
    cy.get<Player>('@captain').then((player: Player) => {
        cy.get(`#roster-${player.player_id}`).should("not.exist");
    });
};
Then(`they are not in the lineup`, assertNotInLineup);

/** Assert the player is bottom of the lineup. */
const assertBottomOfLineup = (): void => {
    cy.get<string>('@first_player').then((player_id: string) => {
        cy.get(`#rosterDown-${player_id}`).should("have.attr", "disabled", "disabled");
        cy.get(`#rosterUp-${player_id}`).should("not.have.attr", "disabled", "disabled");
    });
};
Then(`they are on the bottom of the lineup`, assertBottomOfLineup);

/** Assert the player is bottom of the lineup. */
const assertTopOfLineup = (): void => {
    cy.get<string>('@last_player').then((player_id: string) => {
        cy.get(`#rosterUp-${player_id}`).should("have.attr", "disabled", "disabled");
        cy.get(`#rosterDown-${player_id}`).should("not.have.attr", "disabled", "disabled");
    });
};
Then(`they are at the top of the lineup`, assertTopOfLineup);

const assertScoreSubmitted = (): void => {
    cy.get<Game>('@game').then((game: Game) => {
        cy.get<Team>('@team').then((team: Team) => {
            cy.get<Player>('@captain').then((player: Player) => {
                cy.wait('@batsSubmission').then((interception) => {
                    // expecting 200
                    expect(interception.response?.statusCode).to.be.eq(200);
            
                    // check the submission makes sense
                    const submission = interception.request.body;
                    expect(submission.length).to.be.eq(1);
                    expect(parseInt(submission[0].player_id)).to.be.eq(player.player_id);
                    expect(parseInt(submission[0].team_id)).to.be.eq(team.team_id);
                    expect(submission[0].classification).to.be.eq("hr");
                    expect(parseInt(submission[0].inning)).to.be.eq(1);
                    expect(parseInt(submission[0].rbi)).to.be.eq(1);
            
                    // ensure got a success response body
                    const success: boolean = interception.response?.body as boolean;
                    expect(success).to.be.true;                    
                });
            });
        });
    });
    
};
Then(`score submission is accepted`, assertScoreSubmitted);
