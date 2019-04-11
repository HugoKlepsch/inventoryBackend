from functools import wraps
import hashlib
import os

from flask import Flask, session, redirect, url_for, request

from server.db import DB

app = Flask(__name__, template_folder="templates")
app.secret_key = 'yeetyeetskeetskeet'
db_host = os.environ.get('DBHOST', 'localhost')
db_port = int(os.environ.get('DBPORT', 3301))

db = DB(host=db_host, port=db_port)
db._connect()


def only_logged_in(f):
    @wraps(f)
    def _only_logged_in(*args, **kwargs):
        # just do here everything what you need

        if 'username' not in session:
            return redirect(url_for("catch_route"))

        result = f(*args, **kwargs)

        return result
    return _only_logged_in


def only_logged_out(redirect_to='protected_page'):
    def _only_logged_out(f):
        @wraps(f)
        def __only_logged_out(*args, **kwargs):
            # just do here everything what you need

            if 'username' in session:
                return redirect(url_for(redirect_to))

            result = f(*args, **kwargs)

            return result
        return __only_logged_out
    return _only_logged_out


@app.route('/protected')
@only_logged_in
def protected_page():
    return "This is a protected page. Congrats you logged in" + \
        """<form action="/logout" method="post"> <button type="submit">Log out</button> </form>"""


@app.route('/login', methods=['POST'])
def login():
    name = request.form['username'].encode('utf-8')
    password_hash = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()

    cursor = db.execute("SELECT A_USERNAME from ACCOUNT_INFO where A_USERNAME=%s AND A_PASSWORD=%s",
                        (name, password_hash,))
    if not cursor.fetchone():
        return "Login details incorrect"
    else:
        session['username'] = name
        return redirect(url_for('user_account'))


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['username'].encode('utf-8')
    password_hash = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
    email = request.form['email'].encode('utf-8')

    cursor = db.execute("SELECT A_USERNAME, A_EMAIL from ACCOUNT_INFO where A_USERNAME=%s OR A_EMAIL=%s",
                        (name, email))
    if cursor.fetchone():
        return "Username or email already taken"

    cursor.execute("""INSERT into ACCOUNT_INFO (A_USERNAME, A_PASSWORD, A_EMAIL) VALUES (%s, %s, %s)""",
                   (name, password_hash, email,))

    db.commit()

    return redirect(url_for('catch_route'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('catch_route'))


@app.route('/error', methods=['GET'])
@only_logged_out()
def catch_route():
    return 'Not logged in!'


@app.route('/', methods=['GET'])
@only_logged_out()
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
