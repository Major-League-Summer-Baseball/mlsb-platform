'''
@author: Dallas Fraser
@date: 2019-03-13
@organization: MLSB API
@summary: Tests all the basic fun APIS
'''

from api.routes import Routes
from api.errors import InvalidField, FunDoesNotExist
from base64 import b64encode
from api.test.BaseTest import \
    TestSetup, ADMIN, PASSWORD, SUCCESSFUL_GET_CODE, \
    INVALID_ID, SUCCESSFUL_PUT_CODE


headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
MISSING_PARAMETER = ('Missing required parameter in the JSON body ' +
                     'or the post body or the query string')


class TestBasicFun(TestSetup):

    def testFunInvalidPost(self):
        # Note Valid Requests are tested in BaseTest method add_fun

        # missing parameters
        params = {}
        result = {'message': {'year': MISSING_PARAMETER}}
        error_message = Routes['fun'] + " POST: request with missing parameter"
        self.postInvalidTest(Routes['fun'],
                             params,
                             InvalidField.status_code,
                             self.assertEqual,
                             result,
                             error_message=error_message)

    def testFunListAPI(self):
        # add some fun
        self.add_fun(100, year=1900)

        # test a get with funs
        error_message = Routes['fun'] + " GET Failed to return list of funs"
        self.getListTest(Routes['fun'], error_message=error_message)

    def testFunAPIGet(self):
        # insert a fun object
        fun = self.add_fun(100, year=1900)

        # invalid year
        expect = {'details': INVALID_ID, "message": FunDoesNotExist.message}
        self.getTest(Routes['fun'] + "/" + str(INVALID_ID),
                     FunDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['fun'] + " Get: Invalid Fun")

        # valid year
        self.getTest(Routes['fun'] + "/" + str(fun['year']),
                     SUCCESSFUL_GET_CODE,
                     self.assertFunModelEqual,
                     fun,
                     error_message=Routes['fun'] + " Get: valid Fun")

    def testFunAPIDelete(self):
        # insert a fun object
        fun = self.add_fun(100, year=1900)

        # testing deleting a invalid fun year
        error_message = Routes['fun'] + "DELETE: valid fun"
        self.deleteValidTest(Routes['fun'],
                             FunDoesNotExist.status_code,
                             self.assertFunModelEqual,
                             fun['year'],
                             fun,
                             FunDoesNotExist.message,
                             error_message=error_message)

        # testing deleting invalid fun year
        error_message = Routes['fun'] + "DELETE: invalid fun"
        self.deleteInvalidTest(Routes['fun'],
                               FunDoesNotExist.status_code,
                               FunDoesNotExist.message,
                               error_message=error_message)

    def testFunAPIPut(self):
        # insert a fun object
        fun = self.add_fun(100, year=1900)
        updated_count = 50

        # invalid year
        params = {'count': updated_count}
        expect = {'details': INVALID_ID, "message": FunDoesNotExist.message}
        self.putTest(Routes['fun'] + "/" + str(INVALID_ID),
                     params,
                     FunDoesNotExist.status_code,
                     self.assertEqual,
                     expect,
                     error_message=Routes['fun'] + " Put: Invalid Fun"
                     )

        # valid year
        self.putTest(Routes['fun'] + "/" + str(fun['year']),
                     params,
                     SUCCESSFUL_PUT_CODE,
                     self.assertEqual,
                     None,
                     error_message=Routes['fun'] + " Put: valid Fun"
                     )
        fun['count'] = updated_count
        # now try to get it
        self.getTest(Routes['fun'] + "/" + str(fun['year']),
                     SUCCESSFUL_GET_CODE,
                     self.assertFunModelEqual,
                     fun,
                     error_message=Routes['fun'] + " Get: valid Fun")
