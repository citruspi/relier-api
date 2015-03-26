from peewee import *
import string
from . import database
from organization import Organization
import random

def generate_token():

    token = ''
    length = 10
    pool = string.ascii_uppercase + string.digits

    for _ in range(10):
        token += random.SystemRandom().choice(pool)

    return token

class Invitation(Model):

    organization = ForeignKeyField(Organization, related_name='invitations')
    email = CharField()
    token = CharField(unique=True)

    @staticmethod
    def send(organization, email):

        token = generate_token()

        while Invitation.select().where(Invitation.token == token).count() != 0:
            token = generate_token()

        invitation = Invitation.create(organization = organization,
                                        email = email,
                                        token = token)

        return invitation

    @staticmethod
    def exists(token):

        token = token.encode('utf-8')

        query = Organization.select().where(Invitation.token == token)
        return query.count() != 0

    class Meta:

        database = database
