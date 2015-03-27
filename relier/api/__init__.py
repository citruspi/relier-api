from flask import Flask
from flask.ext import restful
from cors import crossdomain
from organization import OrganizationResource
from authentication import TokenResource, AuthenticatedResource
from user import UserResource, UserInstance
from event import EventResource, EventInstance, EventEndInstance
from question import QuestionResource, QuestionInstance, AnswerResource
from invitation import InvitationResource, InvitationInstance

app = Flask(__name__)
api = restful.Api(app)

<<<<<<< HEAD
api.add_resource(OrganizationResource, '/organizations')
api.add_resource(TokenResource, '/tokens')
api.add_resource(UserResource, '/users')
api.add_resource(UserInstance, '/users/<int:user_id>')
api.add_resource(InvitationResource, '/invitations')
api.add_resource(InvitationInstance, '/invitations/<int:invitation_id>')
api.add_resource(EventResource, '/events')
api.add_resource(EventInstance, '/events/<int:event_id>')
api.add_resource(EventEndInstance, '/events/<int:event_id>/end')
api.add_resource(QuestionResource, '/events/<int:event_id>/questions')  
api.add_resource(QuestionInstance, '/events/<int:event_id>/questions/<int:question_id>') 
api.add_resource(AnswerResource, '/events/<int:event_id>/questions/<int:question_id>/answers') 
=======
api.decorators=[crossdomain(origin='*')]

api.add_resource(OrganizationResource, '/organizations/')
api.add_resource(TokenResource, '/tokens/')
api.add_resource(UserResource, '/users/')
api.add_resource(UserInstance, '/users/<int:user_id>/')
api.add_resource(InvitationResource, '/invitations/')
api.add_resource(InvitationInstance, '/invitations/<int:invitation_id>/')
api.add_resource(EventResource, '/events/')
api.add_resource(EventInstance, '/events/<int:event_id>/')
api.add_resource(EventEndInstance, '/events/<int:event_id>/end/')
api.add_resource(QuestionResource, '/events/<int:event_id>/questions/')
api.add_resource(QuestionInstance, '/events/<int:event_id>/questions/<int:question_id>/') 
api.add_resource(AnswerResource, '/events/<int:event_id>/questions/<int:question_id>/answers/') 
>>>>>>> e98a0d7ea59a818cf13664bf64a345c4b0d87d13
