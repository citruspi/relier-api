from relier.web.views import AuthenticatedView
from relier.models import Invitation
from flask import g, render_template, abort, request

class Invitations(AuthenticatedView):

    def get(self):

        if not g.user.is_admin:
            abort(403)

        invitations = Invitation.select().where(Invitation.organization == g.user.organization)

        invitations.order_by(Invitation.email.desc())
        return render_template('invitations.j2', invitations=invitations)

    def post(self):

        if not g.user.is_admin:
            abort(403)

        email = request.form.get('email_address')

        if not email:
            abort(400)

        if Invitation.select().where(Invitation.email == email).count() != 0:
            abort(409)

        Invitation.send(organization = g.user.organization, email = email)

        invitations = Invitation.select().where(Invitation.organization == g.user.organization)

        invitations.order_by(Invitation.email.desc())
        return render_template('invitations.j2', invitations=invitations)
