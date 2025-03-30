"""Command used for init and mocking database."""
from api.extensions import DB
from api.model import \
    Player, Sponsor, League, Fun, Game, Team, Espys, Bat, Division, \
    LeagueEvent, LeagueEventDate, Image, BlogPost
from api.variables import UNASSIGNED_EMAIL, HITS
from api.tqdm import tqdm
from sqlalchemy import text
import click
import datetime
import random


CURRENT_YEAR = datetime.datetime.now().year
MOCK_EVENTS = [
    (
        'Beerlympics',
        True,
        """
        <p>
            Beerlympics (formerly called Beerfest). Ever seen the movie?
            Well this is even better.
            Teams dressed up as various countries competing under the hot sun coupled with several awesome drinking
            games makes for a day that you will never forget.
        </p>
        """,
        "https://image-store.fly.storage.tigris.dev//events/beerlympics.png",
        f"{CURRENT_YEAR}-07-01"
    ),
    (
        'Jays Game',
        True,
        """
        <p>
            What better way to get ready for the MLSB season than to drive down
            buses full of party animals like yourselves to T.O.
            to watch the boys of summer?
        </p>
        """,
        "https://image-store.fly.storage.tigris.dev/events/jays_game.png",
        f"{CURRENT_YEAR}-06-01"
    ),
    (
        'Summerween',
        True,
        """
        <p>
            We all know Halloween during university is the best holiday for
            several obvious reasons. At MLSB, you get to partake in celebrating
            this joyous day twice a year.
        </p>
        """,
        "https://image-store.fly.storage.tigris.dev/events/summerween.png",
        f"{CURRENT_YEAR}-06-01"
    ),
    (
        'Mystery Bus',
        True,
        """
        <p>
            What do you get when you cram over a hundred students on to school
            buses and send them to a bar in the middle of nowhere? A hell of a
            good time! This event marks the start of
            MLSB every year and takes place in the winter.
        </p>
        """,
        "https://image-store.fly.storage.tigris.dev/events/mystery_bus.png",
        f"{CURRENT_YEAR}-04-01"
    ),
    (
        'Rafting',
        True,
        """
        <p>
            Rafting is the most hyped MLSB event of the summer! It is a
            whirlwind of a weekend with rafting, camping, tanning, and drinking
            events on the Ottawa river with our
            friends at OWL Rafting.
        </p>
        <p>
            If there is one MLSB event you shouldn’t miss, it is definitely
            this one because it is going to be a wild weekend!
        </p>
        """,
        "https://image-store.fly.storage.tigris.dev/events/rafting.png",
        f"{CURRENT_YEAR}-07-08"
    ),
    (
        'Grand Bender',
        True,
        """
        <p>
            MLSB hosts their annual All Star tournament, and what could be
            better than playing it in a baseball field in the middle of
            nowhere!  Those not participating in the All Star Game are in for
            a treat, as they get the entertainment of watching the All-Stars
            get clumsy on the field.
        </p>
        <p>
            Bring your tents because we will be camping out for the night!
        </p>
        """,
        "https://image-store.fly.storage.tigris.dev/events/grand_bender.png",
        f"{CURRENT_YEAR}-07-28"
    ),
    (
        'MLSB Alumni',
        True,
        """
        <p>
            A weekend for those who have graduated to relive the glory days.
            The tournemant is welcome to both current players and alumni.
            It really is the tournament where legends are born.

        </p>
        <p>
            One of the best weekends of the summer.
            <a href="mailto:mlsbalumni@gmail.com?Subject=MLSB Alumni">
                Sign up
            </a>
        </p>
        """,
        "https://image-store.fly.storage.tigris.dev/events/mlsb_alumni.png",
        f"{CURRENT_YEAR}-06-22"
    )
]
sponsors = [
    {
        "name": "Beertown",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/beertown.png"
    },
    {
        "name": "Kik",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/kik.png"
    },
    {
        "name": "Pabst",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/pabst.png"
    },
    {
        "name": "Spitz",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/spitz.png"
    },
    {
        "name": "Tilt",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/tilt.png"
    },
    {
        "name": "Sportszone",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/sportszone.png"
    },
    {
        "name": "Sleeman",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/sleeman.png"
    },
    {
        "name": "Ripshot",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/ripshot.png"
    },
    {
        "name": "Night School",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/night_school.png"
    },
    {
        "name": "Heaven",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/heaven.png"
    },
    {
        "name": "GE",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/ge.png"
    },
    {
        "name": "Gatorade",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/gatorade.png"
    },
    {
        "name": "Chef on Call",
        "url": "https://image-store.fly.storage.tigris.dev/sponsors/chef_on_call.png"
    }
]


