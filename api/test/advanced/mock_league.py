from uuid import uuid1
import datetime


class MockLeague():

    def __init__(self, tester):
        # add a league
        self.division = tester.add_division(str(uuid1()))
        self.league = tester.add_league(str(uuid1()))
        self.sponsor = tester.add_sponsor(str(uuid1()))
        self.field = "WP1"

        # add some players
        names = [str(uuid1()) for i in range(0, 4)]
        players = [(names[0], names[0] + "@testing.ca", "M"),
                   (names[1], names[1] + "@testing.ca", "F"),
                   (names[2], names[2] + "@testing.ca", "M"),
                   (names[3], names[3] + "@testing.ca", "F")]
        self.players = []
        for player in players:
            self.players.append(tester.add_player(player[0],
                                                  player[1],
                                                  gender=player[2]))

        # add some teams
        teams = [(str(uuid1()), self.sponsor, self.league),
                 (str(uuid1()), self.sponsor, self.league)]
        self.teams = []
        for team in teams:
            self.teams.append(tester.add_team(team[0],
                                              sponsor=team[1],
                                              league=self.league))

        # add the players to some teams
        tester.add_player_to_team(self.teams[0], self.players[0], captain=True)
        tester.add_player_to_team(self.teams[0], self.players[1])
        tester.add_player_to_team(self.teams[1], self.players[2])
        tester.add_player_to_team(self.teams[1], self.players[3], captain=True)

        # add some games between the teams
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        if (week_ago.year != today.year):
            week_ago = datetime.datetime.combine(
                datetime.date(today.year, 1, 1), datetime.time(0, 0))
        next_week = today + datetime.timedelta(days=3)
        if (next_week.year != today.year):
            next_week = datetime.datetime.combine(
                datetime.date(today.year, 1, 1), datetime.time(18, 0))
        last_week_string = week_ago.strftime("%Y-%m-%d")
        today_string = today.strftime("%Y-%m-%d")
        next_week_string = next_week.strftime("%Y-%m-%d")
        games = [(last_week_string,
                  "10:00",
                  self.teams[0],
                  self.teams[1],
                  self.league,
                  self.division,
                  self.field),
                 (today_string,
                  "10:00",
                  self.teams[1],
                  self.teams[0],
                  self.league,
                  self.division,
                  self.field),
                 (next_week_string,
                  "10:00",
                  self.teams[0],
                  self.teams[1],
                  self.league,
                  self.division,
                  self.field),
                 ]
        self.games = []
        for game in games:
            self.games.append(tester.add_game(game[0],
                                              game[1],
                                              game[2],
                                              game[3],
                                              game[4],
                                              game[5],
                                              field=game[6]))

        # add some bats to the games
        bats = [(self.players[0], self.teams[0], self.games[0], "K", 0),
                (self.players[0], self.teams[0], self.games[0], "HR", 1),
                (self.players[1], self.teams[0], self.games[0], "SS", 0),
                (self.players[1], self.teams[0], self.games[0], "GO", 0),
                (self.players[2], self.teams[1], self.games[0], "S", 0),
                (self.players[2], self.teams[1], self.games[0], "D", 2),
                (self.players[3], self.teams[1], self.games[0], "HR", 4),
                (self.players[3], self.teams[1], self.games[0], "GO", 0),
                ]
        self.bats = []
        for bat in bats:
            self.bats.append(tester.add_bat(bat[0],
                                            bat[1],
                                            bat[2],
                                            bat[3],
                                            rbi=bat[4]))

    def get_league(self):
        return self.league

    def get_sponsor(self):
        return self.sponsor

    def get_field(self):
        return self.field

    def get_players(self):
        return self.players

    def get_bats(self):
        return self.bats

    def get_games(self):
        return self.games

    def get_teams(self):
        return self.teams

    def get_division(self):
        return self.division

    def get_player_email(self, index):
        name = self.players[index]['player_name'].replace(" ", "")
        return name + "@testing.ca"
