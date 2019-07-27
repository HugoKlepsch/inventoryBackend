from datetime import datetime

from db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship('Item', backref='user', lazy=True)

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__ + '.id'), nullable=False)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__ + '.id'), nullable=False)
    location = db.Column(db.Integer, db.ForeignKey(Location.__tablename__ + '.id'), nullable=True)
    description = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=False )

    purchase_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    purchase_price = db.Column(db.Numeric(precision=19, scale=4, asdecimal=True), nullable=True)
    sell_date = db.Column(db.DateTime, nullable=True)
    sell_price = db.Column(db.Numeric(precision=19, scale=4, asdecimal=True), nullable=True)
    listed_price = db.Column(db.Numeric(precision=19, scale=4, asdecimal=True), nullable=True)

    children = db.relationship("Picture", cascade="all,delete", backref="item")


class Picture(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    item_id = db.Column(db.Integer, db.ForeignKey(Item.__tablename__ + '.id'), nullable=False)
    path = db.Column(db.Text, nullable=False)

