from relier.web.views import AuthenticatedView
from relier.models import Invitation
from flask import render_template, g, abort, redirect, request

class DeleteInvitation(AuthenticatedView):

    def get(self, invitation_id):

        if not g.user.is_admin:
            abort(403)

        if Invitation.select().where(Invitation.id == invitation_id).count() == 0:
            abort(404)

        invitation = Invitation.get(Invitation.id == invitation_id)

        invitation.delete_instance()

        return redirect('/invitations/')
