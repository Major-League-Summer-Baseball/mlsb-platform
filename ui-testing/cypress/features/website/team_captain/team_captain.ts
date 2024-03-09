import { Given, Then, When } from '@badeball/cypress-cucumber-preprocessor';
import { getCurrentYear, randomEmail } from '../../global/helper';
import { create_player, generate_player } from '../../global/login';
import { Pagination } from '../../../interfaces/pagination';
import { Team } from '../../../interfaces/team';
import { Player } from '../../../interfaces/player';
import { JoinLeagueRequest } from '../../../interfaces/league';

/** The current year. */
const YEAR = (new Date()).getFullYear();

/** Create a team. */
const find_team = (): void => {
    cy.request(`/api/teams`).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const paginated_teams: Pagination = response.body;
        expect(paginated_teams.total).to.be.greaterThan(0);
        cy.wrap(paginated_teams.items[0]).as('team');
    })
};
Given(`some team exists`, find_team);

/** Create a captain of some team. */
const create_captain_of_team = (): void => {
    cy.get<Team>('@team').then((team: Team) => {
        create_player(generate_player()).then((player: Player) => {
            cy.wrap(player).as('captain');
            cy.request('POST', `/testing/api/make_captain`, {
                player_id: player.player_id,
                team_id: team.team_id 
            }).then((response) => {
                expect(response.isOkStatusCode).to.be.true;
                expect(response.body).to.be.true;
            });
        });
    });
};
Given(`I am the Captain`, create_captain_of_team);

/** Create a player with no team. */
const create_some_player = (): void => {
    create_player(generate_player()).then((player: Player) => {
        expect(player.player_id).to.be.greaterThan(0);
        cy.wrap(player).as('player');
    });
};
Given(`there is some player`, create_some_player);

/** Create a player on the team. */
const create_player_to_team = (): void => {
    create_some_player();
    cy.get<Player>('@player').then((player: Player) => {
        cy.get<Team>('@team').then((team: Team) => {
            cy.request(
                'POST',
                `/testing/api/${team.team_id}/add_player/${player.player_id}`)
            .then((response) => {
                expect(response.isOkStatusCode).to.be.true;
                expect(response.body).to.be.true;
            });
        });
    });
};
Given(`there is a player on my team`, create_player_to_team);

/** Create a request to join some team for a player. */
const create_request_join_team = (): void => {
    const player = generate_player(); 
    cy.wrap(player).as('player');
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
Given(`someone has requested to join the team`, create_request_join_team);

/** Navigate to the team page. */
const NavigateToTeam = (): void => {
    cy.get<Team>('@team').then((team) => {
        cy.visit(`/website/teams/${getCurrentYear()}/${team.team_id}`);
    });
};
When(`I navigate to the team page`, NavigateToTeam);

/** Accept a request to join the team. */
const accept_join_league_request = (): void => {
    cy.get<JoinLeagueRequest>('@join_league_request').then((league_request) => {
        cy.get(`#acceptRequest${league_request.id}`).click();
        cy.get(`#acceptRequest${league_request.id}`).should('not.exist');
    });
};
When(`accept the request`, accept_join_league_request);

/** Accept a request to join the team. */
const decline_join_league_request = (): void => {
    cy.get<JoinLeagueRequest>('@join_league_request').then((league_request) => {
        cy.get(`#rejectRequest${league_request.id}`).click();
        cy.get(`#rejectRequest${league_request.id}`).should('not.exist');
    });
};
When(`decline the request`, decline_join_league_request);

/** Add a player to the team. */
const add_player_to_team = (): void => {
    cy.get<Player>("@player").then((player) => {-
        cy.get("#selectPlayer")
            .select(`${player.player_id}`)
            .should("have.value", player.player_id);
        cy.get("#addPlayer").click();
    });
};
When(`I add the player`, add_player_to_team);

/** Remove a player from the team. */
const remove_player_from_team = (): void => {
    cy.get<Player>("@player").then((player) => {
        cy.get(`#removePlayer${player.player_id}`)
            .click();
        cy.get(`#removePlayer${player.player_id}`)
            .should('not.exist');
    });
};
When(`I remove the player`, remove_player_from_team);

/** Select the player from a lsit of players. */
const select_player = (): void => {
    cy.get<Player>("@player").then((player) => {
        cy.get(`#playerList${player.player_id}`).click();
    });
};
When(`I add them to my team`, select_player);

/** Captain add new player. */
const add_player = (): void => {
    const player = generate_player();
    cy.get('#playerListAdd').click();
    cy.get(`#newPlayerModalInputName`).type(player.player_name);
    cy.get(`#newPlayerModalInputEmail`).type(player.email);
    cy.get(`#newPlayerModalSubmit`).click();
    cy.get(`#newPlayerModalSubmit`).should('not.be.visible');
    cy.wrap(player).as('player');
};
When(`I add a new player`, add_player);

/** Search for the given player by email. */
const search_player = (): void => {
    cy.get<Player>("@player").then((player) => {-
        cy.get(`#searchPlayer`).type(player.email);
    });
};
When(`I search for the player`, search_player);

/** Search for a non-existent player. */
const search_non_player = (): void => {
    cy.get(`#searchPlayer`).type(randomEmail());
};
When(`I search for the nonexistent player`, search_non_player);

/** Assert that currently on the team page for some team. */
const assert_team_page = (): void => {
    cy.get<Team>('@team').then((team: Team) => {
        cy.get('#MainHeader').contains(team.team_name as string);
    })
};
Then(`I see the team page`, assert_team_page);

/** Assert a player account was created from accepting join league request. */
const assert_player_created = (): void => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.request('POST', `/api/view/player_lookup`, {email: player.email}).then((response) => {
            expect(response.isOkStatusCode).to.be.true;
            expect(response.body).length.to.greaterThan(0);
            cy.wrap(response.body[0]).as('player');
        });
    });
};
Then(`a player is added to the league`, assert_player_created);

/** Assert a player account was not created from rejecting join league request.*/
const assert_player_not_created = (): void => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.request('POST', `/api/view/player_lookup`, {email: player.email}).then((response) => {
            expect(response.isOkStatusCode).to.be.true;
            expect(response.body.length).equal(0);
            cy.wrap(response.body[0]).as('player');
        });
    });
};
Then(`a player is not added to the league`, assert_player_not_created);

/** Assert the player is on a team. */
const assert_player_on_team = (): void => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get<Team>('@team').then((team: Team) => {
            cy.request('POST', `/api/view/players/team_lookup`, {player_id: player.player_id}).then((response) => {
                expect(response.isOkStatusCode).to.be.true;
                expect(response.body).length.to.greaterThan(0);
                expect(response.body[0].team_id).to.be.equal(team.team_id);
            });
        })
        
    });
};
Then(`the player is part of the team`, assert_player_on_team);

/** Assert the player is not on a team. */
const assert_player_not_on_team = (): void => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get<Team>('@team').then((team: Team) => {
            cy.get(`#player${player.player_id}`).should("not.exist");
            cy.request('POST', `/api/view/players/team_lookup`, {player_id: player.player_id}).then((response) => {
                expect(response.isOkStatusCode).to.be.true;
                expect(response.body.length).length.to.equal(0);
            });
        })
        
    });
};
Then(`the player is not part of the team`, assert_player_not_on_team);
