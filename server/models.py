from datetime import datetime

from server.serverRun import db, app


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__ + 'id'), nullable=False)


class Picture(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    item_id = db.Column(db.Integer, db.ForeignKey(Item.__tablename__ + 'id'), nullable=False)


def create_tables():
    db.create_all()
    db.session.commit()
    app.logger.debug("Created databases")