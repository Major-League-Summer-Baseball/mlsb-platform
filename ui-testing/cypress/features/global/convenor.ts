import { Given, Then } from "@badeball/cypress-cucumber-preprocessor";import { Sponsor } from "../../interfaces/sponsor";
import { getDateString, getTimeString, randomName } from "./helper";
import { Player } from "../../interfaces/player";
import { Team } from "../../interfaces/team";
import { Division, JoinLeagueRequest, League } from "../../interfaces/league";
import { LeagueEvent } from "../../interfaces/league_event";
import { LeagueEventDate } from "../../interfaces/league_event_date";
;

/** Generate sponsor data. */
export const generateSponsor = (): Sponsor => {
    return {
        sponsor_id: Math.round(Math.random() * 99),
        sponsor_name: randomName(),
        link: `http://${randomName()}.ca`,
        description: `${randomName()} is great`,
        active: true
    };
};

/** Generate player data. */
export const generatePlayer = (): Player => {
    return {
        player_id: Math.round(Math.random() * 99),
        email: `${randomName()}@mlsb.ca`,
        player_name: randomName(),
        gender: "m",
        active: true,
    };
};

/** Generate league event. */
export const generateLeagueEvent = (): LeagueEvent => {
    return {
        league_event_id: Math.round(Math.random() * 99),
        name: `${randomName()} Event`,
        description: `
        ${randomName()} ${randomName()} ${randomName()} ${randomName()}
        `,
        active: 1,
    };
};

/** Generate league. */
export const generateLeague = (): League => {
    return {
        league_id: Math.round(Math.random() * 99),
        league_name: `League-${randomName()}`,
    };
};

/** Generate division. */
export const generateDivision = (): Division => {
    return {
        division_id: Math.round(Math.random() * 99),
        division_name: `Division-${randomName()}`,
    };
};

/** Generate a league event date. */
export const generateLeagueEventDate = (): LeagueEventDate => {
    const date = new Date();
    return {
        league_event_id: Math.round(Math.random() * 99),
        league_event_date_id: Math.round(Math.random() * 99),
        date: getDateString(date),
        time: getTimeString(date)
    };
};

/** Create a league event */
const createDivision = () => {
    const data = generateDivision();
    cy.request('POST', '/rest/division', data).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const division: Division = response.body;
        cy.wrap(division).as('division');
    });
};
Given(`a division exists`, createDivision);

/** Create a league event */
const createLeague = () => {
    const data = generateLeague();
    cy.request('POST', '/rest/league', data).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const league: League = response.body;
        cy.wrap(league).as('league');
    });
};
Given(`a league exists`, createLeague);

/** Create a league event */
const createLeagueEvent = () => {
    const data = generateLeagueEvent();
    cy.request('POST', '/rest/league_event', data).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const leagueEvent: LeagueEvent = response.body;
        cy.wrap(leagueEvent).as('leagueEvent');
    });
};
Given(`a league event exists`, createLeagueEvent);

/** Create a sponsor through a form request */
const createSponsor = () => {
    const data = generateSponsor();
    cy.request('POST', '/rest/sponsor', data).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const sponsor: Sponsor = response.body;
        cy.wrap(sponsor).as('sponsor');
    });
};
Given(`a sponsor exists`, createSponsor);

/** Create a player through a form request */
const createPlayer = () => {
    const data = generatePlayer();
    cy.request('POST', '/rest/player', data).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const player: Player = response.body;
        cy.wrap(player).as('player');
    });
};
Given(`a player exists`, createPlayer);

/** Get an existing league. */
const getLeague = () => {
    cy.request('GET', '/rest/league').then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        expect(response.body.total).to.be.greaterThan(0);
        const league: League = response.body.items[0];
        cy.wrap(league).as('league');
    });
};

/** Get an existing sponsor. */
const getSponsor = () => {
    cy.request('GET', '/rest/sponsor').then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        expect(response.body.total).to.be.greaterThan(0);
        const sponsor: Sponsor = response.body.items[0];
        cy.wrap(sponsor).as('sponsor');
    });
};


/** Get an existing team. */
const getTeam = () => {
    getLeague();
    getSponsor();
    cy.get<League>('@league').then((league: League) => {
        cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
            cy.request('POST', '/rest/team', {
                color: randomName(),
                sponsor_id: sponsor.sponsor_id,
                league_id: league.league_id,
                year: new Date().getFullYear() 
            }).then((response) => {
                expect(response.isOkStatusCode).to.be.true;
                const team: Team = response.body;
                cy.wrap(team).as('team');
            })
        });
    });
};

/** Create a request to join the league */
const createJoinRequest = () => {
    const player = generatePlayer(); 
    getTeam();
    cy.get<Team>('@team').then((team: Team) => {
        cy.request('POST', '/testing/api/create_league_request', {
            team_id: team.team_id,
            gender: player.gender,
            email: player.email,
            player_name: player.player_name
        }).then((response) => {
            expect(response.isOkStatusCode).to.be.true;
            const join_league_request: JoinLeagueRequest = response.body;
            expect(join_league_request.email).to.be.equal(player.email);
            cy.wrap(join_league_request).as('join_league_request');
        });
    });
};
Given(`a player has requested to join league`, createJoinRequest);

/**
 * Assert a flash message after action on some model
 * @param category the model acted upon 
 * @param result  the result of the action
 */
const assertFlashMessage = (model: string, result: string) => {
    const matcher = new RegExp(`${model} ${result}`, 'i');
    cy.contains(matcher).should('be.visible');
};
Then(`I see {word} was {word}`, assertFlashMessage);
Then(`I see {string} was {string}`, assertFlashMessage);