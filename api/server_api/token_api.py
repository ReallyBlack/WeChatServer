from flask import Blueprint
from flask_restful import reqparse, abort, Api, Resource
import redis
import time

# 暂时使用固定的redis作为token存放的数据库，后期进行模块化处理
# from config import settings
# sql = settings.get('server_sql')

token_api = Blueprint('token', __name__)

api = Api(token_api)
connect_pool = redis.connection_pool(host='127.0.0.1', port=6379, db=2)
redis_cli = redis.StrRedis(connection_pool=connect_pool, decode_responses=True)

# key为db中存入的数据
# 当key为token时，表示存入取出access_token，包含字段为access_token,expires_in
# 当key为js_ticket时，表示存入/取出js_api_ticket,包括字段为ticket,expires_in
# 当key为api_ticket时，表示存入/取出api_ticket，包括字段为ticket,expires_in

server_api = {
    "token": 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi',
    "js_ticket": '',
    "api_ticket": '',
}

def save_db(key):
    

def read_db(key):
    

class Token(Resource):
    def get(self):
        access_token, expires_in = redis_cli.get("token", "access_token", "expires_in")
        if 

"""
class Todo(Resource):
    def get(self):
        return {'todo': 'test'}
    def post(self):
        return {'todo': 'post test'}

api.add_resource(Todo, '/todo')
"""
