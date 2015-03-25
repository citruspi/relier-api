from peewee import PostgresqlDatabase

database = PostgresqlDatabase('relier')

from organization import Organization
from user import User
from invitation import Invitation

database.create_tables([Organization, User, Invitation], True)
