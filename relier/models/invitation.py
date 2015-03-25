from peewee import *
from . import database
from organization import Organization

class Invitation(Model):

    organization = ForeignKeyField(Organization, related_name='invitations')
    email = CharField()
    token = CharField()

    class Meta:

        database = database
