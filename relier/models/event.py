from peewee import *
from . import database
from organization import Organization

class Event(Model):

    organization = ForeignKeyField(Organization, related_name='events')
    start_time = DateTimeField()
    title = CharField()
    description = CharField()
    video_source = CharField(choices="youtube", default="youtube")
    video_id = CharField()
    #TODO Should anonymous be defaulted to true? 
    is_anonymous = BooleanField(default=True)
    end_time = DateTimeField(null=True)

    class Meta:

        database = database
