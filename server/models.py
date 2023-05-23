from server import db, ma
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
    type = db.Column(db.Integer)
    description = db.Column(db.String(255))
    img_path = db.Column(db.String(255))
    costIncl = db.Column(db.Numeric)
class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "type", "description", "img_path", "costIncl")
    
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
