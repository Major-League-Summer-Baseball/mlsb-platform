import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { Sponsor } from "../../../interfaces/sponsor";
import { randomName } from "../../global/helper";
import {generateSponsor} from "../../global/convenor";

/** Fill out the sponsor details for adding a sponsor. */
const fillOutSponsorDetails = () => {
    const sponsor = generateSponsor();
    cy.get("#newSponsorName").type(sponsor.sponsor_name);
    cy.get("#newSponsorLink").type(sponsor.link);
    cy.get("#newSponsorDescription").type(sponsor.description);
    cy.wrap(sponsor).as("sponsor");
};
When(`I fill out the sponsor details`, fillOutSponsorDetails);

/** Update the sponsor details for the wrapped sponsor. */
const updatetSponsorDetails = () => {
    const newDetails = generateSponsor();
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy.get(`#sponsorName${sponsor.sponsor_id}`).type(newDetails.sponsor_name);
        cy.get(`#sponsorLink${sponsor.sponsor_id}`).type(newDetails.link);
        cy.get(`#sponsorDescription${sponsor.sponsor_id}`).type(newDetails.description);
        newDetails.sponsor_id = sponsor.sponsor_id;
        cy.wrap(newDetails).as("sponsor");
    });
};
When(`I update the sponsor details`, updatetSponsorDetails);

/** Submit the sponsor form. */
const submitSponsor = () => {
    cy.get("#sponsorCreate").click();
};
When(`I submit sponsor`, submitSponsor);

/** Click update for the wrapped sponsor. */
const updateSponsor = () => {
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy.get(`#sponsorSubmit${sponsor.sponsor_id}`).click();
    });
};
When(`I click update`, updateSponsor);

/** Hide the wrapped sponsor. */
const hideSponsor = () => {
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy.get(`#sponsorInactive${sponsor.sponsor_id}`).click();
    });
};
When(`I hide the sponsor`, hideSponsor);

/** Assert the wrapped sponsor is hidden. */
const assertHiddenSponsor = () => {
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy.get(`#sponsorActive${sponsor.sponsor_id}`).should('be.visible');
    });
};
Then(`sponsor is no longer visible`, assertHiddenSponsor);

