'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Holds the authentication functions
'''
from typing import TypedDict
from functools import wraps
from sqlalchemy.sql import func, and_
from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import LoginManager, current_user, login_user
from flask import request, Blueprint, session, Response
from api.model import DB, Player, OAuth, JoinLeagueRequest
from api.errors import OAuthException, NotPartOfLeagueException,\
    HaveLeagueRequestException
from api.logging import LOGGER
import os


ADMIN = os.environ.get('ADMIN', 'admin')
PASSWORD = os.environ.get('PASSWORD', 'password')

login_manager = LoginManager()
login_manager.login_view = "loginpage"

github_blueprint = make_github_blueprint(
    scope=["email"],
    storage=SQLAlchemyStorage(OAuth, DB.session, user=current_user)
)
facebook_blueprint = make_facebook_blueprint(
    scope=["email"],
    storage=SQLAlchemyStorage(OAuth, DB.session, user=current_user))
google_blueprint = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuth, DB.session, user=current_user))
FACEBOOK = "facebook"
GOOGLE = "google"
GITHUB = "github"


class UserInfo(TypedDict):
    """The required user info from a ouath provider"""
    name: str
    email: str


@oauth_authorized.connect_via(facebook_blueprint)
@oauth_authorized.connect_via(github_blueprint)
@oauth_authorized.connect_via(google_blueprint)
def oauth_service_provider_logged_in(blueprint: Blueprint, token: str) -> bool:
    """The handler for dealing when OAuth has logged someone in correctly

    Args:
        blueprint (Blueprint): the OAuth provider they logged into
        token (str): the token received from provider

    Raises:
        OAuthException: when missing vital information like token or email
        HaveLeagueRequestException: when they have already request to join

    Returns:
        bool: False - Disable Flask-Dance's default behavior for saving
                      the OAuth token
    """
    # ensure the token is correct
    if not token:
        LOGGER.warning(f"{blueprint.name} did not send token: {token}")
        raise OAuthException("Failed to log in")

    # get the user info
    user_info = get_user_info(blueprint)
    user_id = user_info["id"]

    # user user info to lookup oauth
    oauth = get_oauth(blueprint.name, user_id, token)
    if oauth.player:
        login_user(oauth.player)
        LOGGER.info(f"{oauth.player} signed in")
    else:
        # remember their email in session in case they want to join
        session["oauth_email"] = user_info["email"]
        # check if they have a pending request
        is_pending = JoinLeagueRequest.query.filter(
            and_(JoinLeagueRequest.email == session["oauth_email"],
                 JoinLeagueRequest.pending == True
                )).first()
        if is_pending is not None:
            raise HaveLeagueRequestException()
        # see if they part of the legaue
        player = find_player(user_info)
        # associated the player with this oauth
        oauth.player = player
        DB.session.add(oauth)
        DB.session.commit()
        LOGGER.info(f"{player} has joined the app")
        login_user(oauth.player)
    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


@oauth_error.connect_via(facebook_blueprint)
def oauth_service_provider_error(blueprint: Blueprint,
                                 message: str,
                                 response: dict):
    """Got an error from the OAuth service provider

    Args:
        blueprint (Blueprint): the OAuth service provider
        message (str): the message from the provider
        response (dict): the response from the provider

    Raises:
        OAuthException: the exceptionr raised to be dealt with by application
    """
    msg = f"{blueprint.name}! message={message} response={response}"
    LOGGER.error(msg)
    raise OAuthException(msg)


@login_manager.user_loader
def load_user(player_id: int) -> Player:
    """Loads the logged in user based upon their id."""
    return Player.query.get(int(player_id))


def get_oauth(name: str, user_id: str, token: str) -> OAuth:
    """Get the oauth associated with the given user id and oauth provider.

    Args:
        name (str): the name of the oauth provider
        user_id (str): the id of the user according to oauth provider
        token (str): the oauth token

    Returns:
        OAuth: the oauth that we have saved or newly created one
    """
    # Find this OAuth token in the database, or create it
    user_id = str(user_id)
    query = OAuth.query.filter_by(provider=name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=name, provider_user_id=user_id, token=token)
    return oauth


def get_user_info(blueprint: Blueprint) -> UserInfo:
    """Get the user info from the oauth provider.

    Args:
        blueprint (Blueprint): the oauth provider blueprint

    Raises:
        OAuthException: Unsupported blueprint or unable to get user info

    Returns:
        UserInfo: the user info
    """
    resp = None
    if blueprint.name == FACEBOOK:
        resp = blueprint.session.get("/me?fields=id,email")
    elif blueprint.name == GOOGLE:
        resp = blueprint.session.get("/oauth2/v1/userinfo")
    elif blueprint.name == GITHUB:
        resp = blueprint.session.get("user")
    if resp is None:
        LOGGER.error(f"Unsupported oauth blueprint: {blueprint.name}")
        raise OAuthException(f"Unsupported oauth blueprint: {blueprint.name}")
    if not resp.ok:
        LOGGER.error(resp)
        LOGGER.error(f"Unable to fetch user using {blueprint.name}")
        raise OAuthException(
            f"Failed to get user info oauth blueprint: {blueprint.name}")
    user_info = resp.json()
    if user_info.get("email") is None:
        msg = (
            f"Provider did not give email: {blueprint.name}."
            " Double check your permission from the app."
            " If using Github ensure your email is public."
        )
        LOGGER.error(msg)
        LOGGER.error(user_info)
        raise OAuthException(msg)
    return user_info


def find_player(user_info: UserInfo) -> Player:
    """Find the player associated with the user info.

    Args:
        user_info (UserInfo): the user info

    Raises:
        NotPartOfLeagueException: if the user not part of league

    Returns:
        Player: the player in the legaue
    """
    email = user_info.get('email')
    players = DB.session.query(Player).filter(
        func.lower(Player.email) == email.lower()).all()
    if len(players) == 0:
        LOGGER.info(f"{email} is not part of league right now")
        raise NotPartOfLeagueException(
            "Sorry, looks like you are not in the league")
    return players[0]


def are_logged_in() -> bool:
    """Returns whether the person is logged in."""
    return current_user.get_id() is not None


def get_login_email() -> str:
    """Returns the email based whichever app they have authorized with."""
    return None if not are_logged_in() else current_user.email


def is_gmail_supported() -> bool:
    """Returns whether current setup support Gmail authentication."""
    return os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "") != ""


def is_github_supported() -> bool:
    """Returns whether current setup support Github authentication."""
    return os.environ.get("GITHUB_OAUTH_CLIENT_ID", "") != ""


def is_facebook_supported() -> bool:
    """Returns whether current setup support Facebook authentication."""
    return os.environ.get("FACEBOOK_OAUTH_CLIENT_ID", "") != ""


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == ADMIN and password == PASSWORD


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        elif 'admin' in session and 'password' in session:
            # check if user signed in already
            logged = check_auth(session['admin'], session['password'])
            if not logged:
                return authenticate()
        return f(*args, **kwargs)
    return decorated
