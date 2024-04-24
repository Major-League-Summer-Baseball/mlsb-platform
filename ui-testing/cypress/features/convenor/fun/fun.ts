import { When } from "@badeball/cypress-cucumber-preprocessor";
import { generateFun } from "../../global/convenor";
import { Fun } from "../../../interfaces/fun";

/** Fill out the fun count details for adding a fun. */
const fillOutFunDetails = () => {
    const fun = generateFun();
    cy.get("#newFunYear").type(`${fun.year}`);
    cy.get("#newFunCount").type(`${fun.count}`);
};
When(`I fill out the fun details`, fillOutFunDetails);

/** Fill out the fun count details for adding a fun. */
const submitFun = () => {
    cy.get("#funCreate").click();
};
When(`I submit fun`, submitFun);

const updateFunDetails = () => {
    const updatedFun = generateFun();
    cy.get<Fun>('@fun').then((fun: Fun) => {
        cy.get(`#year${fun.fun_id}`).clear().type(`${updatedFun.year}`);
        cy.get(`#count${fun.fun_id}`).clear().type(`${updatedFun.count}`);
        cy.get(`#funSubmit${fun.fun_id}`).click();
    });
};
When(`I update the fun details`, updateFunDetails)
