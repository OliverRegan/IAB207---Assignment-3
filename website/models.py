import email
from flask_wtf import FlaskForm
from wtforms import *
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin


class user(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, unique=True, nullable=False)
    emailId = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Relationship
    events = db.relationship('event', backref='creator')

    def __repr__(self):
        return "<Name: {}>".format(self.name)


class event(db.Model):

    __tablename__ = "events"

    # Init status - to be calculated on page load
    status = ""

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventName = db.Column(db.String(150), unique=True, nullable=False)
    gameType = db.Column(db.String(100), index=True, nullable=False)
    price = db.Column(db.Integer)
    date = db.Column(db.String(30))
    location = db.Column(db.String(255))
    startTime = db.Column(db.String(20))
    endTime = db.Column(db.String(20))
    blurb = db.Column(db.String(500))
    requirements = db.Column(db.String(400))
    description = db.Column(db.String(5000))
    tickets = db.Column(db.Integer)
    status = db.Column(db.String(100))
    creator = db.Column(db.Integer)
    imagePath = db.Column(db.String(255))

    # add image to this

    # Relationships

    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.eventName, self.id)
