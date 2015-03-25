from peewee import *
from . import database
from user import User
from event import Event

class Question(Model):
    
    user = ForeignKeyField(User, related_name='questions')
    event = ForeignKeyField(Event, related_name='questions')
    created = DateTimeField()
    updated = DateTimeField()
    content = CharField()

    class Meta:

        database = database
