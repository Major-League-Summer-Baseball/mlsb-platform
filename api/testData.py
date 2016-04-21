from api import DB
from api.model import Player, Team, Sponsor, Game, League, Bat, Espys, Fun
from random import randint
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
FUNS = {
       2002:89,
       2003: 100,
       2004: 177,
       2005:186,
       2006:176,
       2007: 254,
       2008: 290,
       2009: 342,
       2010: 304,
       2011: 377,
       2012: 377,
       2013: 461,
       2014: 349,
       2015: 501
       }
for year, count in FUNS.items():
    DB.session.add(Fun(year=year, count=count))
# add the two leagues
DB.session.add(League(name="Monday & Wednesday"))
DB.session.add(League(name="Tuesday & Thursday"))
sponsors = [Sponsor("Brick Brewery", link="https://www.facebook.com/brick.brewery?fref=ts", active=False),
            Sponsor("Chainsaw", link="https://www.facebook.com/ChainsawLovers"),
            Sponsor("Crossroads", link="https://www.facebook.com/domushousing?fref=ts"),
            Sponsor("Domus", link="https://www.facebook.com/domushousing?fref=ts", active=False),
            Sponsor("East Side's Mario's", link="https://www.facebook.com/esm.waterloouniversity?fref=ts", active=False),
            Sponsor("Fat Basrtd Burrito", link="https://www.facebook.com/FatBastardBurritoCo.Waterloo?fref=ts", active=False),
            Sponsor("Frites", link="https://www.facebook.com/frieswithbenefits?fref=ts", active=False),
            Sponsor("Gatorade", link="http://www.pepsicojobs.com/en-ca"),
            Sponsor("Spitz", link="http://www.pepsicojobs.com/en-ca"),
            Sponsor("GE", link="http://www.ge.com/ca/careers", active=False),
            Sponsor("Gino's Pizza", link="http://www.ginospizza.ca/"),
            Sponsor("Huether Hotel", link="https://www.facebook.com/HuetherHotel?fref=ts", active=False),
            Sponsor("Kik", link="http://www.kik.com/careers/"),
            Sponsor("Maxwell's", link="http://maxwellswaterloo.com/", active=False),
            Sponsor("Mel's Diner", link="https://www.facebook.com/Melsdinerwaterloo?fref=ts"),
            Sponsor("Morty's Pub",link="https://www.facebook.com/MortysPub?fref=ts"),
            Sponsor("Night School",link="https://www.facebook.com/NightSchoolWaterloo"),
            Sponsor("Owl Rafting",link="http://www.owl-mkc.ca/owl/", active=False),
            Sponsor("Pita Factory",link="http://www.pitafactory.com/", active=False),
            Sponsor("Reds Whites and Brews",link="http://www.redswhitesandbrews.ca/"),
            Sponsor("SBESS",link="https://www.facebook.com/LazSoc/?fref=ts", active=False),
            Sponsor("Sentry",link="Shoeless Joe's - Waterloo", active=False),
            Sponsor("Shoeless Joe's",link="https://www.facebook.com/ShoelessJoesWaterloo?fref=ts"),
            Sponsor("Sleeman",link="https://www.facebook.com/SleemanBeer?fref=ts"),
            Sponsor("Snapple Vodka",link="http://www.snapple.com/", active=False),
            Sponsor("SportZone",link="https://www.facebook.com/sportszonecanada?fref=ts"),
            Sponsor("Traces",link="http://traces.com/", active=False),
            Sponsor("Turret Nightclub",link="https://www.facebook.com/turretnightclub?fref=ts"),
            Sponsor("Veritas",link="https://www.facebook.com/VeritasCafe?fref=ts"),
            Sponsor("Waterloo",link="https://www.facebook.com/waterloonetworks?fref=ts", active=False),
            Sponsor("Wilfs",link="https://www.facebook.com/wilfsrestaurantbar?fref=ts"),
            Sponsor("CaliBurger",link="https://www.facebook.com/CaliBurgerWaterloo/?fref=ts"),
            Sponsor("Collins Barrow", link="http://www.collinsbarrow.com/en/cbn/"),
            Sponsor("Frat Burger", link="https://www.facebook.com/FratBurger/?fref=ts"),
            Sponsor("Freshii", link="https://www.facebook.com/freshiiwaterloo/?fref=ts"),
            Sponsor("Heaven", link="https://www.facebook.com/heavengastroclub/?fref=ts"),
            Sponsor("Jack Daniels", link="http://www.jackdaniels.com/ca"),
            Sponsor("LazSoc", link="http://lazsoc.ca/"),
            Sponsor("The Pub on King", link="https://www.facebook.com/thepubonking/?fref=ts"),
            Sponsor("Smoke's Poutine", link="https://www.facebook.com/SmokesPoutinerieWaterloo/"),
            Sponsor("Stark & Perri", link="https://www.facebook.com/Stark-Perri-1504025033225383/?fref=ts"),
            Sponsor("Taco Farm", link="https://www.facebook.com/tacofarmco/?fref=ts"),
            Sponsor("Tilt", link="https://www.tilt.com/en-ca/tilts/new"),
            Sponsor("Menchies", link="https://www.facebook.com/pages/Menchies-Waterloo/240980822616062?fref=ts"),
            Sponsor("Pabst", link="http://pabstblueribbon.com/")
          ]
