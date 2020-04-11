from app import db, login
from sqlalchemy import Integer, ForeignKey, String
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Cocktail(db.Model):
    __tablename__ = 'cocktail'
    key = db.Column(Integer, primary_key=True)
    name = db.Column(String(64), index=True, unique=True)
    desc = db.Column(String(180), index=True)
    ingredients = db.relationship('Ingredient', backref='author', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Cocktail: {}>'.format(self.name)

    " A was_published_recently function with timestamps in teh Cocktail would be nice"


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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
