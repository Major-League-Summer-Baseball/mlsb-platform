'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced fun APIs
'''
from datetime import date
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, KIK, KIKPW

headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
kik = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' +
                                                  KIKPW, "utf-8")
                                            ).decode("ascii")
}
VALID_YEAR = date.today().year
INVALID_YEAR = 100


class TestFun(TestSetup):

    def testPost(self):
        """Test fun view"""
        params = {'year': 2002}
        rv = self.app.post(Routes['vfun'], data=params)
        expect = [{'count': 89, 'year': 2002}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vfun'] +
                         " View: on 2012 year")

        # get all the years
        params = {}
        rv = self.app.post(Routes['vfun'], data=params)
        expect = {'count': 89, 'year': 2002}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data)[0], Routes['vfun'] +
                         " View: on 2012 year")
