import json
import uuid
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session
from sqlalchemy.dialects.postgresql import JSON
import datetime

class User_DBModel(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Text, primary_key = True)
	email = db.Column(db.Text)
	name = db.Column(db.Text)
	password = db.Column(db.Text)


	def __init__(self, id, name, password, email):
		self.id = id
		self.name = name
		self.password = password
		self.email = email
		

	@staticmethod
	def authenticate_email_password(email, password):
		if not email or not password:
			return False
		user_info = User_DBModel.query.filter_by(email = email).first()
		if user_info is None:
				return None
		if user_info.password is not None:
				if user_info.password == password:
						return user_info
		return None