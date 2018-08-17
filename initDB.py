'''
@author: Dallas Fraser
@author: 2018-08-17
@organization: MLSB API
@summary: A script that initializes the databases and adds some demo data
'''
from api import DB
from api.model import Player, Sponsor, League, Fun, Game, Team, Espys, Bat
from api.variables import UNASSIGNED_EMAIL, HITS
import requests
import os
import datetime
import random

def random_value_list(l):
    """Returns a random value for the given list l"""
    return l[random.randint(0, len(l) - 1)]

def add_random_score(game_id, team_id, players):
    """Simulates a score by getting a random score and adding random bats"""
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

        
if "FLASK_ENV" not in os.environ or os.environ.get("FLASK_ENV") != "docker":
    print("No FLASK_ENV set or not running on docker")
    print("Just exiting")
    exit

# delete old information
DB.session.commit()
DB.engine.execute('''
                     DROP TABLE IF EXISTS fun;
                     DROP TABLE IF EXISTS roster;
                     DROP TABLE IF EXISTS bat;
                     DROP TABLE IF EXISTS espys;
                     DROP TABLE IF EXISTS game;
                     DROP TABLE IF EXISTS team;
                     DROP TABLE IF EXISTS player;
                     DROP TABLE IF EXISTS sponsor;
                     DROP TABLE IF EXISTS league;
                ''')
DB.create_all()
print("Created tables")
print("Adding mock data ...")

# add the unassigned bats player
DB.session.add(Player("UNASSIGNED", UNASSIGNED_EMAIL, gender="F"))


# add the fun counts
funs = requests.get("http://www.mlsb.ca/api/fun").json()
for fun in funs:
    DB.session.add(Fun(year=fun['year'], count=fun['count']))

# add all the sponsors
_sponsors = requests.get('http://www.mlsb.ca/api/sponsors').json()
sponsors = []
for sponsor in _sponsors:
    temp = Sponsor(sponsor['sponsor_name'],
                   link=sponsor['link'],
                   description=sponsor['description'])
    sponsors.append(temp)
    DB.session.add(temp)

# add a demo league
league = League(name="Demo League")
DB.session.add(league)
DB.session.commit()

# add some players
team_one_players = [Player("Captain1", "captain1@mlsb.ca", gender="M"),
                    Player("MalePlayer1", "mp1@mlsb.ca", gender="M"),
                    Player("FemalePlayer1", "fp1@mlsb.ca", gender="F")]
team_two_players = [Player("Captain2", "captain2@mlsb.ca", gender="F"),
                    Player("MalePlayer2", "mp2@mlsb.ca", gender="M"),
                    Player("FemalePlayer2", "fp2@mlsb.ca", gender="F")]
team_three_players = [Player("Captain3", "captain3@mlsb.ca", gender="M"),
                    Player("MalePlayer3", "mp3@mlsb.ca", gender="M"),
                    Player("FemalePlayer3", "fp3@mlsb.ca", gender="F")]
team_four_players = [Player("Captain4", "captain4@mlsb.ca", gender="F"),
                    Player("MalePlayer4", "mp4@mlsb.ca", gender="M"),
                    Player("FemalePlayer4", "fp4@mlsb.ca", gender="F")]
team_players = [ team_one_players,
                 team_two_players,
                 team_three_players,
                 team_four_players]
for team in team_players:
    for player in team:
        DB.session.add(player)
DB.session.commit()

# add four teams with some players
teams = [Team(color="Black",
              sponsor_id=random_value_list(sponsors).id,
              league_id=league.id),
         Team(color="Blue",
              sponsor_id=random_value_list(sponsors).id,
              league_id=league.id),
         Team(color="Red",
              sponsor_id=random_value_list(sponsors).id,
              league_id=league.id),
         Team(color="Green",
              sponsor_id=random_value_list(sponsors).id,
              league_id=league.id)]
for i in range(0, len(teams)):
    team = teams[i]
    DB.session.add(team)
    # add the players to the team
    for player in team_players[i]:
        team.insert_player(player.id, "captain" in player.name.lower())
DB.session.commit()

# add some random espsy to each team and create a lookup for team id to players
team_player_lookup = {}
random_prices = [9.99, 4.75, 100, 15.50, 12.99]
for i in range(0, len(teams)):
    team_player_lookup[team.id] = team_players[i]
    team = teams[i]
    for j in range(0, 4):
        points = random_value_list(random_prices)
        DB.session.add(Espys(team.id,
                             sponsor_id=random_value_list(sponsors).id,
                             description="Purchase",
                             points=points))
DB.session.commit()

# add some games between the teams
now = datetime.datetime.now()
today = datetime.date.today()
week_ago = today - datetime.timedelta(days=7)
next_week = today + datetime.timedelta(days=3)
last_week_string = week_ago.strftime( "%Y-%m-%d")
next_week_string = next_week.strftime( "%Y-%m-%d")
games = [Game(last_week_string,
              "10:00",
              teams[0].id,
              teams[1].id,
              league.id,
              status="Completed",
              field="WP1"),
         Game(last_week_string,
              "10:00",
              teams[2].id,
              teams[3].id,
              league.id,
              status="Completed",
              field="WP2"),
         Game(last_week_string,
              "11:00",
              teams[0].id,
              teams[2].id,
              league.id,
              status="Completed",
              field="WP1"),
         Game(last_week_string,
              "11:00",
              teams[1].id,
              teams[3].id,
              league.id,
              status="Completed",
              field="WP2"),
         Game(next_week_string,
              "10:00",
              teams[0].id,
              teams[3].id,
              league.id,
              status="To Be Played",
              field="WP1"),
         Game(next_week_string,
              "10:00",
              teams[2].id,
              teams[1].id,
              league.id,
              status="To Be Played",
              field="WP2"),
         Game(next_week_string,
              "11:00",
              teams[1].id,
              teams[0].id,
              league.id,
              status="To Be Played",
              field="WP1"),
         Game(next_week_string,
              "11:00",
              teams[3].id,
              teams[2].id,
              league.id,
              status="To Be Played",
              field="WP2")
              ]
for game in games:
    DB.session.add(game)
DB.session.commit()

# now add a random score to the game
for game in games:
    add_random_score(game.id,
                     game.away_team_id,
                     team_player_lookup[game.away_team_id])
    add_random_score(game.id,
                     game.home_team_id,
                     team_player_lookup[game.home_team_id])
DB.session.commit()

print("Finished adding mock data")