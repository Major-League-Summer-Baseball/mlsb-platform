#!/bin/bash
export FLASK_ENV=development
# Make oauth accept http instead of only https
export OAUTHLIB_INSECURE_TRANSPORT=1
export OAUTHLIB_RELAX_TOKEN_SCOPE=1
export DATABASE_URL=postgresql://postgres:postgres@localhost/mlsb-development
export SECRET_KEY=someSecret
# github for apps running on localhost:5000
export GITHUB_OAUTH_CLIENT_ID=45b9836c16725952ffa0
export GITHUB_OAUTH_CLIENT_SECRET=707f0871e1b02f6f51891191143cbb2d8b65bd43
