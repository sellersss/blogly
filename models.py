from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_PFP = 'https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png'


def connect_db(app):
    db.app = app
    db.init_app
    db.create_all()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String, nullable=False, default=DEFAULT_PFP)
