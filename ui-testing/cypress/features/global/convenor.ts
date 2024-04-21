import { Given, Then } from "@badeball/cypress-cucumber-preprocessor";import { Sponsor } from "../../interfaces/sponsor";
import { randomName } from "./helper";
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