def mock_events():
    """Mock the events"""
    for event in tqdm(MOCK_EVENTS):
        event_image = Image(event[3])
        DB.session.add(event_image)
        DB.session.commit()
        league_event = LeagueEvent(
            event[0], event[2], event[1], image_id=event_image.id
        )
        DB.session.add(league_event)
        DB.session.commit()
        if event[4] is not None:
            event_date = LeagueEventDate(
                event[4], '12:00', league_event.id
            )
            DB.session.add(event_date)
            DB.session.commit()


def mock_fun_count():
    """Mock the fun count"""
    for year in range(2016, CURRENT_YEAR):
        DB.session.add(Fun(year=year, count=random.randint(300, 500)))
    DB.session.commit()


def mock_sponsors():
    """Mock the sponsors"""
    for sponsor in sponsors:
        # add the sponsor images
        logo = Image(sponsor['url'])
        DB.session.add(logo)
        sponsor['logo'] = logo
    DB.session.commit()
    sponsor_lookup = {}
    for index, sponsor_info in enumerate(sponsors):
        sponsor = Sponsor(
            sponsor_info['name'], logo_id=sponsor_info['logo'].id
        )
        DB.session.add(sponsor)
        sponsor_lookup[index + 1] = sponsor
    DB.session.commit()
    return sponsor_lookup


def mock_blog_posts():
    """Mock blog posts"""
    author = Player("Author", "author@mlsb.ca", gender="F")
    image = Image("https://image-store.fly.storage.tigris.dev/posts/launch.jpg")
    DB.session.add(author)
    DB.session.add(image)
    DB.session.commit()
    blog_post = BlogPost(
        author.id,
        'Launch',
        "Get ready MLSBer's!!! Today we launch the official MLSB website",
        "<p>Get ready MLSBer's!!! Today we launch the official MLSB website</p>",
        image_id=image.id
    )
    DB.session.add(blog_post)
    DB.session.commit()


