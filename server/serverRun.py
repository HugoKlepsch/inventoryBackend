import argparse
from functools import wraps
import hashlib
import json
import logging
import os
import re

from flask import Flask, session, redirect, url_for, request, send_from_directory
from flask_apispec import marshal_with
from marshmallow import fields
from webargs.flaskparser import use_args

from db import db
from models import User, Item, Picture, Location
from models import UserSchema, ItemSchema
from schema import JSON_CT, INTERNAL_SERVER_ERROR_JSON_RESPONSE, BAD_REQUEST_JSON_RESPONSE, ok_response
from schema import JsonApiSchema


def create_app():  # {{{
    _app = Flask(__name__, template_folder='templates')
    _app.secret_key = 'yeetyeetskeetskeet'
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

    db.init_app(_app)

    return _app
# }}}


def setup_database(_app):  # {{{
    with _app.app_context():
        _app.logger.info('Creating databases')
        db.drop_all()  # TODO
        db.create_all()
        db.session.commit()
        _app.logger.info('Created databases')

        example_user = User.query.filter_by(username='bugmommy').first()
        if example_user is None:
            _app.logger.info('Creating test user')
            example_user = User(username='bugmommy',
                                email='test@email.com',
                                password_hash=hash_password('asdf'.encode('utf-8')))
            db.session.add(example_user)
            db.session.commit()

        example_item = Item.query.filter_by(user_id=example_user.id).first()
        if example_item is None:
            _app.logger.info('Creating test item')
            example_item = Item(user_id=example_user.id, name='Test', purchase_price=123,
                                sell_price=2345)
            db.session.add(example_item)
            example_item_two = Item(user_id=example_user.id, name='Test2', purchase_price=23,
                                    sell_price=5678)
            db.session.add(example_item_two)
            example_item_three = Item(user_id=example_user.id, name='Test3', purchase_price=1235,
                                      sell_price=778)
            db.session.add(example_item_three)
            db.session.commit()

        example_picture = Picture.query.filter_by(item_id=example_item.id).first()
        if example_picture is None:
            _app.logger.info('Creating test picture')
            example_picture = Picture(item_id=example_item.id, path='http://reddit.com')
            db.session.add(example_picture)
            db.session.commit()

        example_location = Location.query.filter_by(name='Freelton Market').first()
        if example_location is None:
            _app.logger.info('Creating test location')
            example_location = Location(name='Freelton Market', user_id=example_user.id)
            db.session.add(example_location)
            db.session.commit()

        _app.logger.info('Created test user, item, picture and location')
# }}}


def hash_password(password):
    return hashlib.md5(password).hexdigest()


app = create_app()
setup_database(app)


def is_logged_in(as_user=None):
    if 'username' in session:
        username = session['username']
        return (User.query.filter_by(username=username).first() is not None) and \
               (as_user is None or username == as_user)


def logged_in(as_user=None):
    def _logged_in(f):
        @wraps(f)
        def __logged_in(*args, **kwargs):
            # just do here everything what you need

            if not is_logged_in(as_user=as_user):
                return redirect(url_for('not_logged_in'))

            result = f(*args, **kwargs)

            return result
        return __logged_in
    return _logged_in


def logged_out(redirect_to):
    def _logged_out(f):
        @wraps(f)
        def __logged_out(*args, **kwargs):
            # just do here everything what you need

            if is_logged_in():
                if redirect_to is not None:
                    return redirect(url_for(redirect_to))
                else:
                    return json.dumps({
                        'msg': 'Should not be logged in'
                    }), 400, JSON_CT

            result = f(*args, **kwargs)

            return result
        return __logged_out
    return _logged_out


@app.route('/login', methods=['POST'])
@use_args({
    'username': fields.Str(required=True),
    'password': fields.Str(required=True)
})
@marshal_with(JsonApiSchema())
def login(data):
    username = data['username']
    password_hash = hash_password(data['password'].encode('utf-8'))

    user = User.query.filter_by(username=username, password_hash=password_hash).first()

    if user is None:
        return BAD_REQUEST_JSON_RESPONSE
    else:
        session['username'] = username
        session['user_id'] = user.id
        return ok_response('Logged in')


@app.route('/signup', methods=['POST'])
@use_args({
    'username': fields.Str(required=True),
    'email': fields.Str(required=True),
    'password': fields.Str(required=True)
})
@marshal_with(JsonApiSchema())
def signup(data):

    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)

    if username is not None and \
            email is not None and \
            password is not None:
        password_hash = hash_password(password.encode('utf-8'))

        if re.match(r'[a-zA-Z0-9_\-]{4,30}', username) is not None:
            app.logger.info('Creating user {username}'.format(username=username))
            try:
                user = User(username=username, email=email, password_hash=password_hash)
                db.session.add(user)
                db.session.commit()
                return ok_response('User created')
            except Exception:
                return INTERNAL_SERVER_ERROR_JSON_RESPONSE

    return BAD_REQUEST_JSON_RESPONSE


