from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_PFP = 'https://twirpz.files.wordpress.com/2015/06/' + \
    'twitter-avi-gender-balanced-figure.png'


class User(db.Model):
    """Schema for User model.

    Includes id as a primary key, posts has a 1:M relationship with the posts
    table, first_name, last_name, and image_url defaulted to the starter
    Twitter profile picture. The main property full_name() allows for easier
    access of the first_name and last_name, exported as a "merged" string.
    """

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
    """Schema for Post model.

    Includes id as a primary key, user_id as a foreign key, body, and 
    created_at. The main property includes a clean format for the date
    to be easily exported as a string.

    """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @property
    def __repr__(self):
        p = self
        return f"<Post {p.id} {p.title} {p.body} {p.created_at}>"

    def format_date(self):
        return self.created_at.strftime('%B %-d, %Y' + ' at ' + '%I:%M %p')


class Tag(db.Model):
    """Schema for Tag model.

    Includes id as a primary key, posts has a relationship to posts that
    includes the tags, and name.
    """

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='post_tags', backref='tags')

    def __repr__(self):
        t = self
        return f"<Tag id={t.id} {t.name}>"


class PostTag(db.Model):
    """Schema for PostTag model.

    Includes post_id and tag_id as foreign keys in order to coordinate tag
    functionality between the Post and User models.
    """

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)

    def __repr__(self):
        p = self
        return f"<PostTag {p.post_id} {p.tag_id}>"
