from flask.ext import restful
from relier.models import User
from flask import abort, request

class TokenResource(restful.Resource):

    def post(self):

        try:
            body = request.json
            email = body['email_address']
            password = body['password']
        except KeyError:
            abort(400)

        token = User.login(email, password)

        if token is None:
            abort(401)

        return {'token': token}

