'''
@author: Dallas Fraser
@author: 2018-08-17
@organization: MLSB API
@summary: A script that initializes the databases and adds some demo data
'''
from api import DB
from api.model import Player, Sponsor, League, Fun, Game, Team, Espys, Bat,\
    Division
from api.variables import UNASSIGNED_EMAIL, HITS
from tqdm import tqdm
import requests
import os
import datetime
import random
import argparse


def mock_fun_count():
    """Mock the fun count"""
    current_year = datetime.datetime.now().year
    for year in range(2016, current_year):
        DB.session.add(Fun(year=year, count=random.randint(300, 500)))
    DB.session.commit()


def mock_sponsors():
    """Mock the sponsors"""
    sponsor_lookup = {}
    for index, name in enumerate(["Beertown", "Kik", "Pabst", "Spitz", "Tilt",
                                  "Sportszone", "Sleeman", "Ripshot",
                                  "Night School", "Heaven", "GE", "Gatorade",
                                  "Chef on Call"]):
        sponsor = Sponsor(name)
        DB.session.add(sponsor)
        sponsor_lookup[index + 1] = sponsor
    DB.session.commit()
    return sponsor_lookup


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
    DB.engine.execute("DROP TABLE IF EXISTS fun;")
    DB.engine.execute("DROP TABLE IF EXISTS roster;")
    DB.engine.execute("DROP TABLE IF EXISTS bat;")
    DB.engine.execute("DROP TABLE IF EXISTS espys;")
    DB.engine.execute("DROP TABLE IF EXISTS team;")
    DB.engine.execute("DROP TABLE IF EXISTS sponsor;")
    DB.engine.execute("DROP TABLE IF EXISTS league;")
    DB.create_all()


def random_value_lookup(lookup):
    """Returns a object for a random key in the lookup."""
    __, value = random.choice(list(lookup.items()))
    return value


def random_value_list(l):
    """Returns a random value for the given list l."""
    return l[random.randint(0, len(l) - 1)]


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
        if(batter.gender.lower() == "m" and bat.lower() == "ss"):
            bat = "s"
        score = score - rbis
        DB.session.add(Bat(batter.id, team_id, game_id, bat, rbi=rbis))
    DB.session.commit()


def pull_all_pages(url, pagination):
    """ Pulls the items from all the pages (paginated object)."""
    data = pagination['items']
    if(pagination['has_next']):
        pagination = requests.get(url + pagination['next_url'])
        data = data + pull_all_pages(url, pagination.json())
    return data


def pull_fun_count(url):
    """
    pull_fun_count
        Adds all the fun objects from website into the local DB
        Parameters:
            url: the url of the main site
        Returns:
            None"""
    # add the fun counts
    funs = requests.get(url + "/api/fun").json()
    if isinstance(funs, dict):
        funs = pull_all_pages(url, funs)
    for fun in tqdm(funs, desc="Pulling fun from {}".format(url)):
        DB.session.add(Fun(year=fun['year'], count=fun['count']))
    DB.session.commit()


def pull_sponsors(url):
    """
    pull_sponsors
        Returns a lookup of sponsors that were pulled
        from the website into local DB
        Parameters:
            url: the url of the main site
        Returns:
            a dictionary lookup
                for the website sponsor id to local sponsor object
                e.g. sponsor_lookup = {1: Sponsor(), etc..}
    """
    # add all the sponsors
    _sponsors = requests.get(url + '/api/sponsors').json()
    if isinstance(_sponsors, dict):
        _sponsors = pull_all_pages(url, _sponsors)
    sponsors_lookup = {}
    for sponsor in tqdm(_sponsors,
                        desc="Pulling sponsors from {}".format(url)):
        temp = Sponsor(sponsor['sponsor_name'],
                       link=sponsor['link'],
                       description=sponsor['description'])
        sponsors_lookup[sponsor['sponsor_id']] = temp
        DB.session.add(temp)
    DB.session.commit()
    return sponsors_lookup


def pull_leagues(url):
    """
    pull_leagues
        Returns a lookup of leagues that were pulled
        from the website into local DB
        Parameters:
            url: the url of the main site
        Returns:
            a dictionary lookup
                for the website league id to local league object
                e.g. league_lookup = {1: League(), etc..}
    """
    _leagues = requests.get(url + "/api/leagues").json()
    if isinstance(_leagues, dict):
        _leagues = pull_all_pages(url, _leagues)
    leagues_lookup = {}
    for league in tqdm(_leagues, desc="Pulling leagues from {}".format(url)):
        temp = League(name=league['league_name'])
        leagues_lookup[league['league_id']] = temp
        DB.session.add(temp)
    DB.session.commit()
    return leagues_lookup


