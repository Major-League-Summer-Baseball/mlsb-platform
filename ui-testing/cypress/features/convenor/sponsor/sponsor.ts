import { When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { Sponsor } from "../../../interfaces/sponsor";
import { generateSponsor } from "../../global/convenor";

/** Fill out the sponsor details for adding a sponsor. */
const fillOutSponsorDetails = () => {
    const sponsor = generateSponsor();
    cy
        .get('#sponsorFormNew')
        .within(() => {
            cy
                .findByRole('textbox', { name: /sponsor name/i })
                .type(sponsor.sponsor_name);
            cy
                .findByRole('textbox', { name: /link to sponsor/i })
                .type(sponsor.link);
            cy
                .findByRole('textbox', { name: /description/i })
                .type(sponsor.description);
        });
    cy.wrap(sponsor).as("sponsor");
};
When(`I fill out the sponsor details`, fillOutSponsorDetails);

/** Update the sponsor details for the wrapped sponsor. */
const updatetSponsorDetails = () => {
    const newDetails = generateSponsor();
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy
            .get(`#sponsorForm${sponsor.sponsor_id}`)
            .within(() => {
                cy
                    .findByRole('textbox', { name: /sponsor name/i })
                    .type(newDetails.sponsor_name);
                cy
                    .findByRole('textbox', { name: /link to sponsor/i })
                    .type(newDetails.link);
                cy
                    .findByRole('textbox', { name: /description/i })
                    .type(newDetails.description);
                
            });
        newDetails.sponsor_id = sponsor.sponsor_id;
        cy.wrap(newDetails).as("sponsor");
    });
};
When(`I update the sponsor details`, updatetSponsorDetails);

/** Submit the sponsor form. */
const submitSponsor = () => {
    cy
        .get('#sponsorFormNew')
        .within(() => {
            cy
                .findByRole('button', { name: /create/i })
                .click();
        });
};
When(`I submit sponsor`, submitSponsor);

/** Click update for the wrapped sponsor. */
const updateSponsor = () => {
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy
            .get(`#sponsorForm${sponsor.sponsor_id}`)
            .within(() => {
                cy
                    .findByRole('button', { name: /update/i })
                    .click();
            });
    });
};
When(`I click update`, updateSponsor);

/** Hide the wrapped sponsor. */
const hideSponsor = () => {
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy
            .get(`#sponsorForm${sponsor.sponsor_id}`)
            .within(() => {
                cy
                    .findByRole('button', { name: /visible/i })
                    .click();
            });
    });
};
When(`I hide the sponsor`, hideSponsor);

/** Upload the sponsor logo */
const uploadSponsorLogo = () => {
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy.fixture('test.png', null).as('TestImage');
        cy
            .get(`#sponsorForm${sponsor.sponsor_id}`)
            .within(() => {
                cy
                    .findByRole('button', { name: /add image/i })
                    .click();
                cy
                    .get('input[type="file"][name="image"]')
                    .selectFile('@TestImage');
                cy
                    .findByRole('button', { name: /upload/i })
                    .click();
            });
    });
};
When(`I upload a new logo`, uploadSponsorLogo);

/** Assert the wrapped sponsor is hidden. */
const assertHiddenSponsor = () => {
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy
            .get(`#sponsorForm${sponsor.sponsor_id}`)
            .within(() => {
                cy
                    .findByRole('button', { name: /hidden/i })
                    .should('be.visible');
            });
    });
};
Then(`sponsor is no longer visible`, assertHiddenSponsor);

const assertSponsorImage = () => {
    cy.get<Sponsor>('@sponsor').then((sponsor: Sponsor) => {
        cy
            .get(`#sponsorForm${sponsor.sponsor_id}`)
            .within(() => {
                cy
                    .findByRole('img')
                    .should('have.attr', 'src')
                    .should('include', 'test.png');
            });
    });
};
Then (`I see the logo`, assertSponsorImage);
