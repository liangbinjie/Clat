from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now(-6))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # No email will be used twice if unique is set to True
    name = db.Column(db.String(150)) # as well as username, go to auth login
    password = db.Column(db.String(150))
    notes = db.relationship('Note')


class Clat(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    clatname = db.Column(db.String(150), unique=True) # as well as username, go to auth login
    clatpassword = db.Column(db.String(150))
