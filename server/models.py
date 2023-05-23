from server import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    fullname = db.Column(db.String(255))
    password = db.Column(db.String(255))
    level = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.username

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    costIncl = db.Column(db.Numeric)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
