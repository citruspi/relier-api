from peewee import ForeignKeyField, DateTimeField, CharField, Model
from . import database
from question import Question


class Answer(Model):

    question = ForeignKeyField(Question, related_name='answers')
    created = DateTimeField()
    updated = DateTimeField(null=True)
    content = CharField()

    def JSON(self):

        return {
                    'id': self.id,
                    'content': self.content,
                    'created': self.created.strftime('%Y-%m-%d %H:%M'),
                    'updated': self.updated.strftime('%Y-%m-%d %H:%M') if self.updated else ''
                }

    class Meta:

        database = database
