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
-   `npm run docs`: generates a documentation report in folder `/docs`
-   `npm run open`: opens the Cypress app for running feature files
-   `npm run test`: runs all the features file from the command line
-   `npm run test:chrome`: runs all the features file from the command line using Chrome browser
-   `npm run test:firefox`: runs all the features file from the command line using Firefox browser
-   `npm run checkLint`: checks if there are any linting issues

Note: When running the tests from command line it will not run any with @ignore.

# Environment Variables
The following variables are used by Cypress during testing:

* `CYPRESS_baseUrl` : the URL of the MLSB instance under test (requied, example: `http://localhost:5000/` )
* `ADMIN`: the admin username
* `PASSWORD`: the admin password

# Path Aliases

To avoid long relative paths like `../../../models` as set of aliases can be used. The following are the current aliases setup:

-   `@Models`: holds a list of testing models
-   `@Pages`: holds a collection of pages (abstraction for interacting with a page)
-   `@Support`: holds collection of functions and classes to deal with making requests to WJL and its OAuth Providers
-   `@Common`: holds common steps and functionaly that is common between multiple features

Now one can use aliases to import a model using:

```
import {User} from '@Models/user.js';
```

If one wants to add a user edit `webpack.config.js` and `tsconfig.json`.


# Documentation/Style

Everything in this project is documented with [Typedoc](https://typedoc.org/). To produce the code documentation use `npm run docs` and that will produce a high-level report leaving out anything marked as internal. To produce a full-report with more details use `npm run full-docs`. The code documentation provides a good over view and is recommended reading.

To get a better understanding of typedoc read abouts its supported tag [here](https://typedoc.org/guides/doccomments/).


# Feature Files and Steps
This project uses a [cucumber plugin](https://github.com/TheBrainFamily/cypress-cucumber-preprocessor#readme). The config file for the plugin is inside `package.json`. The big difference with the current setup is that steps are only scoped for each feature file. So for example `login.feature` will only look for step definitions inside the folder login. The only exception is that the common folders holds global step definitions. 

# Tips and Tricks
TODO EXPLAIN HOW TO INCORPORATE INTO THE PIPELINE


# Limitations
* Cypress does not support multiple windows [never allowed](https://docs.cypress.io/guides/references/trade-offs.html#Multiple-tabs)
* Cypress only allows test to visit [one domain](https://docs.cypress.io/guides/references/trade-offs.html#Same-origin)

# TODO
* Start implementing/updating old feature files

# Additional Sources
*   [Cypress](https://docs.cypress.io/guides/overview/why-cypress.html#In-a-nutshell) - documentation for Cypress
*   [ESlint](https://eslint.org/) - the linter used for this project
*   [TypeScript](https://www.typescriptlang.org/) - a super set of JavaScript
*   [Typedoc](https://typedoc.org/) - Typescript documentation
