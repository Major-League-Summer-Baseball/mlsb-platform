'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced fun APIs
'''
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD

headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
SOME_YEAR = 100


class TestFun(TestSetup):

    def dataContainFun(self, fun, data):
        """Returns whether the given data contains the expected fun object"""
        for check in data:
            if (check['year'] == fun['year'] and
                    check['count'] == fun['count']):
                return True
        return False

    def testPost(self):
        """Test fun view"""
        fun_count = 100
        self.add_fun(fun_count, year=SOME_YEAR)
        params = {'year': SOME_YEAR}
        first = self.app.post(Routes['vfun'], json=params)
        expect = {'count': fun_count, 'year': SOME_YEAR}
        self.output(loads(first.data))
        self.output(expect)
        self.assertTrue(self.dataContainFun(expect, loads(first.data)),
                        Routes['vfun'] +
                        " View: did not have the expected fun")

        # get all the years
        params = {}
        second = self.app.post(Routes['vfun'], json=params)
        expect = {'count': fun_count, 'year': SOME_YEAR}
        self.output(loads(second.data))
        self.output(expect)
        self.assertTrue(len(loads(second.data)) > 0,
                        "Some fun should have been returned")
        self.assertTrue(self.dataContainFun(expect, loads(second.data)),
                        Routes['vfun'] +
                        " View: did not have the expected fun")
        self.assertTrue(len(loads(first.data)) <= len(loads(second.data)),
                        Routes['vfun'] +
                        " View: filters fun should have less fun")
