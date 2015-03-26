from flask.ext import restful
from flask import abort, request, make_response
from relier.models import User, Invitation

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
