from peewee import ForeignKeyField, DateTimeField, CharField, Model, BooleanField
from . import database
from organization import Organization

class Event(Model):

    organization = ForeignKeyField(Organization, related_name='events')
    start_time = DateTimeField()
    title = CharField()
    description = CharField()
    video_source = CharField(choices="youtube", default="youtube")
    video_id = CharField()
    is_anonymous = BooleanField(default=True)
    end_time = DateTimeField(null=True)
    

    class Meta:

        database = database
