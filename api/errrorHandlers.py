'''
@author: Dallas Fraser
@author: 2015-11-21
@organization: MLSB API
@summary: Holds the error handlers for the database
'''

from api import app
from api.errors import InvalidField, NonUniqueEmail
from flask import Response
from json import dumps

@app.errorhandler(InvalidField)
def handle_invalid_field(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return  response

@app.errorhandler(NonUniqueEmail)
def handle_duplicate_email(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return  response


