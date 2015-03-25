from peewee import *
from . import database
from organization import Organization

class User(Model):

    organization = ForeignKeyField(Organization, related_name='users')
    firstname = CharField(null=True)
    lastname = CharField(null=True)
    email = CharField(null=False, unique=True)
    password = CharField(null=True)
    is_admin = BooleanField(default=False)
    can_ask = BooleanField(default=True)
    can_answer = BooleanField(default=False)
    city = CharField(null=True)
    region = CharField(null=True)
    country = CharField(null=True)
    html_email = BooleanField(default=True)
    registration_token = CharField()

    class Meta:

        database = database