for sponsor in sponsors:
    DB.session.add(sponsor)
DB.session.commit()
teams = [
          Team(
               color="Blue",
               sponsor_id=1,
               league_id=2,
               year=2015
               ),
          Team(
               color="Bronze",
               sponsor_id=1,
               league_id=2,
               year=2015
               
               ),
          Team(
               color="Charcoal",
               sponsor_id=2,
               league_id=1,
               year=2015
               ),
          Team(
               color="Cherry",
               sponsor_id=2,
               league_id=2,
               year=2015
               ),
          Team(
               color="Crimson",
               sponsor_id=3,
               league_id=1,
               year=2015
               ),
          Team(
               color="Desert",
               sponsor_id=4,
               league_id=1,
               year=2015
               ),
          Team(
               color="Diamond",
               sponsor_id=4,
               league_id=1,
               year=2015
               ),
          Team(
               color="Sapphire",
               sponsor_id=5,
               league_id=1,
               year=2015
               ),
          Team(
               color="Black",
               sponsor_id=6,
               league_id=2,
               year=2015
               ),
          Team(
               color="Flame",
               sponsor_id=7,
               league_id=1,
               year=2015
               ),
          Team(
               color="Green",
               sponsor_id=8,
               league_id=2,
               year=2015
               ),
          Team(
               color="Electric Purple",
               sponsor_id=9,
               league_id=2,
               year=2015
               ),
          Team(
               color="Jasper",
               sponsor_id=10,
               league_id=2,
               year=2015
               ),
          Team(
               color="Honeydew",
               sponsor_id=11,
               league_id=2,
               year=2015
               ),
          Team(
               color="Kryptonite",
               sponsor_id=12,
               league_id=1,
               year=2015
               ),
          Team(
               color="Marble",
               sponsor_id=13,
               league_id=2,
               year=2015
               ),
          Team(
               color="Mint",
               sponsor_id=14,
               league_id=1,
               year=2015
               ),
          Team(
               color="Mauve",
               sponsor_id=15,
               league_id=1,
               year=2015
               ),
          Team(
               color="Moonstone",
               sponsor_id=15,
               league_id=2,
               year=2015
               ),
          Team(
               color="Navy",
               sponsor_id=16,
               league_id=2,
               year=2015
               ),
          Team(
               color="Arsenic",
               sponsor_id=17,
               league_id=1,
               year=2015
               ),
          Team(
               color="Blue",
               sponsor_id=26,
               league_id=2,
               year=2015
               ),
          Team(
               color="Fuchsia",
               sponsor_id=18,
               league_id=2,
               year=2015
               ),
          Team(
               color="Burgundy",
               sponsor_id=19,
               league_id=1,
               year=2015
               ),
          Team(
               color="Saffron",
               sponsor_id=20,
               league_id=1,
               year=2015
               ),
          Team(
               color="Silver",
               sponsor_id=20,
               league_id=1,
               year=2015
               ),
          Team(
               color="Sky",
               sponsor_id=21,
               league_id=1,
               year=2015
               ),
          Team(
               color="Jade",
               sponsor_id=22,
               league_id=1,
               year=2015
               ),
          Team(
               color="Jasmine",
               sponsor_id=22,
               league_id=2,
               year=2015
               ),
          Team(
               color="Yellow",
               sponsor_id=23,
               league_id=2,
               year=2015
               ),
          Team(
               color="Vulcan",
               sponsor_id=24,
               league_id=2,
               year=2015
               ),
          Team(
               color="Sunflower",
               sponsor_id=8,
               league_id=1,
               year=2015
               ),
          Team(
               color="Stark Pink",
               sponsor_id=25,
               league_id=1,
               year=2015
               ),
          Team(
               color="Tan",
               sponsor_id=26,
               league_id=2,
               year=2015
               ),
          Team(
               color="Tangerine",
               sponsor_id=27,
               league_id=2,
               year=2015
               ),
          Team(
               color="Turquoise",
               sponsor_id=27,
               league_id=2,
               year=2015
               ),
          Team(
               color="Vermillion",
               sponsor_id=28,
               league_id=2,
               year=2015
               ),
          Team(
               color="Wintergreen",
               sponsor_id=29,
               league_id=1,
               year=2015
               ),
          Team(
               color="Walnut",
               sponsor_id=30,
               league_id=1,
               year=2015
               ),
          Team(
               color="Watermelon",
               sponsor_id=30,
               league_id=1,
               year=2015
               )
          ]

