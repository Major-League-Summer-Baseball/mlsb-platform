from api import DB
from api.model import Player, Team, Sponsor, Game, League, Bat, Espys, Fun
from random import randint
from api.variables import UNASSIGNED_EMAIL
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
            Sponsor("Fat Bastard Burrito", link="https://www.facebook.com/FatBastardBurritoCo.Waterloo?fref=ts", active=False),
            Sponsor("Frites", link="https://www.facebook.com/frieswithbenefits?fref=ts", active=False),
            Sponsor("Gatorade", link="http://www.pepsicojobs.com/en-ca"),
            Sponsor("Spitz", link="http://www.pepsicojobs.com/en-ca"),
            Sponsor("GE", link="http://www.ge.com/ca/careers", active=False),
            Sponsor("Gino's Pizza", link="http://www.ginospizza.ca/", nickname="Gino's"),
            Sponsor("Huether Hotel", link="https://www.facebook.com/HuetherHotel?fref=ts", active=False),
            Sponsor("Kik", link="http://www.kik.com/careers/"),
            Sponsor("Maxwell's", link="http://maxwellswaterloo.com/", active=False),
            Sponsor("Mel's Diner", link="https://www.facebook.com/Melsdinerwaterloo?fref=ts", nickname="Mel's"),
            Sponsor("Morty's Pub",link="https://www.facebook.com/MortysPub?fref=ts", nickname="Morty's"),
            Sponsor("Night School",link="https://www.facebook.com/NightSchoolWaterloo"),
            Sponsor("Owl Rafting",link="http://www.owl-mkc.ca/owl/", active=False),
            Sponsor("Pita Factory",link="http://www.pitafactory.com/", active=False),
            Sponsor("Reds Whites and Brews",link="http://www.redswhitesandbrews.ca/", nickname="RWB"),
            Sponsor("SBESS",link="https://www.facebook.com/LazSoc/?fref=ts", active=False),
            Sponsor("Sentry",link="Shoeless Joe's - Waterloo", active=False),
            Sponsor("Shoeless Joe's",link="https://www.facebook.com/ShoelessJoesWaterloo?fref=ts", nickname="Shoeless"),
            Sponsor("Sleeman",link="https://www.facebook.com/SleemanBeer?fref=ts"),
            Sponsor("Snapple Vodka",link="http://www.snapple.com/", active=False),
            Sponsor("SportZone",link="https://www.facebook.com/sportszonecanada?fref=ts"),
            Sponsor("Traces",link="http://traces.com/", active=False),
            Sponsor("Turret Nightclub",link="https://www.facebook.com/turretnightclub?fref=ts", nickname="Turret"),
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
            Sponsor("Smoke's Poutine", link="https://www.facebook.com/SmokesPoutinerieWaterloo/", nickname="Smoke's"),
            Sponsor("Stark & Perri", link="https://www.facebook.com/Stark-Perri-1504025033225383/?fref=ts"),
            Sponsor("Taco Farm", link="https://www.facebook.com/tacofarmco/?fref=ts"),
            Sponsor("Tilt", link="https://www.tilt.com/en-ca/tilts/new"),
            Sponsor("Menchies", link="https://www.facebook.com/pages/Menchies-Waterloo/240980822616062?fref=ts"),
            Sponsor("Pabst", link="http://pabstblueribbon.com/"),
            Sponsor('Team LTD', link="https://www.teamltdshop.com/"),
            Sponsor('PRISM Resources', link="https://prismresources.ca/")
          ]
for sponsor in sponsors:
    DB.session.add(sponsor)
DB.session.commit()
player = Player("UNASSIGNED", UNASSIGNED_EMAIL,gender="F",  active=False)
DB.session.add(player)
DB.session.commit()
