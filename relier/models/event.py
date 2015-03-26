from peewee import *
from . import database
from organization import Organization
from datetime import datetime 

class Event(Model):

    organization = ForeignKeyField(Organization, related_name='events')
    start_time = DateTimeField()
    title = CharField()
    description = CharField()
    video_source = CharField(choices="youtube", default="youtube")
    video_id = CharField()
    is_anonymous = BooleanField(default=True)
    end_time = DateTimeField(null=True)
    

    def JSON(self):

        return {
                    'id': self.id,
                    'start_time_text': self.start_time.strftime('%Y-%m-%d %H:%M'),
                    'title': self.title,
                    'description': self.description,
                    'video_source' : self.video_source,
                    'video_id' : self.video_id
               }
    class Meta:

        database = database
