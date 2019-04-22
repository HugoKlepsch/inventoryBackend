from functools import wraps
import hashlib
import logging
import os

from flask import Flask, session, redirect, url_for, request

from db import db
from models import User, Item, Picture


def create_app():
    _app = Flask(__name__, template_folder="templates")
    _app.secret_key = 'yeetyeetskeetskeet'
    _app.logger.setLevel(logging.DEBUG)

    db_host = os.environ.get('DBHOST', '127.0.0.1')
    db_port = int(os.environ.get('DBPORT', 3301))
    db_password = os.environ.get('DBPASS', 'notwaterloo')
    db_database = 'inventorydb'
    db_string = "mysql://root:{password}@{host}:{port}/{database}".format(
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
        _app.logger.info("Creating databases")
        db.drop_all()
        db.create_all()
        db.session.commit()
        _app.logger.info("Created databases")

        example_user = User.query.filter_by(username='bugmommy').first()
        if example_user is None:
            _app.logger.info("Creating test user")
            example_user = User(username='bugmommy',
                                name='Tracy',
                                email='test@email.com',
                                password_hash='asdf')
            db.session.add(example_user)
            db.session.commit()

        example_item = Item.query.filter_by(user_id=example_user.id).first()
        if example_item is None:
            _app.logger.info("Creating test item")
            example_item = Item(user_id=example_user.id)
            db.session.add(example_item)
            db.session.commit()

        example_picture = Picture.query.filter_by(item_id=example_item.id).first()
        if example_picture is None:
            _app.logger.info("Creating test picture")
            example_picture = Picture(item_id=example_item.id)
            db.session.add(example_picture)
            db.session.commit()

        _app.logger.info("Created test user, item, picture")


app = create_app()
setup_database(app)


def logged_in(f):
    @wraps(f)
    def _logged_in(*args, **kwargs):
        # just do here everything what you need

        if 'username' not in session:
            return redirect(url_for("catch_route"))

        username = session['username']
        if User.query.filter_by(username=username).first() is None:
            return redirect(url_for("catch_route"))

        result = f(*args, **kwargs)

        return result
    return _logged_in


def logged_out(redirect_to='protected_page'):
    def _logged_out(f):
        @wraps(f)
        def __logged_out(*args, **kwargs):
            # just do here everything what you need

            if 'username' in session:
                return redirect(url_for(redirect_to))

            result = f(*args, **kwargs)

            return result
        return __logged_out
    return _logged_out


@app.route('/protected')
@logged_in
def protected_page():
    return "This is a protected page. Congrats you logged in" + \
        """<form action="/logout" method="post"> <button type="submit">Log out</button> </form>"""


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].encode('utf-8')
    password_hash = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()

    user = User.query.filter_by(username=username, password_hash=password_hash)

    if user is None:
        return "Login details incorrect"
    else:
        session['username'] = username
        return 'Logged in'
#    cursor = db.execute("SELECT A_USERNAME from ACCOUNT_INFO where A_USERNAME=%s AND A_PASSWORD=%s",
#                        (name, password_hash,))
#    if not cursor.fetchone():
#        return "Login details incorrect"
#    else:
#        session['username'] = name
#        return redirect(url_for('user_account'))


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['username'].encode('utf-8')
    password_hash = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
    email = request.form['email'].encode('utf-8')

    return "Signup stub"
    #cursor = db.execute("SELECT A_USERNAME, A_EMAIL from ACCOUNT_INFO where A_USERNAME=%s OR A_EMAIL=%s",
    #                    (name, email))
    #if cursor.fetchone():
    #    return "Username or email already taken"

    #cursor.execute("""INSERT into ACCOUNT_INFO (A_USERNAME, A_PASSWORD, A_EMAIL) VALUES (%s, %s, %s)""",
    #               (name, password_hash, email,))

    #db.commit()

    #return redirect(url_for('catch_route'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('catch_route'))


@app.route('/error', methods=['GET'])
@logged_out()
def catch_route():
    return 'Not logged in!'


@app.route('/', methods=['GET'])
@logged_out()
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
