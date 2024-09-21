from flask import Flask, request
from api.config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from api.extensions import cache, DB, login_manager, tailsman, ckeditor
from api.authentication import github_blueprint, facebook_blueprint,\
    google_blueprint, azure_blueprint, login_manager
from api.website import website_blueprint
from api.convenor import convenor_blueprint
from api.testing_blueprint import testing_blueprint
from api.mock_database import init_database
from api.commands import database_command
import logging
import sys


def configure_app(app):
    """Configure the app."""
    app.config.from_object(Config)
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    app.config['UPLOAD_FOLDER'] = "./static"


def register_error_handlers(app):
    """Register error handlers"""
    with app.app_context():
        from api.errors_handler import \
        handle_existing_league_request, handle_not_part_of_league,\
        handle_generic_error, unhandled_generic_error


def register_extensions(app):
    """Register all flask extensions."""
    cache.init_app(app)
    DB.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    app.config['CKEDITOR_PKG_TYPE'] = 'full'
    if not is_development(app):
        csp = {
            'default-src': [
                '\'self\'',
                'oss.maxcdn.com',
                'fonts.googleapis.com',
                'cdn.datatables.net',
                'cdn.jsdelivr.net',
                'd3js.org',
                'www.google-analytics.com',
                'stats.g.doubleclick.net',
                'www.googletagmanager.com',
                'maxcdn.bootstrapcdn.com',
                'ajax.googleapis.com',
                #TODO: Move all inline scripts to file
                '\'unsafe-inline\'',
                
            ],
            'frame-src': [
                '\'self\'',
                'youtube.com',
                'www.youtube.com',
                'maps.google.ca',
                'www.google.com',
            ],
            'object-src': '\'none\'',
            'font-src': [
                '\'self\'',
                'fonts.gstatic.com',
                'maxcdn.bootstrapcdn.com',
                'fonts.googleapis.com',
            ]
        }
        tailsman.init_app(app, content_security_policy=None)
        app.wsgi_app = ProxyFix(app.wsgi_app)
    else: 
        app.register_blueprint(testing_blueprint)

    @app.after_request
    def add_cors(resp):
        """ Ensure all responses have the CORS headers.
            This ensures any failures are also accessible
            by the client.
        """
        resp.headers['Access-Control-Allow-Origin'] = request.headers.get(
            'Origin', '*')
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
        t = 'Access-Control-Allow-Headers'
        resp.headers[t] = request.headers.get(
            'Access-Control-Request-Headers', 'Authorization')
        # set low for debugging
        if app.debug:
            resp.headers['Access-Control-Max-Age'] = '1'
        return resp


def register_blueprint(app):
    """Register all blueprints for the app."""
    app.register_blueprint(github_blueprint, url_prefix="/login")
    app.register_blueprint(facebook_blueprint, url_prefix="/login")
    app.register_blueprint(google_blueprint, url_prefix="/login")
    app.register_blueprint(azure_blueprint, url_prefix="/login")
    app.register_blueprint(website_blueprint)
    app.register_blueprint(convenor_blueprint)


def register_commands(app):
    """Register command line tasks."""
    app.cli.add_command(database_command)


def configure_logger(app):
    """Configure loggers."""
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)


def register_apixs(app):
    """Register all the apis for restx."""
    from api.restx import apiX
    apiX.init_app(app)


def is_memory_database(url: str) -> bool:
    """Returns whether the database is in memory database."""
    return url.strip().lower() == "sqlite://"


def is_development(app) -> bool:
    """Returns whether the app is in development mode."""
    return app.config["TESTING"] or app.config["DEBUG"]

def create_app():
    app = Flask(__name__)
    configure_app(app)
    configure_logger(app)
    register_error_handlers(app)
    register_blueprint(app)
    register_extensions(app)
    register_apixs(app)
    register_commands(app)
    need_database = is_memory_database(app.config["URL"])
    print(f"Need database: {need_database}")
    if is_memory_database(app.config["URL"]) and is_development(app):
        # if development with no db url use an in memory database
        # so must initialize it
        print("Init memory DB")
        with app.app_context():
            init_database(True, True)
    return app


