# mlsb-platform
A platform for mlsb

See the the Wiki Pages for [help](https://github.com/fras2560/mlsb-platform/wiki)

**Assumed Dependencies**:
* python 3
* pip

# Getting Started
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

# Environment Variables
The following variables are used by mlsb-platform and the defaults are in
brackets:
* ADMIN: the admin's user name ("admin") 
* PASSWORD: the admin password ("password")
* DATABASE_URL: the postgres database to connect to ("sqlite://")
* SECRET_KEY:a secret key used by Flask (randomly generated uuid)
* REDIS_URL: the redis database to use for caching (uses simple cache)

The app does expect the the postgres database has had the tables initiated. To intiated the datbase can use
```
python initDB.py -createDB -mock
```
# Developing Using Docker
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

To bring the docker stack down just use the following:
```
docker-compose down
# (remove volumes)
docker system prune --volumes --force
```

# Documentation/Style
All APIs are document in html and can be found by going to
"http://localhost:5000/documentation". If one is to add an API then it
is expected they add an HTML page that documents it.
The style for how one is to be documented is still open for discussion.

As for style it is recommended that one uses flake8 for checking style. The
following commands can help get feedback about any incorrect styling issues.

```
pip install flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=api/__init__.py,api/website/views.py
```

# Github Actions
Working on Github actions. For now it will run unittests and styling issues
on PRs to Development and Master. Additionally, might work on a Cypress project
for ensuring checkin whether development server on Heroku is working as
expected.

# Additional Sources
TODO
