import json
import uuid
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session
from sqlalchemy.dialects.postgresql import JSON

class Asset_DBModel(db.Model):
	__tablename__ = 'assets'
	recipe_id = db.Column(db.Text, db.ForeignKey('recipe__db_model.id', ondelete='CASCADE'), primary_key = True)
	user_id = db.Column(db.Text, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key = True)

	def __init__(self, recipe_id, user_id):
		self.recipe_id = recipe_id
		self.user_id = user_id

	def __repr__(self):
		return 'id {}'.format(self.recipe_id)
