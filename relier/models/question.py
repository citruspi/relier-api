from peewee import *
from . import database
from event import Event

class Question(Model):

    event = ForeignKeyField(Event, related_name='questions')
    created = DateTimeField()
    updated = DateTimeField(null=True)
    content = CharField()

    class Meta:

        database = database
