'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced player APIs
'''
from datetime import date
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD

headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
CURRENT_YEAR = date.today().year
INVALID_YEAR = 100

ROUTE_VIEW = Routes['vleagueevents']


class LeagueEventTest(TestSetup):

    def testActiveEventsTBD(self):
        """Test active events with no date are TBD"""

        league_event = self.add_league_event(
            "Active Event",
            "<p>test</p>",
            active=True
        )

        rv = self.app.get(f"{ROUTE_VIEW}/{CURRENT_YEAR}")

        events = loads(rv.data)
        my_event = [
            event
            for event in events
            if event['league_event_id'] == league_event['league_event_id']
        ]
        self.assertTrue(
            len(my_event) > 0,
            f"{ROUTE_VIEW} did not return active event"
        )
        self.assertEqual(
            my_event[0]['date'],
            "TBD",
            f"{ROUTE_VIEW} did not fill in date TBD"
        )

    def testNonActiveEventsWithNoDate(self):
        """Test non-active events with no date are not returned"""
        league_event = self.add_league_event(
            "Non-Active Event",
            "<p>test</p>",
            active=False
        )

        rv = self.app.get(f"{ROUTE_VIEW}/{CURRENT_YEAR}")

        events = loads(rv.data)
        my_event = [
            event
            for event in events
            if event['league_event_id'] == league_event['league_event_id']
        ]
        self.assertTrue(
            len(my_event) == 0,
            f"{ROUTE_VIEW} did return non-active event"
        )

    def testActiveEventsWithDate(self):
        """Test active events with a date are given"""
        event_date = f"{CURRENT_YEAR}-10-01"
        league_event = self.add_league_event(
            "Active Event with Date",
            "<p>test</p>",
            active=True
        )
        self.add_league_event_date(
            league_event,
            event_date,
            "10:00"
        )

        rv = self.app.get(f"{ROUTE_VIEW}/{CURRENT_YEAR}")

        events = loads(rv.data)
        my_event = [
            event
            for event in events
            if event['league_event_id'] == league_event['league_event_id']
        ]
        self.assertTrue(
            len(my_event) > 0,
            f"{ROUTE_VIEW} did not return active event"
        )
        self.assertEqual(
            my_event[0]['date'],
            event_date,
            f"{ROUTE_VIEW} did not return event date"
        )

    def testNonActiveEventsWithDate(self):
        """Test non-active events with a date are given"""
        event_date = f"{CURRENT_YEAR}-10-01"
        league_event = self.add_league_event(
            "Non-Active Event with Date",
            "<p>test</p>",
            active=False
        )
        self.add_league_event_date(
            league_event,
            event_date,
            "10:00"
        )

        # test an invalid player id
        rv = self.app.get(f"{ROUTE_VIEW}/{CURRENT_YEAR}")

        events = loads(rv.data)
        my_event = [
            event
            for event in events
            if event['league_event_id'] == league_event['league_event_id']
        ]
        self.assertTrue(
            len(my_event) > 0,
            f"{ROUTE_VIEW} did not return non-active event with date"
        )
        self.assertEqual(
            my_event[0]['date'],
            event_date,
            f"{ROUTE_VIEW} did not return event date"
        )
