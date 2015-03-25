from peewee import *
from . import database

class Question(Model):
    
    user_id = 





organization = ForeignKeyField(Organization, related_name='users')
    firstname = CharField()
    lastname = CharField()
    email = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)
    can_ask = BooleanField(default=True)
    can_answer = BooleanField(default=False)
    city = CharField()
    region = CharField()
    country = CharField()







    class Meta:

        database = database
