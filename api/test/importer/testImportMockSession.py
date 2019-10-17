'''
@author: Dallas Fraser
@date: 2019-04-03
@organization: MLSB API
@summary: Mock DB session so objects added are removed upon tear down
'''
from api.model import Team, Game, Player
from api import DB


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
            if (type(obj) == Game):
                self.tester.games_to_delete.append(obj.id)
            elif (type(obj) == Player):
                self.tester.players_to_delete.append(obj.id)
            elif (type(obj) == Team):
                self.tester.teams_to_delete.append(obj.id)
