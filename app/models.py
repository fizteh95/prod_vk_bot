from datetime import datetime
from app import db
# import json


class VkPublic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200))
    bot_token = db.Column(db.String(200))
    tg_channel = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Address {self.address}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    internal_id = db.Column(db.Integer)
    data_json = db.Column(db.String(10000))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Id {self.internal_id}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    send = db.Column(db.Integer, default=0)
    post_id = db.Column(db.Integer)
    bot_token = db.Column(db.String(200))
    tg_channel = db.Column(db.String(200))

    def __repr__(self):
        return f'<Id {self.post_id}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    publics = db.relationship('VkPublic', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<Chat {self.chat_id}>'
