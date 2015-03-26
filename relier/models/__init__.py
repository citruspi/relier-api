from peewee import PostgresqlDatabase

database = PostgresqlDatabase('relier')

from organization import Organization
from user import User
from invitation import Invitation
from event import Event
from question import Question
from answer import Answer
from json_help import JsonHelper

database.create_tables([Organization, User, Invitation, Event, Question, Answer], True)
