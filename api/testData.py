'''
Created on Sep 22, 2015

@author: Dallas
'''
from api import DB
from api.model import Sponsor, Player, Team, Game, Bat, League
from datetime import datetime, date, time
# add sponsors
DB.create_all()
DB.session.add(Sponsor("Domus"))
DB.session.add(Sponsor("SBE"))
DB.session.add(Sponsor("GE"))
DB.session.add(Sponsor("Wilfs"))
DB.session.add(Sponsor("Nightschool"))
# create league and game
d = date(2015, 8, 23)
t = time(11, 37)
d = datetime.combine(d, t)
DB.session.add(League(name="Monday & Wednesday"))
DB.session.add(Team(color="Green",
                    sponsor_id=1,
                    league_id=1)
               )
DB.session.add(Team(color="SBE",
                    sponsor_id=2,
                    league_id=1)
               )
DB.session.add(Game(d, 1, 2, 1))
# add hits and players to the game
DB.session.add(Player("Dallas Fraser", "fras2560@mylaurier.ca", gender="m"))
DB.session.add(Player("Marc Gallucci", "gall2560@mylaurier.ca", gender="m"))
DB.session.add(Bat(1, 1, 1,"s", 1,))
DB.session.add(Bat(2, 1, 1,"d", 1,))
DB.session.add(Bat(1, 1, 1,"hr", 1, 3))


DB.session.commit()

