from peewee import *
from . import database
from organization import Organization
from invitation import Invitation
import bcrypt

class User(Model):

    organization = ForeignKeyField(Organization, related_name='users')
    firstname = CharField()
    lastname = CharField()
    email = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)
    can_ask = BooleanField(default=True)
    can_answer = BooleanField(default=False)
    timezone = CharField(default='America/Chicago')
    html_email = BooleanField(default=True)

    @staticmethod
    def from_invitation(firstname, lastname, password, invitation):

        invitation = Invitation.get(Invitation.id == invitation)

        password = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User.create(organization = invitation.organization,
                            firstname = firstname,
                            lastname = lastname,
                            email = invitation.email,
                            password = password)

        invitation.delete_instance()

        return user

    @staticmethod
    def exists(email):

        query = User.select().where(User.email == email)
        return query.count() != 0

    class Meta:

        database = database
