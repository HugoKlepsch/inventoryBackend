"""API main"""
import argparse
from functools import wraps
import json
import logging
import os
import re
import bcrypt

from flask import Flask, session, redirect, url_for, send_from_directory
from flask.logging import create_logger
from flask_apispec import marshal_with
from marshmallow import fields
from sqlalchemy.exc import SQLAlchemyError
from webargs.flaskparser import use_args

from api_src.db import DB
from api_src.models import User, Item, Picture, Location
from api_src.models import UserSchema, ItemSchema
from api_src.schema import JSON_CT, INTERNAL_SERVER_ERROR_JSON_RESPONSE, BAD_REQUEST_JSON_RESPONSE, ok_response
from api_src.schema import JsonApiSchema


def create_app():  # {{{
    """
    Get configuration and create the flask instance.

    :return: The flask app instance.
    :rtype: Flask
    """
    _app = Flask(__name__, template_folder='templates')
    _app.secret_key = 'yeetyeetskeetskeet'
    _app.logger = create_logger(_app)
    _app.logger.setLevel(logging.DEBUG)

    db_host = os.environ.get('DBHOST', '127.0.0.1')
    db_port = int(os.environ.get('DBPORT', 5432))
    db_password = os.environ.get('DBPASS', 'notwaterloo')
    db_database = 'inventorydb'
    db_string = 'postgresql://root:{password}@{host}:{port}/{database}'.format(
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_database
    )
    _app.config['SQLALCHEMY_DATABASE_URI'] = db_string
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(_app)

    return _app
# }}}


def setup_database(_app):  # {{{
    """Add some sample data to database"""
    with _app.app_context():
        _app.logger.info('Creating databases')
        DB.drop_all()  # TODO
        DB.create_all()
        DB.session.commit()
        _app.logger.info('Created databases')
        example_user = User.query.filter_by(username='bugmommy').first()
        if example_user is None:
            _app.logger.info('Creating test user')
            example_user = User(username='bugmommy',
                                email='test@email.com',
                                password_hash=hash_password('asdf'))
            DB.session.add(example_user)
            DB.session.commit()

        example_item = Item.query.filter_by(user_id=example_user.id).first()
        if example_item is None:
            _app.logger.info('Creating test item')
            example_item = Item(user_id=example_user.id, name='Test', purchase_price=123,
                                sell_price=2345)
            DB.session.add(example_item)
            example_item_two = Item(user_id=example_user.id, name='Test2', purchase_price=23,
                                    sell_price=5678)
            DB.session.add(example_item_two)
            example_item_three = Item(user_id=example_user.id, name='Test3', purchase_price=1235,
                                      sell_price=778)
            DB.session.add(example_item_three)
            DB.session.commit()

        example_picture = Picture.query.filter_by(item_id=example_item.id).first()
        if example_picture is None:
            _app.logger.info('Creating test picture')
            example_picture = Picture(item_id=example_item.id, path='http://reddit.com')
            DB.session.add(example_picture)
            DB.session.commit()

        example_location = Location.query.filter_by(name='Freelton Market').first()
        if example_location is None:
            _app.logger.info('Creating test location')
            example_location = Location(name='Freelton Market', user_id=example_user.id)
            DB.session.add(example_location)
            DB.session.commit()

        _app.logger.info('Created test user, item, picture and location')
# }}}


