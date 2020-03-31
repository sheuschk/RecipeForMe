from app import db
from sqlalchemy import Integer, ForeignKey, String, Float


class Cocktail(db.Model):
    __tablename__ = 'cocktail'
    key = db.Column(Integer, primary_key=True)
    name = db.Column(String(64), index=True, unique=True)
    desc = db.Column(String(180), index=True)
    ingredients = db.relationship('Ingredient', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Cocktail: {}>'.format(self.name)


class Ingredient(db.Model):
    __tablename__ = "ingredient"
    key = db.Column(Integer, primary_key=True)
    cocktail_key = db.Column(Integer, ForeignKey('cocktail.key'))
    name = db.Column(String, index=True)
    quantity = db.Column(Float, index=True)

    def __repr__(self):
        return '<{}: {} of {}>'.format(self.name, self.quantity, self.cocktail_key)
