from flask.views import MethodView
from flask import render_template, request, flash, redirect, session, abort
from relier.models import User, Invitation

class InvitationView(MethodView):

    def get(self, token):

        if Invitation.select().where(Invitation.token == token).count() == 0:
            abort(404)

        invitation = Invitation.get(Invitation.token == token)

        return render_template('invitation.j2', invitation=invitation)

    def post(self, token):

        if request.form.get('first_name') is None:
            abort(400)

        if request.form.get('last_name') is None:
            abort(400)

        if request.form.get('password') is None:
            abort(400)

        if Invitation.select().where(Invitation.token == token).count() == 0:
            abort(404)

        invitation = Invitation.get(Invitation.token == token)

        user = User.from_invitation(firstname = request.form['first_name'],
                                lastname = request.form['last_name'],
                                password = request.form['password'].encode('utf-8'),
                                invitation = invitation.id)

        token = User.login(user.email,
                            request.form['password'])

        session['token'] = token
        session.modified = True

        return redirect('/')
