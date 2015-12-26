from api import DB
from api.model import Player, Team, Sponsor, Game, League, Bat
DB.create_all()
# add some
DB.session.add(League(name="Monday & Wednesday"))
DB.session.add(League(name="Tuesday & Thursday"))
# add some players
DB.session.add(Player("Dallas Fraser", "fras2560@mylaurier.ca", gender="m"))
DB.session.add(Player("Marc Gallucci", "gall2560@mylaurier.ca", gender="m"))
DB.session.add(Player("Dream Girl", "drea2560@mylaurier.ca", gender="f"))
DB.session.add(Player("Mrs. Gallucci", "gall2561@mylaurier.ca", gender="f"))
# add some sponsors
DB.session.add(Sponsor("Domus"))
DB.session.add(Sponsor("Sentry"))
DB.session.add(Sponsor("Nightschool"))
DB.session.add(Sponsor("Mortys"))
DB.session.add(Sponsor("Sportzone"))
DB.session.add(Sponsor("Fat Bastards"))
DB.session.commit()
s = Sponsor.query.get(1)
print(s)
# add some teams
DB.session.add(Team(
                    color="Green", 
                    sponsor_id=1, 
                    league_id=1, 
                    ))
DB.session.add(Team(
                    color="Sky", 
                    sponsor_id=2, 
                    league_id=1, 
                    ))
DB.session.add(Team(
                    color="Navy", 
                    sponsor_id=3, 
                    league_id=2, 
                    ))
DB.session.add(Team(
                    color="Mauve", 
                    sponsor_id=4, 
                    league_id=1, 
                    ))
DB.session.add(Team(
                    color="Pink", 
                    sponsor_id=5, 
                    league_id=1, 
                    ))
DB.session.add(Team(
                    color="Black", 
                    sponsor_id=6, 
                    league_id=2, 
                    ))
# add some players to a team
domus = Team.query.get(1)
sentry = Team.query.get(2)
night = Team.query.get(3)
domus.players.append(Player.query.get(1))
domus.players.append(Player.query.get(3))
sentry.players.append(Player.query.get(2))
sentry.players.append(Player.query.get(4))
night.players.append(Player.query.get(1))

# create a game
date = "2015-10-01"
time = '11:45'
g = Game(date, time, 1, 2, 1, status="Championship", field="WP1")
g2 = Game(date, time, 3,6,2, status="Semis", field="WP2")
DB.session.add(g)
DB.session.add(g2)


# add guys bats
g.bats.append(Bat(1, 1, 1, "hr", 1,rbi=1))
g.bats.append(Bat(2, 2, 1, "hr", 1,rbi=1))
g.bats.append(Bat(2, 2, 1, "hr", 2,rbi=1))
g2.bats.append(Bat(1, 3, 2, "hr", 2,rbi=1))

# add girls bats
g.bats.append(Bat(3, 1, 1, "ss", 1,rbi=0))
g.bats.append(Bat(4, 2, 1, "ss", 1,rbi=0))
g.bats.append(Bat(4, 2, 1, "ss", 2,rbi=0))

# add players to sentry and 
DB.session.commit()
