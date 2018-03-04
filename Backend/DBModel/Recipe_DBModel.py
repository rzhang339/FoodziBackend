import json
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
import datetime

class Recipe_DBModel(db.Model):
    id = db.Column(db.Text, primary_key = True)
    name = db.Column(db.Text)
    created_by = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    ingredients = db.Column(db.Text)
    directions = db.Column(db.Text)
    likes = db.Column(db.Integer)

    def __init__(self, id, name, created_by, date_created, ingredients, directions, likes):
        self.id = id
        self.name = name
        self.created_by = created_by
        self.date_created = date_created
        self.ingredients = ingredients
        self.directions = directions
        self.likes = likes

    def __repr__(self):
        return 'id {}'.format(self.id)