def mock_teams_games(league, division, sponsor_lookup):
    """
    mock_team_games
        Mocks up some data for the league by add some players to a team,
        then a few games to the league and a few scores for some games
        Parameters:
            league: the league object
            sponsor_lookup: a dictionary lookup for a id to its given sponsor
        Returns:
            None
    """
    # add some players
    domain = "@" + division.name.replace(" ", "").replace("&", "-")
    team_one_players = [Player("Captain1", "captain1" + domain, gender="M"),
                        Player("MalePlayer1", "mp1" + domain, gender="M"),
                        Player("FemalePlayer1", "fp1" + domain, gender="F")]
    team_two_players = [Player("Captain2", "captain2" + domain, gender="F"),
                        Player("MalePlayer2", "mp2" + domain, gender="M"),
                        Player("FemalePlayer2", "fp2" + domain, gender="F")]
    team_three_players = [Player("Captain3", "captain3" + domain, gender="M"),
                          Player("MalePlayer3", "mp3" + domain, gender="M"),
                          Player("FemalePlayer3", "fp3" + domain, gender="F")]
    team_four_players = [Player("Captain4", "captain4" + domain, gender="F"),
                         Player("MalePlayer4", "mp4" + domain, gender="M"),
                         Player("FemalePlayer4", "fp4" + domain, gender="F")]
    team_players = [team_one_players,
                    team_two_players,
                    team_three_players,
                    team_four_players]
    for team in tqdm(team_players, desc="Adding mock Players"):
        for player in team:
            DB.session.add(player)
    DB.session.commit()

    # add four teams with some players
    teams = [Team(color="Black",
                  sponsor_id=random_value_lookup(sponsor_lookup).id,
                  league_id=league.id),
             Team(color="Blue",
                  sponsor_id=random_value_lookup(sponsor_lookup).id,
                  league_id=league.id),
             Team(color="Red",
                  sponsor_id=random_value_lookup(sponsor_lookup).id,
                  league_id=league.id),
             Team(color="Green",
                  sponsor_id=random_value_lookup(sponsor_lookup).id,
                  league_id=league.id)]
    for i in tqdm(range(0, len(teams)), desc="Adding mock players to Teams"):
        team = teams[i]
        DB.session.add(team)
        # add the players to the team
        for player in team_players[i]:
            team.insert_player(player.id, "captain" in player.name.lower())
    DB.session.commit()

    # add some random espsy to each team and
    # create a lookup for team id to players
    team_player_lookup = {}
    random_prices = [9.99, 4.75, 100, 15.50, 12.99]
    for i in tqdm(range(0, len(teams)), desc="Adding mock espys to Teams"):
        team = teams[i]
        team_player_lookup[team.id] = team_players[i]
        for __ in range(0, 4):
            points = random_value_list(random_prices)
            espy = Espys(team.id,
                         sponsor_id=random_value_lookup(sponsor_lookup).id,
                         description="Purchase",
                         points=points)
            DB.session.add(espy)
    DB.session.commit()

    # add some games between the teams
    # need a bunch of games
    today = datetime.date.today()
    games = []
    for day in range(-3, 3):
        date_string = (today +
                       datetime.timedelta(days=day)).strftime("%Y-%m-%d")
        status = "Completed" if day < 0 else "To Be Played"
        games.append(Game(date_string,
                          "10:00",
                          teams[0].id,
                          teams[1].id,
                          league.id,
                          division.id,
                          status=status,
                          field="WP1"))
        games.append(Game(date_string,
                          "10:00",
                          teams[2].id,
                          teams[3].id,
                          league.id,
                          division.id,
                          status=status,
                          field="WP2"))
        games.append(Game(date_string,
                          "11:00",
                          teams[0].id,
                          teams[2].id,
                          league.id,
                          division.id,
                          status=status,
                          field="WP1"))
        games.append(Game(date_string,
                          "11:00",
                          teams[2].id,
                          teams[1].id,
                          league.id,
                          division.id,
                          status=status,
                          field="WP2"))
        games.append(Game(date_string,
                          "12:00",
                          teams[0].id,
                          teams[3].id,
                          league.id,
                          division.id,
                          status=status,
                          field="WP1"))
        games.append(Game(date_string,
                          "12:00",
                          teams[2].id,
                          teams[1].id,
                          league.id,
                          division.id,
                          status=status,
                          field="WP2"))

    for game in tqdm(games, "Adding mock games"):
        DB.session.add(game)
    DB.session.commit()

    # now add a random score to the game
    for game in tqdm(games[:18], desc="Mocking scores for games"):
        add_random_score(game.id,
                         game.away_team_id,
                         team_player_lookup[game.away_team_id])
        add_random_score(game.id,
                         game.home_team_id,
                         team_player_lookup[game.home_team_id])
    DB.session.commit()


def mock_league(league_name="Demo League"):
    """Returns a mock league that was added to local DB."""
    # add a demo league
    league = League(name=league_name)
    DB.session.add(league)
    DB.session.commit()
    return league


def mock_division(division="Monday & Wednesday"):
    """Returns a mock division that was added to local DB."""
    division_model = Division(division)
    DB.session.add(division_model)
    DB.session.commit()
    return division_model