@app.route('/all_users', methods=['GET'])
@logged_in(as_user='bugmommy')  # TODO create admin account
@marshal_with(UserSchema(many=True, exclude=['password_hash', 'items']))
def all_users():
    return User.query.all()


@app.route('/items', methods=['GET'])
@logged_in()
@marshal_with(ItemSchema(many=True))
def items():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    user_items = Item.query.filter_by(user_id=user.id).all() or []
    return user_items


@app.route('/item/<int:item_id>',methods=['DELETE'])
@logged_in()
@marshal_with(JsonApiSchema())
def delete_item(item_id):
    user_id = session['user_id']
    try:
        row = Item.query.filter_by(id=item_id, user_id=user_id).one()
        db.session.delete(row)
        db.session.commit()
        return ok_response('Ok, this has been deleted')

    except Exception as e:
        app.logger.error('Failed to delete item {name}: {e}'.format(name=item_id, e=e))
        return BAD_REQUEST_JSON_RESPONSE


@app.route('/item/<int:_id>', methods=['GET'])
@logged_in()
@marshal_with(ItemSchema())
def get_item(_id):
    # grab item from the list by id.
    item = Item.query.get(_id)

    if item is not None:
        return item
    else:
        return BAD_REQUEST_JSON_RESPONSE


# TODO add validation to this route
@app.route('/item', methods=['POST'])
@logged_in()
def create_item():
    user_id = session['user_id']
    purchase_date = request.form['purchaseDate']
    purchase_date = purchase_date if purchase_date != '' else None
    purchase_price = request.form['purchasePrice']
    purchase_price = purchase_price if purchase_price != '' else None
    sell_date = request.form['sellDate']
    sell_date = sell_date if sell_date != '' else None
    sell_price = request.form['sellPrice']
    sell_price = sell_price if sell_price != '' else None
    description = request.form['description']
    name = request.form['name']
    if ' ' in name:
        app.logger.error('Failed to create item {name}: bad name'.format(name=name, e=e))
        return render_page('redirect_with_timeout.html',
                           title='Inventory',
                           text='Invalid name',
                           timeout=2000,
                           redirect_url=url_for('main_page'))
    app.logger.info('Creating item {name}'.format(name=name))
    try:
        item = Item(user_id=user_id, purchase_date=purchase_date, purchase_price=purchase_price, sell_date=sell_date, sell_price=sell_price, description=description, name=name)#this works but is sending the wrong datetime information
        db.session.add(item)
        db.session.commit()
        return render_page('redirect_with_timeout.html',
                           title='Inventory',
                           text='Added item {name}'.format(name=name),
                           timeout=2000,
                           redirect_url=url_for('main_page'))#change to item/<id> view instead of items
    except Exception as e:
        app.logger.error('Failed to create item {name}: {e}'.format(name=name, e=e))
        return render_page('redirect_with_timeout.html',
                           title='Inventory',
                           text='Failed to add item. Try again later',
                           timeout=2000,
                           redirect_url=url_for('main_page'))


@app.route('/logout', methods=['GET', 'POST'])
@marshal_with(JsonApiSchema())
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return ok_response('Logged out')


@app.route('/error', methods=['GET'])
@logged_out(redirect_to=None)
@marshal_with(JsonApiSchema())
def not_logged_in():
    return {
        'msg': 'Not logged in'
    }, 401, JSON_CT


# @app.route('/main.html', methods=['GET'])
# @logged_in
# def main_page():
#     monthly_items = db.session.query(Item.name, Item.purchase_price, Item.sell_price).all() or []
#     monthly_items = [
#             {
#                 'name': item.name,
#                 'purchase_price': "${p:.2f}".format(p=item.purchase_price) \
#                         if item.purchase_price is not None else "$--",
#                 'sell_price': "${p:.2f}".format(p=item.sell_price) \
#                         if item.sell_price is not None else "$--"
#             }
#             for item in monthly_items
#     ]

#     return render_page('main.html',
#             titleval='Overview',
#             sales=monthly_items
#             )


@app.route('/', methods=['GET'])
def login_page():
    # Use this to serve the Vue rather than the Flask
    return send_from_directory('public', 'index.html')


@app.route('/<path:path>', methods=['GET'])
def catch_route(path):
    return send_from_directory('public', path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=80)
    args = parser.parse_args()

    app.run(debug=True, host='0.0.0.0', port=args.port)
