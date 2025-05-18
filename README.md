# mlsb-platform

[![codecov](https://codecov.io/gh/Major-League-Summer-Baseball/mlsb-platform/branch/master/graph/badge.svg?token=NeZW0H7wRa)](https://codecov.io/gh/Major-League-Summer-Baseball/mlsb-platform)

A platform for mlsb

See the the Wiki Pages for [help](https://github.com/fras2560/mlsb-platform/wiki)

**Assumed Dependencies**:

* python 3
* pip

## Getting Started

### TLDR

```bash
pip install -r requirements.txt
export FLASK_ENV=development
python -m flask --app api/app run --host=0.0.0.0 --debug
# to run pytests
pytest
# to run a particular grouping
pytest api/tests/<FOLDER>
# run flake linter
pip install flake8
flake8 . --count --max-complexity=20 --max-line-length=127 --statistics --exclude=api/__init__.py,api/tqdm.py,api/commands.py,api/app.py,venv/*,ui-testing/*,api/tests/conftest.py,api/model.py --ignore=E712,W503,W504,C901

```

This will use an in-memory database and in-memory cache. To actually test
with a PostGres database or Redis cache one just needs to setup the appropriate
environment variables. Additionally one could use docker as well.

### Virtual Environment

It is recommend to use a virtual environment when developing different apps. This allows for dependencies to be kept separate from each other. `virtualenv` is one good choice when using a virtual environment. See [how to install](https://virtualenv.pypa.io/en/latest/installation.html). Once install one can use the following:

```bash
# Linux
virtualenv venv # create virutal environment, usually do this inside app folder
source venv/bin/activate # activate the virtual environment
... # use virtual environment - install depenendencies and start flask server
deactivate # to deactivate the virtual environment
```

```windows
# windows
virtualenv venv # create virutal environment, usually do this inside app folder
venv\Scripts\activate.bat # activate the virtual environment
... # use virtual environment - install depenendencies and start flask server
deactivate # to deactivate the virtual environment
```

## Environment Variables

The following variables are used by mlsb-platform and the defaults are in
brackets:

* DATABASE_URL: the postgres database to connect to ("sqlite://")
* SECRET_KEY:a secret key used by Flask (randomly generated uuid)
* REDIS_URL: the redis database to use for caching (uses simple cache)
* FLASK_ENV: whether running in development or production (no default)
* AWS_ACCESS_KEY_ID: the access key id for the image storage (no default)
* AWS_SCRET_ACCESS_KEY: the secret key for the image storage (no default)
* AWS_REGION: the region for the image storage (no default)
* AWS_ENDPOINT: the url to the image storage (no default)
* BUCKET_NAME: the name of the bucket for the image storage (no default)
The app does expect the the postgres database has had the tables initiated. To intiated the datbase can use

```bash
python -m flask --app api/app init-db --create
```

Local development will default the image storage to the pictures folder in the static folder. All the AWS variables need to be specified for app to use an external image storage.

## Developing Using Docker

The platform can also be developed locally with Docker. For a simple docker setup one can do

```bash
# build the docker image
docker-compose build
# bring the container up
docker-compose up -d
# wait a few seconds and then init the database
docker-compose exec mlsb python -m flask --app api/app init-db --create
```

The app should be available at `http://localhost:8080`. If you need to chage the port change
in the `docker-compose.yml` line 13 from 8080:8080 to `<PORT>`:8080.
The docker-compose will use the above specified environment variables if they are present.
However, if they are missing is will just defaults but will use redis and postgres
(instead of in-memory database / simple cache).
The flask app will restart anytime changes are made to the app source code since docker-compose use a volume
between the docker container and the code repository.
Just a note about the DATABASE_URL if using docker and want your database
to be some database on your local machine then do not use localhost but
instead use your local IP address.

To bring the docker stack down just use the following:

```bash
docker-compose down
# (remove volumes)
docker system prune --volumes --force
```

### Running unit tests in docker

To run the whole suite of tests use:

```bash
docker-compose exec mlsb python -m pytest
```

To run a particular test suite use:

```bash
docker-compose exec mlsb python -m pytest api/tests/<FOLDER>
```

## Documentation/Style

All APIs are document in html and can be found by going to
`http://localhost:5000/documentation`. If one is to add an API then it
is expected they add an HTML page that documents it.
The style for how one is to be documented is still open for discussion.

As for style it is recommended that one uses flake8 for checking style. The
following commands can help get feedback about any incorrect styling issues.

```bash
pip install flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-complexity=20 --max-line-length=127 --statistics --exclude=api/__init__.py,venv/*,cypress-testing/* --ignore=E712,W503,W504
```

## Github Actions

There is one Github action that runs against pushes to main and development. Additionlly ran when a pull-request is open targeting main and development. It does the following:

* Checks lint issues with flake8
* Runs pytests and creates a coverage report (artifact)
* Runs Cypress UI Tests and video report (artifact)

Additionally there are two Github actions for main and development that deploys them on a commit. They are currently being deployed to fly.IO

Finally, there is a Github action for creating a docker image for pushes to main and development. No real use of the docker images at this moment.

## Flask Commands

```bash
# list all routes for app
flask --app api/app routes
# import a season stats from csv
flask --app api/app import-season <league_name> <division_name> <year> <SPONSOR_CSV_FILE> <TEAM_STANDINGS_CSV_FILE> <HOMERUNS_CSV_FILE> <SPECIAL_SINGLES_CSV_FILE>
```

## Fly IO Commands

```bash
# connect to production app database
flyctl proxy 15432:5432 -a mlsb-development-db
# set environment variable (development - change for production)
flyctl secrets set SOMEVARIABLE=SOMEVALUE --app mlsb
# deploy to some enviroment(development - change for production)
flyctl deploy --config ./deployments/fly-development.toml
# check production certificates
flyctl certs list --app mlsb
# check specific certificate
flyctl certs show mlsb.ca --app mlsb
```

## Production Architecture

### Files/Image Storage

Both the staging and production apps use Tigris to store the images/files. It still uses the pictures folder to save the file before uploading to Tigris. The urls to Tigris are stored in Image database table. Images are used for sponsors, teams and league events.

Tigris can be accessed by going to Fly.io and the left-hand side there is Tigris Object Storage option. Clicking that will take ones to Tigris and can see all the images.
