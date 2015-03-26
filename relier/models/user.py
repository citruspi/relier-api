from peewee import *
from . import database
from organization import Organization
from invitation import Invitation
import bcrypt
import string
import random
import redis

def generate_token():

    token = ''
    length = 10
    pool = string.ascii_lowercase + string.digits

    for _ in range(60):
        token += random.SystemRandom().choice(pool)

    return token

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

    @staticmethod
    def login(email, password):

        email = email.encode('utf-8')
        password = password.encode('utf-8')

        if not User.exists(email):
            return False

        user = User.get(User.email == email)
        hashed = user.password.encode('utf-8')

        if bcrypt.hashpw(password, hashed) != hashed:
            return None

        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        token = generate_token()

        while r.get('auth_token_'+token) is not None:
            token = generate_token()

        r.set('auth_token_'+token, user.id)

        return token

    @staticmethod
    def authenticate(token):

        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        id_ = r.get('auth_token_'+token)

        if id_ is None:
            return None

        user = User.get(User.id == id_)
        return user

    class Meta:

        database = database