for team in teams:
    DB.session.add(team)
DB.session.commit()

#add espys points
espys = [73,75,175,495,248,152,975,583,303,133,321,226,153,218,1029,169,236,
         290,671,197,253,603,44,766,90,211,458,253,161,44,376,906,1399,385,110,
         280,268,431,0,417]
for i in range(0, len(espys)):
    teams[i].espys.append(Espys(teams[i].id, points=espys[i], description="Season"))
UNASSIGNED = Player("Unassigned runs", "doNotUser", "m")
DB.session.add(UNASSIGNED)
captains = [
               Player("Kyle Morrison", "1X", gender="m"),
               Player("Ty Ackerman", "2X", gender="m"),
               Player("Hannah Steele", "3X", gender="f"),
               Player("Kristen Ruetz", "4X", gender="f"),
               Player("Taylor", "5X", gender="f"),
               Player("Brandon Gizzo", "6X", gender="m"),
               Player("Westley Nixon", "7X", gender="m"),
               Player("Derek Hanson", "8X", gender="m"),
               Player("Raj Gangar", "9X", gender="m"),
               Player("Rohit Deora", "10X", gender="m"),
               Player("Mackenzie Young", "11X", gender="f"),
               Player("Michelle Meleskie", "12X", gender="f"),
               Player("Paige O'Grady", "13X", gender="f"),
               Player("Tony Chen", "14X", gender="m"),
               Player("Kevin McGaire", "15X", gender="f"),
               Player("Matt Hadaway", "16X", gender="m"),
               Player("Mike McConnell", "17X", gender="m"),
               Player("Drew Padovan", "18X", gender="m"),
               Player("Sarah Chapman", "19X", gender="f"),
               Player("Dallas Fraser", "20X", gender="m"),
               Player("Ujwal Shah", "21X", gender="m"),
               Player("Charlie Still", "22X", gender="m"),
               Player("Evan", "23X", gender="m"),
               Player("Jeff", "24X", gender="m"),
               Player("Kendall", "25X", gender="f"),
               Player("Dawn Simons", "26X", gender="f"),
               Player("Alex Diakun", "27X", gender="m"),
               Player("Noodles", "28X", gender="m"),
               Player("Victoria Vercillo", "29X", gender="f"),
               Player("Brandon Nunes de Souza", "30X", gender="m"),
               Player("Kassandra Falvo", "31X", gender="f"),
               Player("Aj Paluzzi", "32X", gender="m"),
               Player("Brennan Wilson", "33X", gender="m"),
               Player("Lawren Maris", "34X", gender="f"),
               Player("Laura Visentin", "35X", gender="f"),
               Player("Tea Galli", "36X", gender="f"),
               Player("V", "37X", gender="f"),
               Player("W", "38X", gender="f"),
               Player("Steve Hassan", "39X", gender="m"),
               Player("Brittany Danelon", "40X", gender="f")
          ]
for index, player in enumerate(captains):
    DB.session.add(player)
    teams[index].insert_player(index+1, captain=True)

DB.session.commit()

