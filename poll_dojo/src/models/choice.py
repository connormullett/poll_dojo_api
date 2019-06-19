
from uuid import uuid4

from marshmallow import fields, Schema
from datetime import datetime
from . import db
from ..app import bcrypt


class ChoiceModel(db.Model):

    __tablename__ = 'choices'

    id = db.Column(db.String, primary_key=True, default=str(uuid4()))
    text = db.Column(db.String(128), nullable=False)
    answers = db.Column(db.Integer)
