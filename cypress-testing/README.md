# Testing MLSB with Cypress and Cucumber

This sub-project to explore testing MLSB-platform in the browser with [Cypress](https://www.cypress.io/).

**Assumed Dependencies**:
* npm

# Getting Started
**TLDR**
```
npm install
export ADMIN=<ADMIN_USERNAME>
export PASSWORD=<PASSWORD>
# needed if mlsb url is not http://localhost:5000/
export CYPRESS_baseUrl=<YOUR_MLSB_URL>
# open the cypress app
npm run-script open
```

**Cheat list of commands**
* `npm run docs`: generates a documentation report in folder `/docs`
* `npm run open`: opens the Cypress app for running feature files
* `npm run test`: runs all the features file from the command line
* `npm run test:all`: runs all the features file but saves some time by merging them all into one

# Environment Variables
The following variables are used by Cypress during testing:

* `CYPRESS_baseUrl` : the URL of the MLSB instance under test (requied, example: `http://localhost:5000/` )
* `ADMIN`: the admin username
* `PASSWORD`: the admin password

# Documentation/Style
Everything in this project is documented with [JsDoc](https://devdocs.io/jsdoc/).To produce the code documentation use `npm run docs` and that will produce a high-level report of all public functions/methods. To produce a report with more details use `npm run full-docs`. The code documentation provides a good over view and its recommended that one reads it before starting development. It will provide understanding of scoping of steps and how the hooks work.

# Feature Files and Steps
This project uses a [cucumber plugin](https://github.com/TheBrainFamily/cypress-cucumber-preprocessor#readme). The config file for the plugin is inside `package.json`. The big difference with the current setup is that steps are only scoped for each feature file. So for example `login.feature` will only look for step definitions inside the folder login. The only exception is that the common folders holds global step definitions. 

# Tips and Tricks
### Retry Clicks
Cypress for get will retry until the element is found and `should` command is met. However
the click command does retry. However, there is a nice plugin command called `pipe`. This allows one
to able to click until a certain condition to be met.

The one important note about this command is the function that is **pipe cannot include cy commands**.
Can read more about it at [Pipe](https://github.com/NicholasBoll/cypress-pipe)

# Pipeline Incorpation
TODO EXPLAIN HOW TO INCORPORATE INTO THE PIPELINE


# Limitations
* Cypress does not support FF or IE (on their [road map](https://github.com/cypress-io/cypress/pull/1359))
* Cypress does not support multiple windows [never allowed](https://docs.cypress.io/guides/references/trade-offs.html#Multiple-tabs)
* Cypress only allows test to visit [one domain](https://docs.cypress.io/guides/references/trade-offs.html#Same-origin)

# TODO
* Start implementing/updating old feature files

# Additional Sources
 * [Cypress](https://docs.cypress.io/guides/overview/why-cypress.html#In-a-nutshell) - documentation for Cypress
 * [JsDoc](https://devdocs.io/jsdoc/) - Javascript documentation
 * [Pipe](https://github.com/NicholasBoll/cypress-pipe) - a plugin added for retrying commands