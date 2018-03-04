from flask import Flask
from flask import request

from flaskapp import app, db
from Model.Recipe import Recipe
from Model.User import User

db.create_all()

@app.after_request
def apply_caching(response):
	response.headers["Access-Control-Allow-Credentials"] = "true"
	return response

if __name__ == '__main__':
	app.run(host = "0.0.0.0", port = 5000)