def pull_divisions(url):
    """
    pull_divisions
        Returns a lookup of divisions that were pulled
        from the website into local DB
        Parameters:
            url: the url of the main site
        Returns:
            a dictionary lookup
                for the website division id to local division object
                e.g. division_lookup = {1: Division(), etc..}
    """
    _divisions = requests.get(url + "/api/leagues").json()
    if isinstance(_divisions, dict):
        _divisions = pull_all_pages(url, _divisions)
    divisions_lookup = {}
    for division in tqdm(_divisions,
                         desc="Pulling divisions from {}".format(url)):
        temp = Division(division['division_name'])
        divisions_lookup[division['league_id']] = temp
        DB.session.add(temp)
    DB.session.commit()
    return divisions_lookup


def create_email(player_name):
    """Returns an email for the given player name."""
    return player_name + str(random.randint(0, 100000)) + "@mlsb.ca",


def pull_players(url):
    """
    pull_players
        Returns a lookup of players that were pulled
        from the website into local DB
        Parameters:
            url: the url of the main site
        Returns:
            a dictionary lookup
                for the website sponsor id to local player object
                e.g. player_lookup = {1: Player(), etc..}
    """
    _players = requests.get(url + "/api/players").json()
    if isinstance(_players, dict):
        _players = pull_all_pages(url, _players)
    players_lookup = {}
    for player in tqdm(_players, desc="Pulling players from {}".format(url)):
        if (player['player_name'].lower() != "unassigned"):
            temp = Player(player['player_name'],
                          create_email(player['player_name']),
                          gender=player['gender'],
                          active=False
                          )
            players_lookup[player['player_id']] = temp
            DB.session.add(temp)
    DB.session.commit()
    return players_lookup


def is_player_captain(player, team):
    """Returns whether the given player is the captain of the team."""
    captain = False
    if (team['captain'] is not None and
            'player_id' in team['captain'] and
            (player['player_id'] == team['captain']['player_id'])):
        captain = True
    return captain


def pull_teams(url, player_lookup, sponsor_lookup, league_lookup):
    """
    pull_teams
        Returns a lookup of teams that were pulled
        from the website into local DB
        Parameters:
            url: the url of the main site
        Returns:
            a dictionary lookup
                for the website team id to local team object
                e.g. team_lookup = {1: Team(), etc..}
    """
    _teams = requests.get(url + "/api/teams").json()
    if isinstance(_teams, dict):
        _teams = pull_all_pages(url, _teams)
    team_lookups = {}
    for team in tqdm(_teams, desc="Pulling teams from {}".format(url)):
        temp = Team(color=team['color'],
                    sponsor_id=sponsor_lookup[team['sponsor_id']].id,
                    league_id=league_lookup[team['league_id']].id,
                    year=team['year'])
        # need to add the players from the roster to the team
        players = requests.get(url +
                               "/api/teamroster/" +
                               team['team_id']).json()
        for player in players:
            temp.insert_player(player_lookup[player['player_id']].id,
                               is_player_captain(player, team))
        team_lookups[team['team_id']] = temp
        DB.session.add(temp)
    DB.session.commit()
    return team_lookups


def pull_games(url, team_lookup, league_lookup):
    """
    pull_games
        Returns a lookup of games that were pulled
        from the website into local DB
        Parameters:
            url: the url of the main site
        Returns:
            a dictionary lookup
                for the website game id to local game object
                e.g. game_lookup = {1: Game(), etc..}
    """
    _games = requests.get(url + "/api/games").json()
    if isinstance(_games, dict):
        _games = pull_all_pages(url, _games)
    game_lookup = {}
    for game in tqdm(_games, desc="Pulling games from {}".format(url)):
        temp = Game(game['date'],
                    game['time'],
                    team_lookup[game['home_team_id']].id,
                    team_lookup[game['away_team_id']].id,
                    league_lookup[game['league_id']].id,
                    status=game['status'],
                    field=game['field'])
        game_lookup[game['game_id']] = temp
        DB.session.add(temp)
    DB.session.commit()
    return game_lookup


