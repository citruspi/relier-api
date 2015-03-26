from flask import Flask
from flask.ext import restful
from organization import OrganizationResource
from authentication import TokenResource, AuthenticatedResource
from user import UserInstance
from invitation import InvitationResource

app = Flask(__name__)
api = restful.Api(app)

api.add_resource(OrganizationResource, '/organizations/')
api.add_resource(TokenResource, '/tokens/')
api.add_resource(InvitationResource, '/invitations/')
api.add_resource(InvitationInstance, '/invitations/<int:invitation_id>/')
