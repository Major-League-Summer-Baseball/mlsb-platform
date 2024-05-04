# -*- coding: utf-8 -*-
"""Test some authentication methods"""
from api.test.BaseTest import TestSetup
from api.authentication import \
    oauth_service_provider_error, load_user, get_oauth, find_player, \
    is_facebook_supported, is_github_supported, is_gmail_supported
from api.extensions import DB
from api.errors import OAuthException, NotPartOfLeagueException
import uuid


class MockBlueprint():
    """A class for mocking a blueprint"""
    def __init__(self):
        self.name = "MockBlueprint"

    def __str__(self):
        return self.name


class TestWebsiteViews(TestSetup):

    def testProviderError(self):
        """Test an error from service provider"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            try:
                oauth_service_provider_error(MockBlueprint(), "message", {})
                self.assertTrue(False, "Should raise service execption")
            except OAuthException:
                pass

    def testLoadUser(self):
        """Test able to load existing player"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            email = str(uuid.uuid1()) + "@mlsb.ca"
            player = self.add_player(
                str(uuid.uuid1()), email, gender="m"
            )
            load_user(player["player_id"])

    def testGetOauth(self):
        """Test a helper function that looks up OAuth"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            name = str(uuid.uuid1())
            email = str(uuid.uuid1()) + "@mlsb.ca"
            user_id = str(uuid.uuid1())
            oauth = get_oauth(str(MockBlueprint()), user_id, {})
            self.assertTrue(oauth.id is None, "Should create new oauth")
            player = self.add_player(name, email, gender="m")
            oauth.player_id = player['player_id']
            DB.session.add(oauth)
            DB.session.commit()
            oauth = get_oauth(str(MockBlueprint()), user_id, {})
            self.assertTrue(oauth.id is not None, "Should get existing oauth")

    def testFindPlayer(self):
        """Test able to find players and not find player"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            name = str(uuid.uuid1())
            email = str(uuid.uuid1()) + "@mlsb.ca"
            try:
                find_player({"name": name, "email": email})
                self.assertTrue(False, "Found player who does not exist")
            except NotPartOfLeagueException:
                pass
            self.add_player(name, email, gender="m")
            player = find_player({"name": name, "email": email})
            self.assertEqual(
                player.email, email, "Found player email does not match"
            )

    def testProviderHelperFunctions(self):
        """Test some simple boolean methods for the service providers"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            self.assertTrue(isinstance(is_facebook_supported(), bool))
            self.assertTrue(isinstance(is_github_supported(), bool))
            self.assertTrue(isinstance(is_gmail_supported(), bool))
