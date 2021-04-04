# -*- coding: utf-8 -*-
"""Holds configuration for the app."""
import os
from uuid import uuid1

DB_URL = os.environ.get('DATABASE_URL', "sqlite://")
# Heroku uses postgres but SQL Alchhemy requires full dialect of postgresql
DB_URL = (DB_URL.replace("postgres://", "postgresql://")
    if DB_URL.startswith("postgres://") else DB_URL)


class Config(object):
    URL = DB_URL
    SECRET_KEY = os.environ.get("SECRET_KEY", str(uuid1()))
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get(
        "GOOGLE_OAUTH_CLIENT_SECRET", "")
    FACEBOOK_OAUTH_CLIENT_ID = os.environ.get("FACEBOOK_OAUTH_CLIENT_ID", "")
    FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get(
        "FACEBOOK_OAUTH_CLIENT_SECRET", "")
    GITHUB_OAUTH_CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID", "")
    GITHUB_OAUTH_CLIENT_SECRET = os.environ.get(
        "GITHUB_OAUTH_CLIENT_SECRET", "")
    USE_SESSION_FOR_NEXT = True
    ARE_TESTING = os.environ.get("ARE_TESTING", False)
    REDIS_CACHE = ({'CACHE_TYPE': 'simple'}
        if os.environ.get("REDIS_URL", None) is None
        else {'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': os.environ.get("REDIS_URL")})
