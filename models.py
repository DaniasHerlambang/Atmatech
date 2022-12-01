from flask import Flask
from datetime import datetime, timedelta
from sqlalchemy.orm import backref
from flask_sqlalchemy import SQLAlchemy
import os

BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)
app.config['SECRET_KEY']= "ini_secret_key_untuk_JWT"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://postgres:x@localhost:5432/atmatech"
db = SQLAlchemy(app)

class UserProfile(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    publik_id       = db.Column(db.String(150), unique=True)
    username        = db.Column(db.String(50))
    password        = db.Column(db.String(150))
    active          = db.Column(db.Boolean)
    created_at      = db.Column(db.DateTime, default=datetime.now)

    # books = db.relationship('Book', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Book(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(100))
    description     = db.Column(db.Text)
    content     = db.Column(db.String(100))
    created_at    = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    created_by_id = db.relationship("UserProfile", backref=backref("user_profile" , uselist=False))
    # created_by_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    deleted = db.Column(db.DateTime, nullable=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, title, description , content , created_by_id):
        self.title = title
        self.description = description
        self.content = content
        self.created_by_id = created_by_id

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            # 'created_by_id': self.created_by_id.username,
        }

    def __repr__(self):
        return '<id {}>'.format(self.id)

with app.app_context():
    db.create_all()