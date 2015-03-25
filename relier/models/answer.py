from peewee import *
from . import database

from user import User
from question import Question

class Answer(Model):

    user = ForeignKeyField(User, related_name='answers')
    question = ForeignKeyField(Question, related_name='answers')
    created = DateTimeField()
    updated = DateTimeField()
    content = CharField()
    
    class Meta:

        database = database
