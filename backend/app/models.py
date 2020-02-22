from app import db
from datetime import datetime

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        type = db.Column(db.Integer, index=True,)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))

        def __repr__(self):
            return '<User {}>'.format(self.username)


class Listing(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        body = db.Column(db.String, index=True)
        timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def __repr__(self):
            return '<Post {}>'.format(self.body)
