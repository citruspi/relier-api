from peewee import PostgresqlDatabase

database = PostgresqlDatabase('relier')

from organization import Organization
from user import User
from invitation import Invitation
from event import Event

database.create_tables([Organization, User, Invitation, Event], True)
