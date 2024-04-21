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

const submitSponsor = () => {
    cy.get("#sponsorCreate").click();
};
When(`I submit sponsor`, submitSponsor);


