from flask.ext import restful
from flask import abort, request, make_response
from relier.models import User, Invitation
from relier.api.authentication import verify
from flask import g

class UserResource(restful.Resource):

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

        users = [{
                    'id': user.id,
                    'first_name': user.firstname,
                    'last_name': user.lastname,
                    'timezone': user.timezone,
                    'is_admin': user.is_admin,
                    'can_ask': user.can_ask,
                    'can_answer': user.can_answer,
                    'email': user.email
                 } for user in query]

        return users
