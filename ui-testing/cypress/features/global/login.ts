import { Given } from "@badeball/cypress-cucumber-preprocessor";;
import { Player } from '../../interfaces/player';
import { randomName, randomEmail } from './helper';

/**
 * Generates a random player.
 * @returns a player
 */
export const generate_player = (): Player => {
    return {
        player_name: randomName(),
        email: randomEmail(),
        active: true,
        gender: "m",
        player_id: null
    } as Player;
};

/**
 * Create a player.
 * @param player the player to create
 * @returns the created player
 */
export const create_player = (player: Player): Cypress.Chainable<Player> => {
    cy.request('POST', '/testing/api/create_and_login', player).then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const created_player: Player = response.body;
        created_player.email = player.email;
        cy.wrap(created_player).as(created_player.player_name);
    })
    return cy.get<Player>(`@${player.player_name}`);
};

/**
 * A global step that creates a random user for the given roll and then
 * logins by making a POST request.
 * @param {string} role - the role of the user to log in as.
 * @example
 * Given I am logged in as administrator
 */
export const login = (): void => {
    cy.login();
};
Given(`I am logged in as an admin`, login);


/** Login as a newly created player. */
const login_as_player = (): void => {
    create_player(generate_player()).then((player: Player) => {
        cy.wrap(player).as('player');
    })
};
Given(`I am logged in as a player`, login_as_player);