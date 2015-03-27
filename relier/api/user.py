from flask import abort, request, make_response
from relier.models import User, Invitation
from relier.api import Resource, AuthenticatedResource
from relier.api.authentication import verify
from flask import g
import bcrypt

class UserResource(Resource):

    def post(self):

        try:
            body = request.json
            invitation = body['invitation'].encode('utf-8')
            firstname = body['first_name'].encode('utf-8')
            lastname = body['last_name'].encode('utf-8')
            password = body['password'].encode('utf-8')
        except KeyError:
            abort(400)

        if not Invitation.exists(invitation):
            abort(400)

        invitation = Invitation.get(Invitation.token == invitation)

        try:
            user = User.from_invitation(firstname = firstname,
                                        lastname = lastname,
                                        password = password,
                                        invitation = invitation.id)
        except Exception:
            abort(500)

        response = make_response('', 201)
        response.headers['Location'] = '/users/{id_}/'.format(id_ = user.id)
        return response

    @verify
    def get(self):

        if not g.user.is_admin:
            abort(403)

        query = User.select().where(User.organization == g.user.organization)

        users = [user.JSON() for user in query]

        return users

class UserInstance(AuthenticatedResource):

    def get(self, user_id):

        if not g.user.is_admin and user_id != g.user.id:
            abort(403)

        if User.select().where(User.id == user_id).count() == 0:
            abort(404)

        user = User.get(User.id == user_id)

        return user.JSON()

    def delete(self, user_id):

        if not g.user.is_admin or user_id == g.user.id:
            abort(403)

        if User.select().where(User.id == user_id).count() == 0:
            abort(404)

        user = User.get(User.id == user_id)
        user.delete_instance()

        return {}, 204

    def put(self, user_id):

        if not request.json:
            abort(400)

        admin_only = set(['can_ask', 'can_answer', 'is_admin'])

        if len(admin_only.intersection(request.json.keys())) > 0:
            if not g.user.is_admin:
                abort(403)

        if not g.user.is_admin and user_id != g.user.id:
            abort(403)

        user = User.get(User.id == user_id)

        user.firstname = request.json.get('first_name', user.firstname)
        user.lastname = request.json.get('last_name', user.lastname)
        user.email = request.json.get('email_address', user.email)
        user.is_admin = request.json.get('is_admin', user.is_admin)
        user.can_ask = request.json.get('can_ask', user.can_ask)
        user.can_answer = request.json.get('can_answer', user.can_answer)
        user.timezone = request.json.get('timezone', user.timezone)
        user.html_email = request.json.get('html_email', user.html_email)

        if 'password' in request.json.keys():
            password = request.json['password'].encode('utf-8')
            user.password = bcrypt.hashpw(password, bcrypt.gensalt())

        user.save()

        return {}, 204
