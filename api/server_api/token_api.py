from flask import Blueprint
from flask_restful import reqparse, abort, Api, Resource

token_api = Blueprint('token', __name__)

api = Api(token_api)

class Todo(Resource):
    def get(self):
        return {'todo': 'test'}
    def post(self):
        return {'todo': 'post test'}

api.add_resource(Todo, '/todo')
