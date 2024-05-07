import { Given, Then } from "@badeball/cypress-cucumber-preprocessor";import { Sponsor } from "../../interfaces/sponsor";
import { getCurrentYear, getDateString, randomId, randomName, getRandomInt } from "./helper";
import { Player } from "../../interfaces/player";
import { Team } from "../../interfaces/team";
import { Division, JoinLeagueRequest, League } from "../../interfaces/league";
import { LeagueEvent } from "../../interfaces/league_event";
import { LeagueEventDate } from "../../interfaces/league_event_date";
import { Game } from "../../interfaces/game";
import { Fun } from "../../interfaces/fun";

/** Generate sponsor data. */
export const generateSponsor = (): Sponsor => {
    return {
        sponsor_id: randomId(),
        sponsor_name: randomName(),
        link: `http://${randomName()}.ca`,
        description: `${randomName()} is great`,
        active: true
    };
};

/** Generate fun. */
export const generateFun = (): Fun => {
    return {
        fun_id: randomId(),
        year: getCurrentYear(),
        count: getRandomInt(999),
    };
};

/** Generate player data. */
export const generatePlayer = (): Player => {
    return {
        player_id: randomId(),
        email: `${randomName()}@mlsb.ca`,
        player_name: randomName(),
        gender: "m",
        active: true,
    };
};

/** Generate team data. */
export const generateTeam = (): Team => {
    return {
        team_id: randomId(),
        league_id: randomId(),
        sponsor_id: randomId(),
        color: `${randomName()}-Color`,
        year: getCurrentYear(),
        espys: 0,
        team_name: null,
        captain: null
    };
};

/** Generate league. */
export const generateLeague = (): League => {
    return {
        league_id: randomId(),
        league_name: `League-${randomName()}`,
    };
};

/** Generate division. */
export const generateDivision = (): Division => {
    return {
        division_id: randomId(),
        division_name: `Division-${randomName()}`,
    };
};

/** Generate game. */
export const generateGame = (): Game => {
    return {
        game_id: randomId(),
        home_team_id: randomId(),
        home_team: randomName(),
        away_team: randomName(),
        away_team_id: randomId(),
        league_id: randomId(),
        division_id: randomId(),
        date: getDateString(new Date()),
        time: "11:00",
        status: "",
        field: "WP1"
    };
};

/** Generate league event. */
export const generateLeagueEvent = (): LeagueEvent => {
    return {
        league_event_id: randomId(),
        name: `${randomName()} Event`,
        description: `
        ${randomName()} ${randomName()} ${randomName()} ${randomName()}
        `,
        active: 1,
    };
};

/** Generate a league event date. */
export const generateLeagueEventDate = (): LeagueEventDate => {
    const date = new Date();
    return {
        league_event_id: randomId(),
        league_event_date_id: randomId(),
        date: getDateString(date),
        time: "10:00"
    };
};

/** Create a fun count */
const createFun = () => {
    const data = generateFun();
    cy.request('POST', '/rest/fun', data).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const fun: Fun = response.body;
        cy.wrap(fun).as('fun');
    });
};
Given(`a fun exists`, createFun);

/** Create a division event */
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

/** Create a player through a rest request */
const createPlayer = () => {
    const data = generatePlayer();
    cy.request('POST', '/rest/player', data).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const player: Player = response.body;
        cy.wrap(player).as('player');
    });
};
Given(`a player exists`, createPlayer);

/** Create two player through a rest request */
const createTwoPlayer = () => {
    createPlayer();
    const data2 = generatePlayer();
    cy.request('POST', '/rest/player', data2).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const player: Player = response.body;
        cy.wrap(player).as('secondPlayer');
    });
};
Given(`a players exists`, createTwoPlayer);

/** Create a team through a rest request */
const createTeam = () => {
    createSponsor();
    createLeague();
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy.get<League>('@league').then((league: League) => {
            cy.request('POST', '/rest/team', {
                color: randomName(),
                year: getCurrentYear(),
                sponsor_id: sponsor.sponsor_id,
                league_id: league.league_id
            }).then((response) => {
                expect(response.isOkStatusCode).to.be.true;
                const team: Team = response.body;
                cy.wrap(team).as('team');
            });
        });
    });
};
Given(`a team exists`, createTeam);

/** Create a two teams. */
const createTwoTeams = () => {
    createSponsor();
    createLeague();
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy.get<League>('@league').then((league: League) => {
            cy.request('POST', '/rest/team', {
                color: randomName(),
                year: getCurrentYear(),
                sponsor_id: sponsor.sponsor_id,
                league_id: league.league_id
            }).then((response) => {
                expect(response.isOkStatusCode).to.be.true;
                const team: Team = response.body;
                cy.wrap(team).as('home_team');
            });
            cy.request('POST', '/rest/team', {
                color: randomName(),
                year: getCurrentYear(),
                sponsor_id: sponsor.sponsor_id,
                league_id: league.league_id
            }).then((response) => {
                expect(response.isOkStatusCode).to.be.true;
                const team: Team = response.body;
                cy.wrap(team).as('away_team');
            });
        });
    });
};
Given(`two team exists`, createTwoTeams);


const createGame = () => {
    createTwoTeams();
    createDivision();
    cy.get<Team>('@home_team').then((homeTeam: Team) => {
        cy.get<Team>('@away_team').then((awayTeam: Team) => {
            cy.get<Division>('@division').then((division: Division) => {
                cy.request('POST', '/rest/game', {
                    'home_team_id': homeTeam.team_id,
                    'away_team_id': awayTeam.team_id,
                    'league_id': homeTeam.league_id,
                    'division_id': division.division_id,
                    'status': '',
                    'field': 'WP1',
                    'time': '11:00',
                    'date': getDateString(new Date())
                }).then((response) => {
                    expect(response.isOkStatusCode).to.be.true;
                    const game: Game = response.body;
                    cy.wrap(game).as('game');
                });
            });
        });
    });
}
Given(`a game exists`, createGame);

/** Add a player to a team. */
const addPlayerToTeam = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get<Team>('@team').then((team: Team) => {
            cy.request('POST', `/testing/api/${team.team_id}/add_player/${player.player_id}`).then((response) => {
                expect(response.isOkStatusCode).to.be.true;
            });
        });
    });
};
Given(`player is on the team`, addPlayerToTeam);

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