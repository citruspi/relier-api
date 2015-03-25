from flask import Flask
from flask.ext import restful
from organization import OrganizationResource

app = Flask(__name__)
api = restful.Api(app)

api.add_resource(OrganizationResource, '/organizations/')
