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

# Running Using Docker
TODO

# Additional Sources
TODO