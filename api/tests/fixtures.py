from json import dumps
import pytest
import uuid
from datetime import date, datetime, timedelta
from flask import url_for
from api.app import create_app
from api.extensions import DB
from api.model import JoinLeagueRequest, Sponsor, Player, LeagueEvent, \
    LeagueEventDate, Team, League, Game, Division, Bat, Espys, split_datetime


@pytest.fixture(scope="session")
def mlsb_app():
    """The mlsb flask app."""
    mlsb_app = create_app()
    mlsb_app.config.update({
        "SERVER_NAME": 'localhost:5000',
    })

    # other setups
    yield mlsb_app

    # clean up / reset resources
    pass


@pytest.fixture(scope="session")
def client(mlsb_app):
    return mlsb_app.test_client()


@pytest.fixture(scope="session")
def runner(mlsb_app):
    return mlsb_app.test_cli_runner()


class AuthActions():
    def __init__(self, client):
        self.client = client

    def login(self, email: str):
        return self.client.post(
            url_for("testing.create_and_login"),
            data=dumps({"email": email}),
            content_type='application/json'
        )

    def logout(self):
        return self.client.post(
            url_for("testing.logout")
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)


def factory_fixture(factory):
    @pytest.fixture(scope='session')
    def maker():
        return factory
    maker.__name__ = factory.__name__
    return maker


@factory_fixture
def sponsor_factory(
    sponsor_name: str = '',
    link=None,
    description=None
) -> Sponsor:
    name = sponsor_name if sponsor_name != '' else random_name('Sponsor')
    sponsor = Sponsor(name, link=link, description=description)
    DB.session.add(sponsor)
    DB.session.commit()
    return sponsor


@factory_fixture
def league_factory(league_name: str = '') -> League:
    name = league_name if league_name != '' else random_name('League')
    league = League(name=name)
    DB.session.add(league)
    DB.session.commit()
    return league


@factory_fixture
def division_factory(name: str = '', shortname: str = None) -> Division:
    fallback = f"Division - {str(uuid.uuid4())}"
    name = name if name != '' else fallback
    division = Division(name=name, shortname=shortname)
    DB.session.add(division)
    DB.session.commit()
    return division


@factory_fixture
def player_factory(
    name: str = '',
    email: str = '',
    gender="M",
    password="default",
    active=True
) -> Player:
    name = name if name != '' else random_name("Player")
    email = email if email != '' else random_email()
    player = Player(
        name=name,
        email=email,
        gender=gender,
        password=password,
        active=active
    )
    DB.session.add(player)
    DB.session.commit()
    return Player.query.get(player.id)


@factory_fixture
def team_factory(
    color: str = '',
    sponsor: Sponsor = None,
    league: League = None,
    year: int = date.today().year,
    players: list[Player] = [],
    captain: Player = None,
) -> Team:
    color = color if color != '' else f"{str(uuid.uuid4())}"
    sponsor_id = None if sponsor is None else sponsor.id
    league_id = None if league is None else league.id
    team = Team(
        color=color,
        sponsor_id=sponsor_id,
        league_id=league_id,
        year=year
    )
    for player in players:
        team.insert_player(player.id)
    if captain is not None:
        team.insert_player(captain.id, captain=True)
    DB.session.add(team)
    DB.session.commit()
    return team


@factory_fixture
def league_event_factory(
    name: str = '',
    description: str = 'Description',
    active: bool = True
) -> LeagueEvent:
    name = name if name != '' else random_name("Event")
    league_event = LeagueEvent(
        name=name,
        description=description,
        active=active,
    )
    DB.session.add(league_event)
    DB.session.commit()
    return league_event


@factory_fixture
def league_event_date_factory(
    league_event: LeagueEvent,
    date: str = "2022-10-01",
    time: str = "10:00",
    attendees: list[Player] = []
) -> LeagueEventDate:
    league_event_date = LeagueEventDate(
        date=date,
        time=time,
        league_event_id=league_event.id,
    )
    for player in attendees:
        league_event_date.signup_player(player.id)
    DB.session.add(league_event_date)
    DB.session.commit()
    return league_event_date


@factory_fixture
def game_factory(
    home_team: Team,
    away_team: Team,
    league: League,
    division: Division,
    date: str = "2022-10-01",
    time: str = "10:00",
    status: str = "",
    field: str = "WP1",
) -> Game:
    game = Game(
        date=date,
        time=time,
        home_team_id=home_team.id,
        away_team_id=away_team.id,
        league_id=league.id,
        division_id=division.id,
        status=status,
        field=field
    )
    DB.session.add(game)
    DB.session.commit()
    return game


