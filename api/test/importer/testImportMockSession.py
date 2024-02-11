from api.model import Team, Game, Player
from api.extensions import DB


class TestImportMockSession():

    def __init__(self, tester):
        """Constructor given a testing object"""
        self.tester = tester
        self.objs = []

    def add(self, obj):
        """Add the give model object"""
        self.objs.append(obj)
        DB.session.add(obj)

    def commit(self):
        """Commits all given objects in a session"""
        DB.session.commit()
        for obj in self.objs:
            if (type(obj) is Game):
                self.tester.games_to_delete.append(obj.id)
            elif (type(obj) is Player):
                self.tester.players_to_delete.append(obj.id)
            elif (type(obj) is Team):
                self.tester.teams_to_delete.append(obj.id)
