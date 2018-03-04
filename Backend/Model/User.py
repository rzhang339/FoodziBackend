import json
import uuid
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session
from sqlalchemy.dialects.postgresql import JSON
from DBModel.User_DBModel import User_DBModel
from DBModel.Follow_DBModel import Follow_DBModel
from DBModel.Asset_DBModel import Asset_DBModel
import datetime


class User():

	@staticmethod
	def isLoggedIn():
		return make_response(str('user' in session.keys()))

	@staticmethod
	def login():

		parsed_json = request.get_json()
		email = parsed_json["email"]
		password = parsed_json["password"]

		user_info = User_DBModel.authenticate_email_password(email, password)
		if user_info is not None:
			#then this data is good, and we're in.

			user = {'id': user_info.id, 'email' : email, 'password' : password}
			
			if 'user' in session.keys():
				dict_local = {'code': 200, 'message': "already logged in"}
			else:
				session['user'] = user
				session.modified=True
				dict_local = {'code': 200}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			response = make_response(return_string)  
			return response
		else:
			#not a good cookie and no login.
			dict_local = {'code': 31, 'message': "login failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def logoff():
		if 'user' not in session.keys():
			dict_local = {'code': 31, 'message': "User not logged in anyways."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			session.pop('user', None)
			session.modified = True
			dict_local = {'code': 200}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string


	@staticmethod
	def list_all_users():
		if 'user' in session.keys():
			user = session['user']
			
			db_user_devices = User_DBModel.query.all()
			return_json_list = []
			for report in db_user_devices:
				dict_local = {'id': report.id,
												'name': report.name,
												'email': report.email,
												'password' : report.password,
												'tags': report.tags
												}

				return_json_list.append(dict_local)
			return_string = json.dumps(return_json_list, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
			
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def register_user():
		parsed_json = request.get_json()
		email = parsed_json["email"]
		password = parsed_json["password"]
		name = parsed_json["name"]
	

		if User_DBModel.query.filter_by(email = email).first() is None:
			id = str(uuid.uuid4())
			user = User_DBModel(id, name, password, email)

			db.session.add(user)
			db.session.commit()

			return_json = {'code': 200}
			return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			return_json = {'code': 31, 'message': 'Email already taken.'}
			return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	def add_new_recipe():
		if 'user' in session.keys():
			user = session['user']
			parsed_json = request.get_json()

			asset = Asset_DBModel(parsed_json['recipe_id'], user['id'])
			db.session.add(asset)

			db.session.commit()
			return_dict = {'code': 200}
			return_string = json.dumps(return_dict, sort_keys=True, indent=4, seperators=(',',': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	def unsave_recipe():
		user = session['user']
		parsed_json = request.get_json()

		asset = Asset_DBModel.query.filter(Asset_DBModel.recipe_id == parsed_json["recipe_id"]).filter(Asset_DBModel.user_id == user['id']).first()
		db.session.delete(asset)
		db.session.commit
		return_dict = {'code': 200}
		return_string = json.dumps(return_dict, sort_keys=True, indent=4, seperators=(',',': '))
		return return_string


	def add_user_following():
	
		if 'user' in session.keys:
			user = session['user']
			parsed_json = request.get_json()
			user_following = parsed_json["added_following"]
			follow = Follow_DBModel(user['id'], user_following)
			
			db.session.add(follow)
			db.session.commit()
			return_dict = {'code': 200}
			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',',':'))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	def remove_user_following():
	
		if 'user' in session.keys():
			user = session['user']
			parsed_json = request.get_json()
			
			user_following = parsed_json['added_following']
			isTrue = (Follow_DBModel.followers == user_following)
			print(isTrue)
			unfollow = Follow_DBModel.query.filter(Follow_DBModel.id is user["id"]).filter(Follow_DBModel.followers is user_following).first()
			if (unfollow is None):
				dict_local = {'code': 31, 'message': "auth error"}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			
			db.session.delete(unfollow)
		
			db.session.commit()
		
			return_dict = {'code': 200}
			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',',': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
	

	@staticmethod
	def update_user_info():
		if 'user' in session.keys():
			user = session['user']
			parsed_json = request.get_json()
			user_info = User_DBModel.query.filter_by(id = user["id"]).first()

			if 'email' in parsed_json:
				user_info.email = parsed_json['email']
			if 'password' in parsed_json:
				user_info.password = parsed_json['password']
			if 'name' in parsed_json:
				user_info.name = parsed_json['name']


			db.session.commit()

			return_dict = {'code': 200}
			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def get_user_info():
		if 'user' in session.keys():
			user = session['user']
			user_info = User_DBModel.query.filter_by(id = user["id"]).first()

			return_dict = {
				'id': user_info.id,
				'email': user_info.email,
				'name': user_info.name,
				'following': user_info.following,
				'followers': user_info.followers
			}

			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

app.add_url_rule('/isLoggedIn', 'isLoggedIn', User.isLoggedIn, methods=['GET'])
app.add_url_rule('/login', 'login', User.login, methods=['POST'])
app.add_url_rule('/logoff', 'logoff', User.logoff, methods=['GET'])
app.add_url_rule('/list_all_users', 'list_all_users', User.list_all_users, methods=['GET'])
app.add_url_rule('/register_user', 'register_user', User.register_user, methods=['POST'])


app.add_url_rule('/add_user_following', 'add_user_following', User.add_user_following, methods=['POST'])
app.add_url_rule('/remove_user_following', 'remove_user_following', User.remove_user_following, methods=['POST'])

app.add_url_rule('/get_user_info', 'get_user_info', User.get_user_info, methods=['GET'])
app.add_url_rule('/update_user_info', 'update_user_info', User.update_user_info, methods=['POST'])
app.add_url_rule('/unsave_recipe', 'unsave_recipe', User.unsave_recipe, methods=['POST'])
