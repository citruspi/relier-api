from peewee import PostgresqlDatabase

database = PostgresqlDatabase('relier')

from organization import Organization
from user import User


