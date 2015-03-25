from peewee import *
from . import database

class Organization(Model):

    name = CharField()

    @staticmethod
    def exists(name):

        query = Organization.select().where(Organization.name == name)
        return query.count() != 0

    class Meta:

        database = database
