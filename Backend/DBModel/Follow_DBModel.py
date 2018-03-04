import json
import uuid
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session
from sqlalchemy.dialects.postgresql import JSON
import datetime

class Follow_DBModel(db.Model):
	__tablename__ = 'follows_db'
	id = db.Column(db.Text, db.ForeignKey('users.id', ondelete = 'CASCADE'), primary_key = True)
	followers = db.Column(db.Text, db.ForeignKey('users.id', ondelete = 'CASCADE'), primary_key = True)


	def __init__(self, i, followers):
		self.id = i
		self.followers = followers

	