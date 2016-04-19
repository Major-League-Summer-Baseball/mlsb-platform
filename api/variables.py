'''
Name: Dallas Fraser
Date: 2016-04-12
Project: MLSB API
Purpose: Holds constant variables that used
'''
NOTFOUND = "notFound.png"
SPONSORS = {0: "notFound.png",
            1: "domus.jpg",
            2: "sentry.jpeg", 
            3: "nightschool.jpg", 
            4: "mortys.jpg",
            5: "sportszone.jpg"} # maps the sponsors to their pictures
TEAMS = {
         0: "noTeam.png",
         } # maps the teams to their picture
UNASSIGNED = 1 # the UNASSIGNED player id used for bats that are not assigned to a player
HITS = ["s", "ss", "d", "hr"] # the hits that are available
BATS = ['s', 'd', 'ss', 'hr', 'k', 'e','fc', 'fo','go'] # all the possible results from a bat
GENDERS = ["f", "m"] # the genders currently supported
EVENTS = {2016: {
                  "Beerfest": "May 14th",
                  "ESPYS_Awards": "July 27th",
                  "Jays_Game": "May 17th",
                  "Summerween": "June 11th",
                  "Mystery_Bus" : "March 19th",
                  "Rafting": "July 9th",
                  "Hitting_for_the_Cycle": "July 16th",
                  "Beerwell_Classic": "July 23rd",
                  "Tournaments": "May 21st, May27th, July 15th, July 22ond"}
          } # all the events baby
FIELDS = ["WP1", "WP2", "WP3", "WP4", "Hillside Upper", "Hillside Lower"] # the fields we play at
KIKPOINTS = 2 # the kik points assigned for subscription
