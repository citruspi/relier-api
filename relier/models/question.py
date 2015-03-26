from peewee import ForeignKeyField, DateTimeField, CharField, Model
from event import Event
from . import database


class Question(Model):

    event = ForeignKeyField(Event, related_name='questions')
    created = DateTimeField()
    updated = DateTimeField(null=True)
    content = CharField()

    class Meta:
        database = database