games  = [
          (Game(  "2015-05-11",
                    "11:45",
                    33,
                    18,
                    1,
                    status="",
                    field="WP1"),24, 5),
          (Game(  "2015-05-11",
                    "11:45",
                    15,
                    28,
                    1,
                    status="",
                    field="WP2"),28, 2),
          (Game(  "2015-05-11",
                    "11:45",
                    27,
                    3,
                    1,
                    status="",
                    field="WP3"),8, 0),
          (Game(  "2015-05-11",
                    "11:45",
                    8,
                    17,
                    1,
                    status="",
                    field="WP4"),17, 2),
          (Game(  "2015-05-11",
                    "12:45",
                    40,
                    26,
                    1,
                    status="",
                    field="WP1"),25, 1),
          (Game(  "2015-05-11",
                    "12:45",
                    5,
                    6,
                    1,
                    status="",
                    field="WP2"),8, 11),
          (Game(  "2015-05-11",
                    "12:45",
                    7,
                    38,
                    1,
                    status="",
                    field="WP3"),12, 0),
          (Game(  "2015-05-11",
                    "12:45",
                    24,
                    21,
                    1,
                    status="",
                    field="WP4"),9, 1),
          (Game(  "2015-05-11",
                    "13:45",
                    32,
                    25,
                    1,
                    status="",
                    field="WP1"),12, 3),
          (Game(  "2015-05-11",
                    "13:45",
                    10,
                    39,
                    1,
                    status="",
                    field="WP2"),3, 14),
          (Game(  "2015-05-13",
                    "11:45",
                    26,
                    17,
                    1,
                    status="",
                    field="WP1"),5, 5),
          (Game(  "2015-05-13",
                    "11:45",
                    7,
                    33,
                    1,
                    status="",
                    field="WP2"),7, 23),
          (Game(  "2015-05-13",
                    "11:45",
                    21,
                    25,
                    1,
                    status="",
                    field="WP3"),7, 6),
          (Game(  "2015-05-13",
                    "11:45",
                    27,
                    39,
                    1,
                    status="",
                    field="WP4"),7, 7),
          (Game(  "2015-05-13",
                    "12:45",
                    5,
                    15,
                    1,
                    status="",
                    field="WP1"),0, 36),
          (Game(  "2015-05-13",
                    "12:45",
                    24,
                    32,
                    1,
                    status="",
                    field="WP2"),21, 16),
          (Game(  "2015-05-13",
                    "12:45",
                    3,
                    10,
                    1,
                    status="",
                    field="WP3"),2, 5),
          (Game(  "2015-05-13",
                    "12:45",
                    6,
                    28,
                    1,
                    status="",
                    field="WP4"),3, 7),
          (Game(  "2015-05-13",
                    "13:45",
                    18,
                    38,
                    1,
                    status="",
                    field="WP1"),14, 9),
          (Game(  "2015-05-13",
                    "13:45",
                    8,
                    40,
                    1,
                    status="",
                    field="WP2"),2, 21),
          (Game(  "2015-05-12",
                    "11:45",
                    4,
                    12,
                    2,
                    status="",
                    field="WP1"),19, 2),
          (Game(  "2015-05-12",
                    "11:45",
                    19,
                    13,
                    2,
                    status="",
                    field="WP2"),12, 0),
          (Game(  "2015-05-12",
                    "11:45",
                    22,
                    2,
                    2,
                    status="",
                    field="WP3"),8, 0),
          (Game(  "2015-05-12",
                    "11:45",
                    1,
                    35,
                    2,
                    status="",
                    field="WP4"),4, 0),
          (Game(  "2015-05-12",
                    "12:45",
                    37,
                    20,
                    2,
                    status="",
                    field="WP1"),10, 8),
          (Game(  "2015-05-12",
                    "12:45",
                    23,
                    31,
                    2,
                    status="",
                    field="WP2"),19, 7),
          (Game(  "2015-05-12",
                    "12:45",
                    9,
                    36,
                    2,
                    status="",
                    field="WP3"),12, 1),
          (Game(  "2015-05-12",
                    "12:45",
                    14,
                    34,
                    2,
                    status="",
                    field="WP4"),3, 2),
          (Game(  "2015-05-12",
                    "13:45",
                    11,
                    30,
                    2,
                    status="",
                    field="WP1"),29, 1),
          (Game(  "2015-05-12",
                    "13:45",
                    16,
                    29,
                    2,
                    status="",
                    field="WP2"),5, 12),
     ]
bat_hash = {1:"s",2:"d", 3:"s",4:"hr"}
for index, game in enumerate(games):
    DB.session.add(game[0])
    home_score = game[1]
    away_score = game[2]
    home_captain_id = Team.query.get(game[0].home_team_id).player_id
    away_captain_id = Team.query.get(game[0].away_team_id).player_id
    while home_score > 0:
        home_score -= 1
        r = randint(1,2)
        if r == 1:
            # assigned to captain
            bat = Bat(home_captain_id,
                      game[0].home_team_id,
                      index+1,
                      bat_hash[randint(1,4)],
                      inning=1,
                      rbi=1)
        else:
            bat = Bat(UNASSIGNED.id,
                         game[0].home_team_id,
                         index+1,
                         "s",
                         inning=1,
                         rbi=1)
        game[0].bats.append(bat)
    while away_score > 0:
        away_score -= 1
        r = randint(1,2)
        if r == 1:
            # assigned to captain
            bat = Bat(away_captain_id,
                         game[0].home_team_id,
                         index+1,
                         bat_hash[randint(1,4)],
                         inning=1,
                         rbi=1)               
        else:
            bat = Bat(UNASSIGNED.id,
                         game[0].home_team_id,
                         index+1,
                         "s",
                         inning=1,
                         rbi=1)
        game[0].bats.append(bat)
# mock up of each team's first two games

# add players to sentry and 
DB.session.commit()
