from peewee import *
from . import database
from organization import Organization

class Event(Model):

    organization = ForeignKeyField(Organization, related_name='events')
    start_time = DateTimeField()
    title = CharField(null=False)
    description = CharField()
    video_source = CharField(choices="youtube")
    video_id = CharField()
    #TODO Should anonymous be defaulted to true? 
    is_anonymous = BooleanField(default=True)

    class Meta:

        database = database
