'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Holds the authentication functions
'''
from functools import wraps
from flask import request, Response
from flask import session
import os

ADMIN = os.environ.get('ADMIN', 'admin')
PASSWORD = os.environ.get('PASSWORD', 'password')


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == ADMIN and password == PASSWORD


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        elif 'admin' in session and 'password' in session:
            # check if user signed in already
            logged = check_auth(session['admin'], session['password'])
            if not logged:
                return authenticate()
        return f(*args, **kwargs)
    return decorated
