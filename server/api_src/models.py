"""
Module for declaring database models, and their marshmallow schemas
"""
from datetime import datetime
from marshmallow import fields

from api_src.db import DB
from api_src.schema import JsonApiSchema


class User(DB.Model):
    """User database model"""
    __tablename__ = 'users'

    id = DB.Column(DB.Integer, nullable=False, autoincrement=True, primary_key=True)
    username = DB.Column(DB.String(80), unique=True, nullable=False)
    email = DB.Column(DB.String(120), nullable=False)
    password_hash = DB.Column(DB.String(64), nullable=False)
    create_date = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
    items = DB.relationship('Item', backref='user', lazy=True)


class Location(DB.Model):
    """Location database model"""
    __tablename__ = 'locations'

    id = DB.Column(DB.Integer, nullable=False, autoincrement=True, primary_key=True)
    name = DB.Column(DB.String(120), nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey(User.__tablename__ + '.id'), nullable=False)


class Item(DB.Model):
    """Item database model"""
    __tablename__ = 'items'

    id = DB.Column(DB.Integer, nullable=False, autoincrement=True, primary_key=True)
    create_date = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
    user_id = DB.Column(DB.Integer, DB.ForeignKey(User.__tablename__ + '.id'), nullable=False)
    location = DB.Column(DB.Integer, DB.ForeignKey(Location.__tablename__ + '.id'), nullable=True)
    description = DB.Column(DB.Text, nullable=True)
    name = DB.Column(DB.Text, nullable=False)

    purchase_date = DB.Column(DB.DateTime, nullable=True)
    purchase_price = DB.Column(DB.Numeric(precision=19, scale=4, asdecimal=True), nullable=True)
    sell_date = DB.Column(DB.DateTime, nullable=True)
    sell_price = DB.Column(DB.Numeric(precision=19, scale=4, asdecimal=True), nullable=True)
    listed_price = DB.Column(DB.Numeric(precision=19, scale=4, asdecimal=True), nullable=True)

    pictures = DB.relationship("Picture", cascade="all,delete", backref="item")


class Picture(DB.Model):
    """Picture database model"""
    __tablename__ = 'pictures'

    id = DB.Column(DB.Integer, nullable=False, autoincrement=True, primary_key=True)
    create_date = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
    item_id = DB.Column(DB.Integer, DB.ForeignKey(Item.__tablename__ + '.id'), nullable=False)
    path = DB.Column(DB.Text, nullable=False)


class PictureSchema(JsonApiSchema):
    """Picture marshmallow schema"""
    _object_class = Picture

    id = fields.Integer()
    create_date = fields.DateTime()
    item_id = fields.Integer()
    path = fields.String()


class LocationSchema(JsonApiSchema):
    """Location marshmallow schema"""
    _object_class = Location

    id = fields.Integer()
    name = fields.String()
    user_id = fields.Integer()


class ItemSchema(JsonApiSchema):
    """Item marshmallow schema"""
    _object_class = Item

    id = fields.Integer()
    create_date = fields.DateTime()
    user_id = fields.Integer()
    location_id = fields.Integer()
    description = fields.String()
    name = fields.String()
    purchase_date = fields.DateTime()
    purchase_price = fields.Decimal(places=19, as_string=True)
    sell_date = fields.DateTime()
    sell_price = fields.Decimal(places=19, as_string=True)
    listed_price = fields.Decimal(places=19, as_string=True)
    pictures = fields.List(fields.Nested(PictureSchema))


class UserSchema(JsonApiSchema):
    """User marshmallow schema"""
    _object_class = User

    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    password_hash = fields.String()
    create_date = fields.DateTime()
    items = fields.List(fields.Nested(ItemSchema))
