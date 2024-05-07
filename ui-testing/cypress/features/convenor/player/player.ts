import { When } from "@badeball/cypress-cucumber-preprocessor";
import { generatePlayer } from "../../global/convenor";
import { Player } from "../../../interfaces/player";

/** Click something based upon text. */
const clickByText = (btnText: string) => {
    cy.findByText(btnText).click();
};
When(`I click {string}`, clickByText);

/** Fill out the player details for adding a player. */
const fillOutPlayerDetails = () => {
    const player = generatePlayer();
    cy.get("#newPlayerModalInputName").type(player.player_name);
    cy.get("#newPlayerModalInputEmail").type(player.email);
    cy.wrap(player).as("player");
};
When(`I fill out the player details`, fillOutPlayerDetails);

/** Fill out the player details for adding a player. */
const updatePlayerDetails = () => {
    const newDetails = generatePlayer();
    cy.get<Player>('@player').then((player: Player) => {
        cy.get("#newPlayerModalInputName").clear().type(newDetails.player_name);
        cy.get("#newPlayerModalInputEmail").clear().type(newDetails.email);
        player.player_name = newDetails.player_name;
        player.email = newDetails.email;
        cy.wrap(player).as("player");
    });
    submitPlayer();
};
When(`I update the player details`, updatePlayerDetails);

/** Submit the new player. */
const submitPlayer = () => {
    cy.get('#playerSubmit').click();
};
When(`I submit player`, submitPlayer);

/** Search for the given wrapped player. */
const searchPlayer = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get('#searchPlayer').type(player.player_name);
    });
};
When(`I search for the player`, searchPlayer);

/** Select a playe.r */
const selectPlayer = () => {
    cy.get<Player>('@player').then((player: Player) => {
        cy.get(`#playerList${player.player_id}`).click();
    });
}
When(`I select the player`, selectPlayer);

/** Accept a player request */
const acceptPlayerRequest = () => {
    cy.findAllByText("Accept").first().click();
}
When(`I respond to their request`, acceptPlayerRequest);

/** Merge the player in second player. */
const mergePlayer = () => {
    cy.get<Player>('@secondPlayer').then((player: Player) => {
        cy.get('#mergePlayer').click();
        cy.get('#searchPlayer').type(player.player_name);
        cy.get(`#playerList${player.player_id}`).click();
        cy.get('#submitMergePlayer').click();
    });
}
When(`I merge the player`, mergePlayer);
