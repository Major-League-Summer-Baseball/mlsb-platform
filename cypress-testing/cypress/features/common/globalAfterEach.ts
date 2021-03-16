/** A hook that runs once after each test. */
const globalAfterEach = (): void => {
    cy.log('Runs after each test');
};
afterEach(globalAfterEach);
