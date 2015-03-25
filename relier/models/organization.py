from peewee import *
from . import database

class Organization(Model):

    name = CharField()

    class Meta:

        database = database
