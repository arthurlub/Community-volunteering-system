from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    area = db.Column(db.String(150))
    type = db.Column(db.Integer, default=1)


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    area = db.Column(db.String(150))
    description = db.Column(db.String(150))
    users = db.relationship('User')
    rating = db.Column(db.Float)
    votersNumber = db.Column(db.Integer)
    pic = db.Column(db.String(150))
    raters = db.Column(db.String)
