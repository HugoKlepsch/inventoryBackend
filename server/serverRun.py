from functools import wraps
import hashlib
from os import environ

from flask import Flask, session, redirect, url_for, request

from db import DB

app = Flask(__name__, template_folder="templates")
app.secret_key = environ['APP_SECRET_KEY']

db = DB()

def only_logged_in(f):
    @wraps(f)
    def _only_logged_in(*args, **kwargs):
        # just do here everything what you need

        if not 'username' in session:
            return redirect(url_for("catch_route"));

        result = f(*args, **kwargs)

        return result
    return _only_logged_in

def only_logged_out(f, redirect_to):
    @wraps(f)
    def _only_logged_out(*args, **kwargs):
        # just do here everything what you need

        if 'username' in session:
            return redirect(url_for(redirect_to))

        result = f(*args, **kwargs)

        return result
    return _only_logged_out

@app.route('/protected')
@only_logged_in
def protected_page():
    return "This is a protected page. Congrats you logged in" + \
        """<form action="/logout" method="post"> <button type="submit">Log out</button> </form>"""

@app.route('/login', methods=['POST'])
def login():
    name = request.form['username'].encode('utf-8')
    passwordHash = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()

    cursor = db.execute("SELECT A_USERNAME from ACCOUNT_INFO where A_USERNAME=%s AND A_PASSWORD=%s",
                   (name, passwordHash,))
    if (not cursor.fetchone()):
        return "Login details incorrect"
    else:
        session['username'] = name
        return redirect(url_for('user_account'))

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['username'].encode('utf-8')
    passwordHash = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
    email = request.form['email'].encode('utf-8')

    cursor = db.execute("SELECT A_USERNAME, A_EMAIL from ACCOUNT_INFO where A_USERNAME=%s OR A_EMAIL=%s",
                   (name, email))
    if (cursor.fetchone()):
        return "Username or email already taken"

    cursor.execute("""INSERT into ACCOUNT_INFO (A_USERNAME, A_PASSWORD, A_EMAIL) VALUES (%s, %s, %s)""",
                   (name, passwordHash, email,))

    db.commit()

    return redirect(url_for('catch_route'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('catch_route'))

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
