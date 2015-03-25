from peewee import *
from . import database
from organization import Organization
from invitation import Invitation
import requests
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
    def from_invitation(firstname, lastname, password, address, invitation):

        invitation = Invitation.get(Invitation.id == invitation)

        geoip_endpoint = 'https://freegeoip.net/json/{address}'
        geoip_endpoint = geoip_endpoint.format(address = address)

        timezone = None

        r = requests.get(geoip_endpoint)

        if r.status_code == 200:

            try:
                timezone = r.json()['time_zone']
            except KeyError:
                pass

        if timezone is None:
            timezone = 'America/Chicago'

        password = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User.create(organization = invitation.organization,
                            firstname = firstname,
                            lastname = lastname,
                            email = invitation.email,
                            password = password,
                            timezone = timezone)

        invitation.delete_instance()

        return user

    class Meta:

        database = database
