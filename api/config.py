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
    SERVER_NAME = os.environ.get("SERVER_NAME", None)
    TESTING = os.environ.get("TESTING", False)
    SECRET_KEY = os.environ.get("SECRET_KEY", str(uuid1()))
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True
    }
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_ENDPOINT_URL_S3 = os.environ.get("AWS_ENDPOINT_URL_S3", "")
    AWS_REGION = os.environ.get("AWS_REGION", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    BUCKET_NAME = os.environ.get("BUCKET_NAME", "")
    AZURE_OAUTH_CLIENT_ID = os.environ.get("AZURE_OAUTH_CLIENT_ID", "")
    AZURE_OAUTH_CLIENT_SECRET = os.environ.get("AZURE_OAUTH_CLIENT_SECRET", "")
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
    RESTX_MASK_SWAGGER = False
    REDIS_CACHE = ({'CACHE_TYPE': 'simple'}
                   if os.environ.get("REDIS_URL", None) is None
                   else {'CACHE_TYPE': 'redis',
                         'CACHE_REDIS_URL': os.environ.get("REDIS_URL")})