def pull_bats(url, team_lookup, player_lookup, game_lookup):
    """
    pull_bats
        Returns a lookup of bats that were pulled
        from the website into local DB
        Parameters:
            url: the url of the main site
        Returns:
            a dictionary lookup
                for the website bat id to local bat object
                e.g. bat_lookup = {1: Bat(), etc..}
    """
    _bats = requests.get(url + "/api/bats").json()
    if isinstance(_bats, dict):
        _bats = pull_all_pages(url, _bats)
    bat_lookup = {}
    for bat in tqdm(_bats, desc="Pulling bats from {}".format(url)):
        temp = Bat(player_lookup[bat['player_id']].id,
                   team_lookup[bat['team_id']].id,
                   game_lookup[bat['game_id']].id,
                   bat['hit'],
                   bat['inning'],
                   bat['rbi'])
        bat_lookup[bat['bat_id']] = temp
        DB.session.add(temp)
    DB.session.commit()
    return bat_lookup


def pull_espys(url, team_lookup, sponsor_lookup):
    """
    pull_espys
        Returns a lookup of espys that were pulled
        from the website into local DB
        Parameters:
            url: the url of the main site
        Returns:
            a dictionary lookup
                for the website espy id to local espy object
                e.g. bat_lookup = {1: Espys(), etc..}
    """
    _espys = requests.get(url + "/api/espys").json()
    if isinstance(_espys, dict):
        _espys = pull_all_pages(url, _espys)
    espy_lookup = {}
    for espy in tqdm(_espys, desc="Pulling espys from {}".format(url)):
        temp = Espys(team_lookup[espy['team_id']].id,
                     sponsor_lookup[espy['sponsor_id']].id,
                     espy['description'],
                     espy['points'],
                     espy['receipt'],
                     espy['time'],
                     espy['date'])
        espy_lookup[espy['espy_id']] = temp
        DB.session.add(temp)
    DB.session.commit()
    return espy_lookup


def init_database(mock, copy_locally, url, create_db):
    """
    init_database
        Initialize the database either by mocking data or copying main
        website locally
        Parameters:
            mock: whether to mock some data for the current year
            copy_locally: whether to copy the main website locally
            url: the main website main url (https://www.mlsb.ca)
            create_db: True if database should be created
        Returns:
            None
    """
    if (create_db):
        create_fresh_tables()
        DB.session.add(Player("UNASSIGNED", UNASSIGNED_EMAIL, gender="F"))
        DB.session.commit()
    if (mock):
        print("Adding mock data ...")
        # add the unassigned bats player
        mock_fun_count()
        sponsor_lookup = mock_sponsors()
        league = mock_league()
        mock_teams_games(league, mock_division(), sponsor_lookup)
        mock_teams_games(league, mock_division(
            division="Tuesday & Thursday"), sponsor_lookup)
    else:
        if(copy_locally):
            print("Pulling a local copy of the given website")
            pull_fun_count(url)
            sponsor_lookup = pull_sponsors(url)
            player_lookup = pull_players(url)
            league_lookup = pull_leagues(url)
            team_lookup = pull_teams(url,
                                     player_lookup,
                                     sponsor_lookup,
                                     league_lookup)
            game_lookup = pull_games(url, team_lookup, league_lookup)
            pull_bats(url, team_lookup, player_lookup, game_lookup)
            pull_espys(url, team_lookup, sponsor_lookup)
    return


if __name__ == "__main__":
    descp = """
            Initialize the database for MLSB platform
            One can mock some data or can pull the main platform data
            to create a local copy
            Author: Dallas Fraser (dallas.fraser.waterloo@gmail.com)
            """
    if ("FLASK_ENV" not in os.environ or
            os.environ.get("FLASK_ENV").lower() != "docker"):
        print("No FLASK_ENV set or not running on docker")
        print("Just exiting")
        exit

    if ("FLASK_ENV" not in os.environ or
            os.environ.get("FLASK_ENV").lower() == "production"):
        print("Running on Production")
        exit
    parser = argparse.ArgumentParser(description=descp)

    # use the development serve (just so not touching production)
    default_url = "https://mlsb-platform-development.herokuapp.com"
    parser.add_argument("-url",
                        dest="url",
                        action="store",
                        help="The main platform URL",
                        default=default_url)
    prompt = "Set if one wants to mock some data for this year"
    parser.add_argument("-mock",
                        dest="mock",
                        action="store_true",
                        help=prompt,
                        default=False)
    parser.add_argument("-localCopy",
                        dest="localCopy",
                        action="store_true",
                        help="Set if one wants to pull all data from url",
                        default=False)
    parser.add_argument("-createDB",
                        dest="createDB",
                        action="store_true",
                        help="Set if want to create DB (delete if exists)",
                        default=False)
    args = parser.parse_args()
    print(args)
    init_database(args.mock, args.localCopy, args.url, args.createDB)
