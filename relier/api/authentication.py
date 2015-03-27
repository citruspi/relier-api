from relier.api import Resource
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

class AuthenticatedResource(Resource):

    method_decorators = [verify]

class TokenResource(Resource):

    def post(self):

        if not request.json:
            abort(400)

        try:
            email = request.json['email_address']
            password = request.json['password']
        except KeyError:
            abort(400)

        token = User.login(email, password)

        if token is None:
            abort(401)

        return {'token': token}
