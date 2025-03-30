import { When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { generateLeagueEvent, generateLeagueEventDate } from "../../global/convenor";
import { LeagueEvent } from "../../../interfaces/league_event";

/** Fill out the league event details for adding a league event. */
const fillOutLeagueEventDetails = () => {
    const leagueEvent = generateLeagueEvent();
    cy.get("#newLeagueEventName").type(leagueEvent.name);
    cy.get("#quillTextareaNew").should('be.visible').then(($quillContainer) => {
        const quillEditor = $quillContainer.find('.ql-editor')[0];
        if (quillEditor) {
        cy.wrap(quillEditor).type(leagueEvent.description);
        } else {
        // Handle the case when Quill editor is not found
        throw new Error('Quill editor not found within the selected element');
        }
    });
};
When(`I fill out the league events details`, fillOutLeagueEventDetails);

/** Update the league event details. */
const updateLeagueEventDetails = () => {
    const updatedEvent = generateLeagueEvent();
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy
        .get(`#leagueEventForm${leagueEvent.league_event_id}`)
        .within(() => {
            cy
                .findByRole('textbox', { name: /league event name/i })
                .clear()
                .type(updatedEvent.name);
            leagueEvent.name = updatedEvent.name;
            cy.wrap(leagueEvent).as('leagueEvent');
            cy
                .findByRole('button', { name: /update/i })
                .click();
        });
    });
};
When(`I update the league event details`, updateLeagueEventDetails);

/** Hide the wrapped league event. */
const hideLeagueEvent = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy
            .get(`#leagueEventForm${leagueEvent.league_event_id}`)
            .within(() => {
                cy
                    .findByRole('link', { name: /visible/i })
                    .click();
            });
    });
};
When(`I hide the league event`, hideLeagueEvent);

/** See league event dates for wrapped league event. */
const seeLeagueEventDates = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy
            .get(`#leagueEventForm${leagueEvent.league_event_id}`)
            .within(() => {
                cy
                    .findByRole('link', { name: /see dates/i})
                    .click();
            });
    });
};
When(`see dates for the league event`, seeLeagueEventDates);

/** Enter league event date. */
const enterLeagueEventDate = () => {
    const eventDate = generateLeagueEventDate();
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy
        .get(`#leagueEventDateForm`)
        .within(() => {
            cy.get(`input[type="date"]`).type(eventDate.date);
            cy.get(`input[type="time"]`).type(eventDate.time);
            cy.findByRole('button', { name: /create/i }).click();
        });
        
    });
};
When(`I enter a new date`, enterLeagueEventDate);

/** Click update for the wrapped league event. */
const updateLeagueEvent = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((event: LeagueEvent) => {
        cy
            .get(`#leagueEventForm${event.league_event_id}`)
            .within(() => {
                cy
                    .findByRole('button', { name: /update/i })
                    .click();
            });
    });
};
When(`I click update`, updateLeagueEvent);

/** Click submit for a new eventupdate for the wrapped league event. */
const submitLeagueEvent = () => {
    cy
        .get(`#leagueEventFormNew`)
        .within(() => {
            cy
                .findByRole('button', { name: /create/i })
                .click();
        });
};
When(`I submit league event`, submitLeagueEvent);

/** Update an image for the league event */
const uploadLeagueEventImage = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((event: LeagueEvent) => {
        cy.fixture('test.png', null).as('TestImage');
        cy
            .get(`#leagueEventForm${event.league_event_id}`)
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
}
When(`I upload an image to the league event`, uploadLeagueEventImage);

/** Assert the wrapped league event is hidden. */
const assertLeagueEventHidden = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((leagueEvent: LeagueEvent) => {
        cy
        .get(`#leagueEventForm${leagueEvent.league_event_id}`)
        .within(() => {
            cy
                .findByRole('link', { name: /hidden/i })
                .should('be.visible');
        });
    });
};
Then(`I see league event is hidden`, assertLeagueEventHidden);

/** Assert the league event image was added. */
const assertLeagueEventImage = () => {
    cy.get<LeagueEvent>('@leagueEvent').then((event: LeagueEvent) => {
        cy
            .get(`#leagueEventForm${event.league_event_id}`)
            .within(() => {
                cy
                    .findByRole('img')
                    .should('have.attr', 'src')
                    .should('include', 'test.png');
            });
    });
};
Then(`I see the event image`, assertLeagueEventImage);