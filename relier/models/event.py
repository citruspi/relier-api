from peewee import *
from . import database

class Event(Model):

    organizationid = ForeignKeyField(Organization, related_names='organizations')
    start_time = DateTimeField(null=False)
    title = CharField(null=False)
    description = CharField()
    video_source = CharField(choices='youtube')
    video_id = CharField()
    #TODO Should anonymous be defaulted to true? 
    _is_anonymous = BooleanField(default=true)

    class Meta:

        database = database
