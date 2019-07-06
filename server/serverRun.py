from functools import wraps
import hashlib
import logging
import os

from flask import Flask, session, redirect, url_for, request, render_template, send_from_directory

from db import db
from models import User, Item, Picture


def create_app():
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


def setup_database(_app):
    with _app.app_context():
        _app.logger.info('Creating databases')
        # db.drop_all() #TODO
        db.create_all()
        db.session.commit()
        _app.logger.info('Created databases')

        example_user = User.query.filter_by(username='bugmommy').first()
        if example_user is None:
            _app.logger.info('Creating test user')
            example_user = User(username='bugmommy',
                                name='Tracy',
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
            db.session.commit()

        example_picture = Picture.query.filter_by(item_id=example_item.id).first()
        if example_picture is None:
            _app.logger.info('Creating test picture')
            example_picture = Picture(item_id=example_item.id, path='http://reddit.com')
            db.session.add(example_picture)
            db.session.commit()

        _app.logger.info('Created test user, item, picture')


def hash_password(password):
    return hashlib.md5(password).hexdigest()


app = create_app()
setup_database(app)


def render_page(template_name, **kwargs):
    return render_template('pages/' + template_name, **kwargs)


def is_logged_in():
    return ('username' in session and
            User.query.filter_by(username=session['username']).first() is not None)


def logged_in(f):
    @wraps(f)
    def _logged_in(*args, **kwargs):
        # just do here everything what you need

        if not is_logged_in():
            return redirect(url_for('not_logged_in'))

        result = f(*args, **kwargs)

        return result
    return _logged_in


def logged_out(redirect_to='protected_page'):
    def _logged_out(f):
        @wraps(f)
        def __logged_out(*args, **kwargs):
            # just do here everything what you need

            if is_logged_in():
                return redirect(url_for(redirect_to))

            result = f(*args, **kwargs)

            return result
        return __logged_out
    return _logged_out


@app.route('/protected')
@logged_in
def protected_page():
    return 'This is a protected page. Congrats you logged in' + \
        '''<form action='/logout' method='post'> <button type='submit'>Log out</button> </form>'''


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password_hash = hash_password(request.form['password'].encode('utf-8'))

    user = User.query.filter_by(username=username, password_hash=password_hash).first()

    if user is None:
        return render_page('redirect_with_timeout.html',
                           title='Inventory',
                           text='Login details incorrect',
                           timeout=2000,
                           redirect_url=url_for('login_page'))
    else:
        session['username'] = username
        return redirect( url_for( 'main_page' ) )


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    username = request.form['username']
    if ' ' in username:
        app.logger.error('Failed to create user {username}: bad username'.format(username=username, e=e))
        return render_page('redirect_with_timeout.html',
                           title='Inventory',
                           text='Invalid username',
                           timeout=2000,
                           redirect_url=url_for('signup_page'))
    email = request.form['email']
    password_hash = hash_password(request.form['password'].encode('utf-8'))

    app.logger.info('Creating user {username}'.format(username=username))
    try:
        user = User(name=name, username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return render_page('redirect_with_timeout.html',
                           title='Inventory',
                           text='Added user {username}'.format(username=username),
                           timeout=2000,
                           redirect_url=url_for('login_page'))
    except Exception as e:
        app.logger.error('Failed to create user {username}: {e}'.format(username=username, e=e))
        return render_page('redirect_with_timeout.html',
                           title='Inventory',
                           text='Failed to add user. Try again later',
                           timeout=2000,
                           redirect_url=url_for('signup_page'))


@app.route('/all_users', methods=['GET'])
def all_users():
    users = User.query.all()
    for user in users:
        user.numItems = len(Item.query.filter_by(user_id=user.id).all())
    return render_page('user.html', users=users)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))


@app.route('/error', methods=['GET'])
@logged_out()
def not_logged_in():
    return 'Not logged in!'


@app.route('/signup.html', methods=['GET'])
@logged_out()
def signup_page():
    return render_page('signup.html')


@app.route('/login.html', methods=['GET'])
@logged_out()
def login_page():
    return render_page('login.html')


@app.route('/main.html', methods=['GET'])
@logged_in
def main_page():
    monthly_items = db.session.query(Item.name, Item.purchase_price, Item.sell_price).all() or []
    monthly_items = [
            {
                'name': item.name,
                'purchase_price': "${p:.2f}".format(p=item.purchase_price),
                'sell_price': "${p:.2f}".format(p=item.sell_price)
            }
            for item in monthly_items
    ]

    return render_page('main.html',
            titleval='Overview',
            sales=monthly_items
            )


@app.route('/', methods=['GET'])
def no_path_handler():
    if is_logged_in():
        return redirect(url_for('main_page'))
    else:
        return redirect(url_for('login_page'))


@app.route('/<path:path>', methods=['GET'])
def catch_route(path):
    if path.split('.')[-1] == 'html':
        return render_page(path)
    else:
        return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
