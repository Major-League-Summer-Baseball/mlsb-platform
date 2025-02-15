import { Given } from "@badeball/cypress-cucumber-preprocessor";;
import { Player } from '../../interfaces/player';
import { randomName, randomEmail } from './helper';

/**
 * Generates a random player.
 * @params gender if given otherwise m
 * @returns a player
 */
export const generate_player = (gender?: string): Player => {
    return {
        player_name: randomName(),
        email: randomEmail(),
        active: true,
        gender: gender || "m",
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
 * Login as a convenor and wrap it to convenor
 * @returns the convenor
 */
export const login_convenor = () => {
    cy.request('POST','/testing/api/convenor/login').then((response) => {
        expect(response.isOkStatusCode).to.be.true;
        const created_player: Player = response.body;
        cy.wrap(create_player).as('convenor');
    })
    return cy.get<Player>(`@convenor`);
}

/** Login as a newly created player. */
const login_as_player = (): void => {
    create_player(generate_player()).then((player: Player) => {
        cy.wrap(player).as('player');
    })
};
Given(`I am logged in as a player`, login_as_player);


/** Login as a convenor. */
const login_as_convenor = (): void => {
    login_convenor();
};
Given(`I am logged in as a convenor`, login_as_convenor);

