from peewee import *
from . import database
from question import Question

class Answer(Model):

    question = ForeignKeyField(Question, related_name='answers')
    created = DateTimeField()
    updated = DateTimeField(null=True)
    content = CharField()

    class Meta:

        database = database
