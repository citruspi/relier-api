from flask.ext import restful
from relier.models import User
from flask import abort, request, g
from functools import wraps

def verify (function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Auth-Token')

        user = User.authenticate(token)

        if user is None:
            abort(401)

        g.user = user

        return function(*args, **kwargs)
    return wrapper

class AuthenticatedResource(restful.Resource):

    method_decorators = [verify]

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
