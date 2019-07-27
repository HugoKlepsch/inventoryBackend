from datetime import datetime
from marshmallow import fields

from db import db
from schema import ObjectSchema


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

    pictures = db.relationship("Picture", cascade="all,delete", backref="item")


class Picture(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    item_id = db.Column(db.Integer, db.ForeignKey(Item.__tablename__ + '.id'), nullable=False)
    path = db.Column(db.Text, nullable=False)


class PictureSchema(ObjectSchema):
    _object_class = Picture

    id = fields.Integer()
    create_date = fields.DateTime()
    item_id = fields.Integer()
    path = fields.String()


class LocationSchema(ObjectSchema):
    _object_class = Location

    id = fields.Integer()
    name = fields.String()
    user_id = fields.Integer()


class ItemSchema(ObjectSchema):
    _object_class = Item

    id = fields.Integer()
    create_date = fields.DateTime()
    user_id = fields.Integer()
    location = fields.Nested(LocationSchema)
    description = fields.String()
    name = fields.String()
    purchase_date = fields.DateTime()
    purchase_price = fields.Decimal(places=19, as_string=True)
    sell_date = fields.DateTime()
    sell_price = fields.Decimal(places=19, as_string=True)
    listed_price = fields.Decimal(places=19, as_string=True)
    pictures = fields.List(fields.Nested(PictureSchema))


class UserSchema(ObjectSchema):
    _object_class = User

    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    password_hash = fields.String()
    create_date = fields.DateTime()
    items = fields.List(fields.Nested(ItemSchema))
