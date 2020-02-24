from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        type = db.Column(db.String(), index=True,)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))

        def __repr__(self):
            return '<User {}>'.format(self.username)

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)


class Listing(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(64), index=True)
        desc = db.Column(db.String, index=True)
        body = db.Column(db.String, index=True)
        timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        location = db.Column(db.String, index=True)
        type = db.Column(db.String, index=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def __repr__(self):
            return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
