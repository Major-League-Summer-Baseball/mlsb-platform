from typing import TypedDict, Callable
from functools import wraps
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.azure import make_azure_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import LoginManager, current_user, login_user
from flask import request, Blueprint, session, Response, redirect, \
    url_for
from api.extensions import DB
from api.model import Player, OAuth, JoinLeagueRequest, Team
from api.errors import OAuthException, NotPartOfLeagueException, \
    HaveLeagueRequestException, NotTeamCaptain, TeamDoesNotExist,\
    NotLeagueConvenor
from api.logging import LOGGER
import os


ADMIN = os.environ.get('ADMIN', 'admin')
PASSWORD = os.environ.get('PASSWORD', 'password')

login_manager = LoginManager()
login_manager.login_view = "website.loginpage"

github_blueprint = make_github_blueprint(
    scope=["email"],
    storage=SQLAlchemyStorage(OAuth, DB.session, user=current_user)
)
azure_blueprint = make_azure_blueprint(
    scope=["user.read"],
    storage=SQLAlchemyStorage(OAuth, DB.session, user=current_user)
)
facebook_blueprint = make_facebook_blueprint(
    scope=["email"],
    storage=SQLAlchemyStorage(OAuth, DB.session, user=current_user)
)
google_blueprint = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuth, DB.session, user=current_user)
)
FACEBOOK = "facebook"
GOOGLE = "google"
GITHUB = "github"
AZURE = "azure"


class UserInfo(TypedDict):
    """The required user info from a ouath provider"""
    name: str
    email: str


class TeamAuthorization(TypedDict):
    """The authorization the user has relative to a team."""
    on_team: bool
    is_convenor: bool
    is_captain: bool
    pending_request: bool


@oauth_authorized.connect_via(azure_blueprint)
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
        is_pending = JoinLeagueRequest.find_request(session["oauth_email"])
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
    elif blueprint.name == AZURE:
        resp = blueprint.session.get("/v1.0/me")
    if resp is None:
        LOGGER.error(f"Unsupported oauth blueprint: {blueprint.name}")
        raise OAuthException(f"Unsupported oauth blueprint: {blueprint.name}")
    if not resp.ok:
        LOGGER.error(resp)
        LOGGER.error(f"Unable to fetch user using {blueprint.name}")
        raise OAuthException(
            f"Failed to get user info oauth blueprint: {blueprint.name}")
    user_info = resp.json()
    if user_info.get("mail"):
        # azure sets mail instead of email
        user_info["email"] = user_info.get("mail")
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


def get_user_information() -> dict:
    """Returns information about the logged in user."""
    logged_in = are_logged_in()
    teams = get_player_teams()
    player_id = get_player_id()
    is_captain = False if teams is None else any(
        team['captain'] is not None and
        team['captain']['player_id'] == player_id for team in teams
    )
    return {
        'logged_in': logged_in,
        'email': get_login_email(),
        'player_information': get_player_information(),
        'teams': teams,
        'captain': is_captain
    }


def are_logged_in() -> bool:
    """Returns whether the person is logged in."""
    return current_user.get_id() is not None


def get_login_email() -> str:
    """Returns the email based whichever app they have authorized with."""
    return None if not are_logged_in() else current_user.email


def get_player_id() -> int:
    """Returns the player id of the logged in user"""
    return None if not are_logged_in() else current_user.id


def get_player_information() -> dict:
    """Returns the email based whichever app they have authorized with."""
    return None if not are_logged_in() else current_user.json()


def get_player_teams() -> list[dict]:
    """Returns a list of teams associated with the player"""
    return (None
            if not are_logged_in()
            else [team.json() for team in current_user.teams])


def is_gmail_supported() -> bool:
    """Returns whether current setup support Gmail authentication."""
    return os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "") != ""


def is_github_supported() -> bool:
    """Returns whether current setup support Github authentication."""
    return os.environ.get("GITHUB_OAUTH_CLIENT_ID", "") != ""


def is_facebook_supported() -> bool:
    """Returns whether current setup support Facebook authentication."""
    return os.environ.get("FACEBOOK_OAUTH_CLIENT_ID", "") != ""


def is_azure_supported() -> bool:
    """Returns whether current setup support Facebook authentication."""
    return os.environ.get("AZURE_OAUTH_CLIENT_ID", "") != ""


def check_auth(username: str, password: str) -> bool:
    """Returns if a username password combination is valid.
    """
    return username == ADMIN and password == PASSWORD


def authenticate() -> 'Response':
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def get_team_authorization(team: 'Team') -> TeamAuthorization:
    """Get the user authorization relative to the team"""
    is_captain = are_logged_in() and team.player_id == current_user.id
    on_team = (are_logged_in() and
               bool([player for player in team.players
                    if player.id == current_user.id]))
    can_join = are_logged_in() and not on_team and not is_captain
    has_pending_request = False
    if can_join:
        requests = JoinLeagueRequest.query.filter(
            JoinLeagueRequest.team_id == team.id).all()
        has_pending_request = bool([True for request in requests
                                    if request.email == current_user.email])
    return {'on_team': on_team,
            'is_convenor': False,
            'is_captain': is_captain,
            'pending_request': has_pending_request,
            'logged_in': are_logged_in()}


def api_require_login(f: Callable) -> Callable:
    """Api requires that user it logged in"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not are_logged_in():
            return Response("Not logged in", 401)
        return f(*args, **kwargs)
    return decorated


def api_require_captain(f: Callable) -> Callable:
    """Api that requires the current user be a captain of the team"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not are_logged_in():
            return Response("Not logged in", 401)
        team_id = kwargs.get('team_id', 1 if not (len(args) > 0) else args[0])
        team = Team.query.get(team_id)
        if team is None:
            return Response("Team does not exist", 404)
        if team.player_id != current_user.id:
            return Response("Player is not captain of team", 403)
        return f(*args, **kwargs)
    return decorated


def require_login(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        if not are_logged_in():
            return redirect(url_for("website.loginpage"))
        return f(*args, **kwargs)
    return decorated


def require_captain(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        if not are_logged_in():
            return redirect(url_for("website.loginpage"))
        team_id = kwargs.get('team_id', 1 if not (len(args) > 0) else args[0])
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={"details": team_id})
        if team.player_id != current_user.id:
            raise NotTeamCaptain(payload={"details": team_id})
        return f(*args, **kwargs)
    return decorated


def require_to_be_a_captain(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        if not are_logged_in():
            return redirect(url_for("website.loginpage"))
        teams = Player.get_teams_captained(current_user.id)
        team_id = kwargs.get('team_id', 1 if not (len(args) > 0) else args[0])
        if len(teams) == 0:
            raise NotTeamCaptain(payload={"details": team_id})
        if Team.query.get(team_id) is None:
            raise TeamDoesNotExist(payload={"details": team_id})
        return f(*args, **kwargs)
    return decorated


def require_to_be_convenor(f: Callable) -> Callable:
    """Route requires person to be a convenor."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not are_logged_in():
            return redirect(url_for("website.loginpage"))
        if not current_user.is_convenor:
            raise NotLeagueConvenor(payload={"details": current_user.id})
        return f(*args, **kwargs)
    return decorated


def requires_admin(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if 'admin' in session and 'password' in session:
            # check if user signed in already
            logged = check_auth(session['admin'], session['password'])
            if not logged:
                return authenticate()
        elif are_logged_in() and current_user.is_convenor:
            return f(*args, **kwargs)
        elif not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
