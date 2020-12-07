from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_PFP = 'https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png'


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=DEFAULT_PFP)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def __repr__(self):
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @property
    def __repr__(self):
        p = self
        return f"<Post {p.id} {p.title} {p.body} {p.created_at}>"

    def format_date(self):
        return self.created_at.strftime('%B %-d, %Y' + ' at ' + '%I:%M %p')