@factory_fixture
def bat_factory(
    game: Game,
    player: Player,
    team: Team,
    classification: str = "s",
    inning: int = 1,
    rbi: int = 0
) -> Bat:
    bat = Bat(
        player_id=player.id,
        team_id=team.id,
        game_id=game.id,
        classification=classification,
        inning=inning,
        rbi=rbi
    )
    DB.session.add(bat)
    DB.session.commit()
    return bat


@factory_fixture
def espys_factory(
    team: Team,
    sponsor: Sponsor = None,
    description: str = "Random Espys",
    points: float = 1.0,
    receipt: str = None,
    time: str = None,
    date: str = None
) -> Espys:
    espy = Espys(
        team_id=team.id,
        sponsor_id=None if sponsor is None else sponsor.id,
        description=description,
        points=points,
        receipt=receipt,
        time=time,
        date=date
    )
    DB.session.add(espy)
    DB.session.commit()
    return espy


@factory_fixture
def join_league_request_factory(
    team: Team,
    email: str = "",
    name: str = "",
    gender="M"
) -> JoinLeagueRequest:
    email = email if email != "" else random_email()
    name = name if name != "" else random_name("Player Request")
    request = JoinLeagueRequest(
        email=email,
        name=name,
        gender=gender,
        team=team,
    )
    DB.session.add(request)
    DB.session.commit()
    return request


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('espys_factory')
@pytest.fixture
def sample_league(
    mlsb_app,
    sponsor_factory,
    league_factory,
    division_factory,
    player_factory,
    team_factory,
    game_factory,
    espys_factory,
    bat_factory
) -> dict:
    """Generates a random league with sponsors, teams and games."""
    with mlsb_app.app_context():
        sponsors = [
            sponsor_factory(),
            sponsor_factory(),
            sponsor_factory()
        ]
        league = league_factory()
        division = division_factory()

        teams = [
            team_factory(
                league=league,
                sponsor=sponsors[0],
                players=[player_factory(), player_factory()]
            ),
            team_factory(
                league=league,
                sponsor=sponsors[1],
                players=[player_factory(), player_factory()]
            ),
            team_factory(
                league=league,
                sponsor=sponsors[2],
                players=[player_factory(gender="f"), player_factory(gender="f")]
            ),
            team_factory(
                league=league,
                players=[player_factory(), player_factory()]
            ),
        ]
        for team in teams:
            # pick first player as captain
            team.insert_player(team.players[0].id, captain=True)
        espys_factory(team=teams[0], sponsor=sponsors[0], points=1000)

        (yesterday_date, _) = split_datetime(datetime.today())
        (today_date, _) = split_datetime(datetime.today() + timedelta(days=1))
        (tomorrow_date, _) = split_datetime(datetime.today() + timedelta(days=1))
        games = [
            game_factory(
                home_team=teams[0],
                away_team=teams[1],
                league=league,
                division=division,
                date=yesterday_date,
                time="11:00"
            ),
            game_factory(
                home_team=teams[2],
                away_team=teams[3],
                league=league,
                division=division,
                date=yesterday_date,
                time="12:00"
            ),
            game_factory(
                home_team=teams[0],
                away_team=teams[2],
                league=league,
                division=division,
                date=today_date,
                time="11:00",
            ),
            game_factory(
                home_team=teams[1],
                away_team=teams[3],
                league=league,
                division=division,
                date=today_date,
                time="12:00"
            ),
            game_factory(
                home_team=teams[0],
                away_team=teams[3],
                league=league,
                division=division,
                date=tomorrow_date,
                time="11:00"
            ),
            game_factory(
                home_team=teams[1],
                away_team=teams[2],
                league=league,
                division=division,
                date=tomorrow_date,
                time="12:00"
            )
        ]

        # add some scores for the two games
        bat_factory(
            game=games[0],
            team=games[0].home_team,
            player=games[0].home_team.players[0],
            classification="hr",
            rbi=1
        )
        bat_factory(
            game=games[1],
            team=games[1].home_team,
            player=games[1].home_team.players[0],
            classification="ss",
            rbi=2
        )
        result = {
            "sponsors": [sponsor.json() for sponsor in sponsors],
            "league": league.json(),
            "division": division.json(),
            "teams": [team.json() for team in teams]
        }
    return result


def random_email() -> str:
    return f"{str(uuid.uuid4())}@mlsb.ca"


def random_name(category: str) -> str:
    return f"{category} - {str(uuid.uuid4())}"
