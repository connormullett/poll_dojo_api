
from uuid import uuid4

from marshmallow import fields, Schema
from datetime import datetime
from . import db
from ..app import bcrypt

from .choice import ChoiceSchema


class PollModel(db.Model):

    __tablename__ = 'polls'

    id = db.Column(db.String, primary_key=True, default=str(uuid4()))
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.String(128), nullable=False, unique=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    choices = db.relationship('ChoiceModel', backref='polls', 
                              cascade='all, delete-orphan', lazy=True)
    total_answers = db.Column(db.Integer)
    source = db.Column(db.String(128))

    def __init__(self, data):
        self.owner_id = data.get('owner_id')
        self.question = data.get('question')
        self.source = data.get('source')
        self.created_at = self.modified_at = datetime.utcnow()
        self.total_answers = 0

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def get_all_polls():
        return PollModel.query.all()
    
    @staticmethod
    def get_poll_by_id(value):
        return PollModel.query.get(value)
    
    @staticmethod
    def get_poll_by_question(question):
        return PollModel.query.filter_by(question=question).first()


class PollSchema(Schema):
    id = fields.Str(dump_only=True)
    owner_id = fields.Str(required=True)
    question = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    choices = fields.Nested(ChoiceSchema, many=True)
