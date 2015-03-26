from relier.api import AuthenticatedResource
from flask import abort, request, g, make_response
from relier.models import Invitation, User

class InvitationResource(AuthenticatedResource):

    def post(self):

        if not g.user.is_admin:
            abort(403)

        try:
            email = request.json['email_address']
        except KeyError:
            abort(400)

        if User.exists(email):
            abort(409)

        try:
            invitation = Invitation.send(g.user.organization, email)
        except:
            abort(500)

        response = make_response('', 201)
        response.headers['Location'] = '/invitations/{id_}/'.format(
                                                        id_ = invitation.id)
        return response

    def get(self):

        if not g.user.is_admin:
            abort(403)

        query = Invitation.select().where(
                                Invitation.organization == g.user.organization)

        invitations = [{'email': invitation.email} for invitation in query]

        return invitations

class InvitationInstance(AuthenticatedResource):

    def get(self, invitation_id):

        if not g.user.is_admin:
            abort(403)

        query = Invitation.select().where(Invitation.id == invitation_id)

        if query.count() == 0:
            abort(404)

        invitation = Invitation.get(Invitation.id == invitation_id)

        return {'email': invitation.email}

    def delete(self, invitation_id):

        if not g.user.is_admin:
            abort(403)

        query = Invitation.select().where(Invitation.id == invitation_id)

        if query.count() == 0:
            abort(404)

        try:
            invitation = Invitation.get(Invitation.id == invitation_id)
            invitation.delete_instance()
        except:
            abort(500)

        return '', 204
