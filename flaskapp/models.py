import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime
from flaskapp import db, login


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(60), nullable=True, unique=True)
    username = db.Column(db.String(60), nullable=True, unique=True)
    password = db.Column(db.String(255))

    def get_reset_token(self, expires_sec=18000):
        s = Serializer(os.environ.get('SECRET_KEY'), expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.environ.get('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "<User {} {}>".format(self.email, self.username)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    pub_date = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)

    def __init__(self, title, author, body):
        self.title = title
        self.author = author
        self.body = body


