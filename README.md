[![codecov](https://codecov.io/gh/Major-League-Summer-Baseball/mlsb-platform/branch/master/graph/badge.svg?token=NeZW0H7wRa)](https://codecov.io/gh/Major-League-Summer-Baseball/mlsb-platform)

# mlsb-platform
A platform for mlsb

See the the Wiki Pages for [help](https://github.com/fras2560/mlsb-platform/wiki)

**Assumed Dependencies**:
* python 3
* pip


## Getting Started
**TLDR**
```
pip install -r requirements.txt
python runserver.py
# to run unittests
python -m unittest discover -s api/test
# want to run one suite
python -m unittest discover -s api/test -p <TEST_SUITE>.py
```
This will use an in-memory database and in-memory cache. To actually test
with a PostGres database or Redis cache one just needs to setup the appropriate
environment variables. Additionally one could use docker as well.

### Virtual Environment
It is recommend to use a virtual environment when developing different apps. This allows for dependencies to be kept separate from each other. `virtualenv` is one good choice when using a virtual environment. See [how to install](https://virtualenv.pypa.io/en/latest/installation.html). Once install one can use the following:
```
# Linux
virtualenv venv # create virutal environment, usually do this inside app folder
source venv/bin/activate # activate the virtual environment
... # use virtual environment - install depenendencies and start flask server
deactivate # to deactivate the virtual environment
```
```
# windows
virtualenv venv # create virutal environment, usually do this inside app folder
venv\Scripts\activate.bat # activate the virtual environment
... # use virtual environment - install depenendencies and start flask server
deactivate # to deactivate the virtual environment
```

## Environment Variables
The following variables are used by mlsb-platform and the defaults are in
brackets:
* ADMIN: the admin's user name ("admin") 
* PASSWORD: the admin password ("password")
* DATABASE_URL: the postgres database to connect to ("sqlite://")
* SECRET_KEY:a secret key used by Flask (randomly generated uuid)
* REDIS_URL: the redis database to use for caching (uses simple cache)
* FLASK_ENV: whether running in development or production (no default)

The app does expect the the postgres database has had the tables initiated. To intiated the datbase can use
```
python initDB.py -createDB -mock
```
## Developing Using Docker
The platform can also be developed locally with Docker. For a simple docker setup one can do
```
# build the docker image
docker-compose build
# bring the container up
docker-compose up -d
# wait a few seconds and then init the database
docker-compose exec mlsb python initDB.py -createDB -mock
```
The app should be available at `http://localhost:8080`. If you need to chage the port change
in the `docker-compose.yml` line 13 from 8080:8080 to <PORT>:8080.
The docker-compose will use the above specified environment variables if they are present.
However, if they are missing is will just defaults but will use redis and postgres
(instead of in-memory database / simple cache).
The flask app will restart anytime changes are made to the app source code since docker-compose use a volume
between the docker container and the code repository.
Just a note about the DATABASE_URL if using docker and want your database
to be some database on your local machine then do not use localhost but
instead use your local IP address. 


To bring the docker stack down just use the following:
```
docker-compose down
# (remove volumes)
docker system prune --volumes --force
```

### Running unit tests in docker
To run the whole suite of tests use:
```
docker-compose exec mlsb python -m unittest discover -s api/test -p test*.py
```
To run a particular test suite use:
```
docker-compose exec mlsb python -m unittest discover -s api/test -p <TEST_SUITE>.py
```

## Documentation/Style
All APIs are document in html and can be found by going to
"http://localhost:5000/documentation". If one is to add an API then it
is expected they add an HTML page that documents it.
The style for how one is to be documented is still open for discussion.

As for style it is recommended that one uses flake8 for checking style. The
following commands can help get feedback about any incorrect styling issues.

```
pip install flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-complexity=20 --max-line-length=127 --statistics --exclude=api/__init__.py,venv/*,cypress-testing/* --ignore=E712,W503,W504
```

## Github Actions
There is one Github action that runs against pushes to main and development. Additionlly ran when a pull-request is open targeting main and development. It does the following:
* Checks lint issues with flake8
* Runs unittests and creates a coverage report (artifact)
* Runs Cypress UI Tests and video report (artifact)
 
Additionally there are two Github actions for main and development that deploys them on a commit. They are currently being deployed to fly.IO

Finally, there is a Github action for creating a docker image for pushes to main and development. No real use of the docker images at this moment.

## Fly IO Commands
```
# connect to production app database
flyctl proxy 15432:5432 -a mlsb-development-db
# set environment variable (development - change for production)
flyctl secrets set SOMEVARIABLE=SOMEVALUE --config ./deployments/fly-development.toml
# deploy to some enviroment(development - change for production)
flyctl deploy --config ./deployments/fly-development.toml
# check production certificates
flyctl certs list --config ./deployments/fly-production.toml
# check specific certificate
flyctl certs show mlsb.ca --config ./deployments/fly-production.toml
```