def create_fresh_tables():
    """Creates fresh tables and deletes any previous information."""
    # delete old information
    DB.session.commit()
    with DB.engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS blog_post;"))
        conn.execute(text("DROP TABLE IF EXISTS flask_dance_oauth;"))
        conn.execute(text("DROP TABLE IF EXISTS attendance;"))
        conn.execute(text("DROP TABLE IF EXISTS league_event_date;"))
        conn.execute(text("DROP TABLE IF EXISTS league_event;"))
        conn.execute(text("DROP TABLE IF EXISTS join_league_request;"))
        conn.execute(text("DROP TABLE IF EXISTS flask_dance_oauth;"))
        conn.execute(text("DROP TABLE IF EXISTS fun;"))
        conn.execute(text("DROP TABLE IF EXISTS roster;"))
        conn.execute(text("DROP TABLE IF EXISTS bat;"))
        conn.execute(text("DROP TABLE IF EXISTS espys;"))
        conn.execute(text("DROP TABLE IF EXISTS game;"))
        conn.execute(text("DROP TABLE IF EXISTS division;"))
        conn.execute(text("DROP TABLE IF EXISTS team;"))
        conn.execute(text("DROP TABLE IF EXISTS player;"))
        conn.execute(text("DROP TABLE IF EXISTS sponsor;"))
        conn.execute(text("DROP TABLE IF EXISTS league;"))
        conn.execute(text("DROP TABLE IF EXISTS image;"))
        conn.commit()
    DB.create_all()


def random_value_lookup(lookup):
    """Returns a object for a random key in the lookup."""
    __, value = random.choice(list(lookup.items()))
    return value


def random_value_list(some_list):
    """Returns a random value for the given list l."""
    return some_list[random.randint(0, len(some_list) - 1)]


def add_random_score(game_id, team_id, players):
    """Simulates a score by getting a random score and adding random bats."""
    score = random.randint(1, 15)
    while score > 0:
        batter = random_value_list(players)
        bat = random_value_list(HITS)
        rbis = 0
        if (bat.lower() == "s" or bat.lower() == "ss"):
            rbis = random.randint(0, 1)
        elif (bat.lower() == "d"):
            rbis = random.randint(0, 2)
        elif (bat.lower() == "hr"):
            rbis = random.randint(1, 4)

        # just make sure not submitting a guy hitting ss
        if (batter.gender.lower() == "m" and bat.lower() == "ss"):
            bat = "s"
        score = score - rbis
        DB.session.add(Bat(batter.id, team_id, game_id, bat, rbi=rbis))
    DB.session.commit()


def create_email(player_name):
    """Returns an email for the given player name."""
    return player_name + str(random.randint(0, 100000)) + "@mlsb.ca",


def is_player_captain(player, team):
    """Returns whether the given player is the captain of the team."""
    captain = False
    if (team['captain'] is not None and
            'player_id' in team['captain'] and
            (player['player_id'] == team['captain']['player_id'])):
        captain = True
    return captain


def init_database(mock, create):
    """
    init_database
        Initialize the database either by mocking data or copying main
        website locally
        Parameters:
            mock: whether to mock some data for the current year
            create: True if database should be created
        Returns:
            None
    """
    if (create):
        create_fresh_tables()
        DB.session.add(Player("UNASSIGNED", UNASSIGNED_EMAIL, gender="F"))
        DB.session.commit()
    if (mock):
        print("Adding mock data ...")
        # add the unassigned bats player
        mock_events()
        mock_fun_count()
        sponsor_lookup = mock_sponsors()
        league = mock_league()
        mock_teams_games(league, mock_division(), sponsor_lookup)
        mock_teams_games(league, mock_division(
            division="Tuesday & Thursday"), sponsor_lookup)
        mock_blog_posts()
    return


@click.command("init-db")
@click.option(
    "-m/-M",
    "--mock/--no-mock",
    default=True,
    is_flag=True,
    help="Mock the database with data"
)
@click.option(
    "-c/-C",
    "--create/--no-create",
    default=False,
    is_flag=True,
    help="Create the tables in the database"
)
def database_command(mock, create):
    """Flask cli command for database."""
    init_database(mock, create)
    return
