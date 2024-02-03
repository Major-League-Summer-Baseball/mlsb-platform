# Testing MLSB with Cypress and Cucumber

This sub-project to explore testing MLSB-platform in the browser with [Cypress](https://www.cypress.io/).

**Assumed Dependencies**:

* npm

## Getting Started

### TLDR

```bash
npm install
export ADMIN=<ADMIN_USERNAME>
export PASSWORD=<PASSWORD>
# needed if mlsb url is not http://localhost:5000/
export CYPRESS_baseUrl=<YOUR_MLSB_URL>
# open the cypress app
npm run-script cypress:test
```

#### Cheat list of commands

* `npm run cypress:open`: opens the Cypress app for running feature files
* `npm run cypress:test`: runs all the features file from the command line

Note: When running the tests from command line it will not run any with @ignore.

## Environment Variables

The following variables are used by Cypress during testing:

* `CYPRESS_baseUrl` : the URL of the MLSB instance under test (requied, example: `http://localhost:5000/` )
* `ADMIN`: the admin username
* `PASSWORD`: the admin password

## Feature Files and Steps

This project uses a [cucumber plugin](https://github.com/badeball/cypress-cucumber-preprocessor). The config file for the plugin is inside `package.json`. The big difference with the current setup is that steps are only scoped for each feature file. So for example `login.feature` will only look for step definitions inside the folder login. The only exception is that the global folder holds step definitions available anywhere. 

## Limitations

* Cypress does not support multiple windows [never allowed](https://docs.cypress.io/guides/references/trade-offs.html#Multiple-tabs)
* Cypress only allows test to visit [one domain](https://docs.cypress.io/guides/references/trade-offs.html#Same-origin)

## Additional Sources

* [Cypress](https://docs.cypress.io/guides/overview/why-cypress.html#In-a-nutshell) - documentation for Cypress
* [TypeScript](https://www.typescriptlang.org/) - a super set of JavaScript
