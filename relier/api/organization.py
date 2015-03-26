from relier.models import Organization, User, database
from flask.ext import restful
from flask import abort, request, make_response
import bcrypt

class OrganizationResource(restful.Resource):

    def post(self):

        try:
            body = request.json
        except:
            abort(400)

        user = {}
        name = None

        try:
            name = body['name'].encode('utf-8')
            user['firstname'] = body['user']['first_name'].encode('utf-8')
            user['lastname'] = body['user']['last_name'].encode('utf-8')
            user['email'] = body['user']['email_address'].encode('utf-8')
            user['password'] = body['user']['password'].encode('utf-8')
        except KeyError:
            abort(400)

        if Organization.exists(name):
            abort(409)

        if User.exists(user['email']):
            abort(409)

        with database.atomic() as transaction:

            try:
                organization = Organization.create(name = name)
            except:
                abort(500)

            user['password'] = bcrypt.hashpw(user['password'], bcrypt.gensalt())
            user['is_admin'] = True
            user['organization'] = organization

            try:
                User.create(**user)
            except Exception as e:
                print e
                abort(500)

        response = make_response('', 201)
        response.headers['Location'] = '/organizations/{id_}/'.format(
                                                        id_ = organization.id)
        return response

