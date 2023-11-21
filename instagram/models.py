# Vai as classes / estrura do banco de dados
from instagram import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.relationship("Posts", backref='user', lazy=True)


class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    post_text = database.Column(database.String, default='')
    post_img = database.Column(database.String, default='default.png')
    creation_date = database.Column(database.String, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    likes = database.relationship('Like', backref='posts', lazy=True)

class Like(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), nullable=False)

class Comment(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    text = database.Column(database.String(255), nullable=False)
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), nullable=False)
    post = database.relationship('Posts', backref=database.backref('comments', lazy=True))
