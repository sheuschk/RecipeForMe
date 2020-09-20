from flask import current_app
from app import db, login
from time import time
import jwt
from sqlalchemy import Integer, ForeignKey, String
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Cocktail(db.Model):
    __tablename__ = 'cocktail'
    __searchable__ = ['name']
    key = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), index=True, unique=True)
    desc = db.Column(String(400), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    picture = db.Column(String(64), index=True, unique=True, default=None)
    ingredients = db.relationship('Ingredient', backref='parent', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Recipe: {}>'.format(self.name)

    " A was_published_recently function would be nice"


class Ingredient(db.Model):
    __tablename__ = "ingredient"
    key = db.Column(Integer, primary_key=True)
    cocktail_key = db.Column(Integer, ForeignKey('cocktail.key'))
    name = db.Column(String, index=True)
    quantity = db.Column(String, index=True)

    def __repr__(self):
        return '<{}: {} of {}>'.format(self.name, self.quantity, self.cocktail_key)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cocktails = db.relationship('Cocktail', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
