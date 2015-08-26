'''
Created on Aug 21, 2015

@author: Dallas
'''
import os
from flask import Flask, g, request
from flask.ext.restful import Api
from flask.ext.restful.utils import cors
from flask.ext.sqlalchemy import SQLAlchemy
from api.credentials import PWD, URL

#create the application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URL
DB = SQLAlchemy(app)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

api = Api(app)
api.decorators=[cors.crossdomain(origin='*',headers=['accept', 'Content-Type'])]