def hash_password(password):
    """
    Hash the password with bcrypt.

    :param str password: The password to hash
    :return: The string of hex digits of the hash.
    :rtype: str
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


APP = create_app()
setup_database(APP)


def is_logged_in(as_user=None):
    """
    Check if the requester is logged in

    :param str as_user: Optional username the requester should be logged in as
    :return: Is the requester logged in
    :rtype: bool
    """
    if 'username' in session:
        username = session['username']
        return (User.query.filter_by(username=username).first() is not None) and \
               (as_user is None or username == as_user)
    return False


def logged_in(as_user=None):
    """
    Decorator to ensure a user is logged in before calling decorated function.

    :param str as_user: Optional username the requester should be logged in as
    :return: The decorated function
    :rtype: funct
    """
    def _logged_in(function):
        @wraps(function)
        def __logged_in(*args, **kwargs):
            # just do here everything what you need

            if not is_logged_in(as_user=as_user):
                return {'msg': 'Not logged in'}, 401, JSON_CT

            result = function(*args, **kwargs)

            return result
        return __logged_in
    return _logged_in


def logged_out(redirect_to):
    """
    Decorator to ensure a user is logged out before calling decorated function.

    :param str redirect_to: Optional name of function with route that this should redirect to when logged in.
    :return: The decorated function
    :rtype: funct
    """
    def _logged_out(function):
        @wraps(function)
        def __logged_out(*args, **kwargs):
            # just do here everything what you need

            if is_logged_in():
                if redirect_to is not None:
                    return redirect(url_for(redirect_to))

                return json.dumps({
                    'msg': 'Should not be logged in'
                }), 400, JSON_CT

            result = function(*args, **kwargs)

            return result
        return __logged_out
    return _logged_out


@APP.route('/api/login', methods=['POST'])
@use_args({
    'username': fields.Str(required=True),
    'password': fields.Str(required=True)
})
@marshal_with(JsonApiSchema())
def login(credentials):
    """
    Login API. If credentials are valid, set the session cookie to log the requester in.

    :param dict credentials: The sign in credentials.
    :return: Status of the request. 200 if valid, 400 if not.
    :rtype: tuple[dict, int, dict]
    """
    username = credentials['username']

    user = User.query.filter_by(username=username).first()

    if user is None:
        return BAD_REQUEST_JSON_RESPONSE


    # this check using the built in salt.
    if not bcrypt.checkpw(credentials['password'].encode('utf-8'), user.password_hash):
        return BAD_REQUEST_JSON_RESPONSE

    session['username'] = username
    session['user_id'] = user.id
    return ok_response('Logged in')


@APP.route('/api/signup', methods=['POST'])
@use_args({
    'username': fields.Str(required=True),
    'email': fields.Str(required=True),
    'password': fields.Str(required=True)
})
@marshal_with(JsonApiSchema())
def signup(credentials):
    """
    Signup API. If credentials are valid, set the session cookie to log the requester in.

    :param dict credentials: The sign in credentials.
    :return: Status of the request. 200 if valid, 400 if not.
    :rtype: tuple[dict, int, dict]
    """

    username = credentials.get('username', None)
    email = credentials.get('email', None)
    password = credentials.get('password', None)

    if username is not None and \
            email is not None and \
            password is not None:
        password_hash = hash_password(password)

        if re.match(r'[a-zA-Z0-9_\-]{4,30}', username) is not None:
            APP.logger.info('Creating user %s', username)
            try:
                user = User(username=username, email=email, password_hash=password_hash)
                DB.session.add(user)
                DB.session.commit()
                return ok_response('User created')
            except SQLAlchemyError:
                return INTERNAL_SERVER_ERROR_JSON_RESPONSE

    return BAD_REQUEST_JSON_RESPONSE


@APP.route('/api/all_users', methods=['GET'])
@logged_in(as_user='bugmommy')  # TODO create admin account
@marshal_with(UserSchema(many=True, exclude=['password_hash', 'items']))
def all_users():
    """
    Get all users. Must be logged in as 'bugmommy'.

    :return: All users
    :rtype: list[User]
    """
    return User.query.all()


@APP.route('/api/items', methods=['GET'])
@logged_in()
@marshal_with(ItemSchema(many=True, exclude=['id', 'create_date', 'user_id']))
def items():
    """
    Get all items for the logged in user.

    :return: All items for the logged in user.
    :rtype: list[Item]
    """
    username = session['username']
    user = User.query.filter_by(username=username).first()
    user_items = Item.query.filter_by(user_id=user.id).all() or []
    return user_items


@APP.route('/api/item/<int:item_id>', methods=['DELETE'])
@logged_in()
@marshal_with(JsonApiSchema())
def delete_item(item_id):
    """
    Delete the given item.

    :param int item_id: The id of the item to delete.
    :return: Status of the request. 200 if valid, 400 if not.
    :rtype: tuple[dict, int, dict]
    """
    user_id = session['user_id']
    try:
        row = Item.query.filter_by(id=item_id, user_id=user_id).one()
        DB.session.delete(row)
        DB.session.commit()
        return ok_response('Ok, this has been deleted')

    except SQLAlchemyError as exception:
        APP.logger.error('Failed to delete item %s: %s', item_id, exception)
        return BAD_REQUEST_JSON_RESPONSE


@APP.route('/api/item/<int:item_id>', methods=['GET'])
@logged_in()
@marshal_with(ItemSchema())
def get_item(item_id):
    """
    Get an item for the logged in user.

    :return: Requested item.
    :rtype: Item
    """
    # grab item from the list by id.
    item = Item.query.get(item_id)

    if item is not None:
        return item

    return BAD_REQUEST_JSON_RESPONSE


@APP.route('/api/item', methods=['POST'])
@logged_in()
@use_args(ItemSchema(exclude=['id', 'create_date', 'user_id']))
@marshal_with(JsonApiSchema())
def create_item(item_data):
    """
    Create an item.

    :param dict item_data: Dict with a subset of the Item fields.
    :return: Status of the request. 200 if valid, 400 or 500 if not.
    :rtype: tuple[dict, int, dict]
    """
    user_id = session['user_id']
    location_id = item_data.get('location_id', None)
    description = item_data.get('description', None)
    name = item_data.get('name', None)
    purchase_date = item_data.get('purchase_date', None)
    purchase_price = item_data.get('purchase_price', None)
    sell_date = item_data.get('sell_date', None)
    sell_price = item_data.get('sell_price', None)
    listed_price = item_data.get('listed_price', None)

    if name and ' ' in name:
        return BAD_REQUEST_JSON_RESPONSE
    APP.logger.info('Creating item %s', name)
    try:
        item = Item(user_id=user_id,
                    location_id=location_id,
                    description=description,
                    name=name,
                    purchase_date=purchase_date,
                    purchase_price=purchase_price,
                    sell_date=sell_date,
                    sell_price=sell_price,
                    listed_price=listed_price
                    )
        DB.session.add(item)
        DB.session.commit()
        return ok_response('Added item {name}'.format(name=name))
    except SQLAlchemyError as exception:
        APP.logger.exception('Failed to create item %s: %s', name, exception)
        return INTERNAL_SERVER_ERROR_JSON_RESPONSE


@APP.route('/api/item/<int:item_id>', methods=['PUT'])
@logged_in()
@use_args({"item_id": fields.Integer()}, locations=('query',))
@use_args(ItemSchema(exclude=['id', 'create_date', 'user_id']), locations=('json',))
@marshal_with(JsonApiSchema())
def update_item(_, item_data, item_id):
    """
    Update an item.

    :param dict _: Unused positional argument that use_args needs.
    :param dict item_data: Dict with a subset of the Item fields.
    :param int item_id: id of the item.
    :return: Status of the request. 200 if valid, 400 or 500 if not.
    :rtype: tuple[dict, int, dict]
    """
    user_id = session['user_id']
    name = item_data.get('name', None)

    try:
        item = DB.session.query(Item).filter_by(id=item_id, user_id=user_id)
        if item is None:
            return BAD_REQUEST_JSON_RESPONSE

        concrete_item = item.first()
        item.update({
            Item.location_id: item_data.get('location_id', None) or concrete_item.location_id,
            Item.description: item_data.get('description', None) or concrete_item.description,
            Item.name: item_data.get('name', None) or concrete_item.name,
            Item.purchase_date: item_data.get('purchase_date', None) or concrete_item.purchase_date,
            Item.purchase_price: item_data.get('purchase_price', None) or concrete_item.purchase_price,
            Item.sell_date: item_data.get('sell_date', None) or concrete_item.sell_date,
            Item.sell_price: item_data.get('sell_price', None) or concrete_item.sell_price,
            Item.listed_price: item_data.get('listed_price', None) or concrete_item.listed_price
        })

        DB.session.commit()
        return ok_response('Updated item {name}'.format(name=name))
    except SQLAlchemyError as exception:
        APP.logger.exception('Failed to update item %s, id %d: %s', name, item_id, exception)
        return INTERNAL_SERVER_ERROR_JSON_RESPONSE


@APP.route('/api/logout', methods=['GET', 'POST'])
@marshal_with(JsonApiSchema())
def logout():
    """
    Log out the requester.

    :return: Status of the request. 200.
    :rtype: tuple[dict, int, dict]
    """
    session.pop('username', None)
    return ok_response('Logged out')


@APP.route('/', methods=['GET'])
def login_page():
    """
    Serve the vue index.

    :return: The vue index page
    :rtype: str
    """
    return send_from_directory('../public', 'index.html')


@APP.route('/<path:path>', methods=['GET'])
def catch_route(path):
    """
    Serve all other files.

    :return: The vue index page
    :rtype: str
    """
    return send_from_directory('../public', path)


def main():
    """Main"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=80)
    args = parser.parse_args()

    APP.run(debug=True, host='0.0.0.0', port=args.port, use_reloader=False)

if __name__ == '__main__':
    main()
