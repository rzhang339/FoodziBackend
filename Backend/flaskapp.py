from flask import Flask
from flask import request

#from authentication import UserAuthentication
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask('Foodzi')

# app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://foodzi:elephants_remember_1984@localhost/foodzi'
app.config['COOKIE_KEY'] = b'Zwo81Qe3Pi7aAHnsPVGkjyW2FApg9ekJVN26iWPRps4='
CORS(app)
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SECRET_KEY'] = 'Zwo81Qe3Pi7aAHnsPVGkjyW2FApg9ekJVN26iWPRps4='
app.config['SESSION_COOKIE_NAME'] = 'foodzi'

Session(app)

db.create_all()