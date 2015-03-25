from peewee import *
from . import database
from organization import Organization

class User(Model):

    organization = ForeignKeyField(Organization, related_name='users')
    firstname = CharField()
    lastname = CharField()
    email = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)
    can_ask = BooleanField(default=True)
    can_answer = BooleanField(default=False)
    timezone = CharField()
    html_email = BooleanField(default=True)

    class Meta:

        database = database
