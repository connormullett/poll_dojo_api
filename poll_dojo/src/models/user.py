

from uuid import uuid4

from marshmallow import fields, Schema
from datetime import datetime
from . import db
from ..app import bcrypt

from .poll import PollSchema


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    polls = db.relationship('PollModel', backref='users', 
                            cascade='all, delete-orphan', lazy=True)

    def __init__(self, data):
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self._generate_hash(data.get('password'))
        self.created_at = self.modified_at = datetime.utcnow()

    def _check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def _generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self._generate_hash(value)
            setattr(self, key, item)
        self.modified_at = datetime.utcnow()
        db.session.commit()
        
    @staticmethod
    def get_all_users():
        return UserModel.query.all()
    
    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    @staticmethod
    def get_user_by_id(value):
        return UserModel.query.get(value)

    @staticmethod
    def get_user_by_name(name):
        return UserModel.query.filter_by(name=name).first()


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    polls = fields.Nested(PollSchema, many=True)
