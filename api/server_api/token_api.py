import requests, redis, xmltodict
from flask import Blueprint
from flask_restful import reqparse, abort, Api, Resource

import time
import ast
from config import auth

appinfo = auth.APPINFO
# 暂时使用固定的redis作为token存放的数据库，后期进行模块化处理
# from config import settings
# sql = settings.get('server_sql')

token_api = Blueprint('token', __name__)
api = Api(token_api)

connect_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)
# redis_cli = redis.StrRedis(connection_pool=connect_pool, decode_responses=True)

# key为db中存入的数据
# 当key为token时，表示存入取出access_token，包含字段为access_token,expires_in
# 当key为js_ticket时，表示存入/取出js_api_ticket,包括字段为ticket,expires_in
# 当key为api_ticket时，表示存入/取出api_ticket，包括字段为ticket,expires_in

server_api = {
    "token": 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appinfo.get('appID'),appinfo.get('appsecret')),
    "js_ticket": 'None',
    "api_ticket": 'None',
}

# 获取token/ticket并存储到redis，返回token或ticket或False
def save_db(key):
    response = requests.get(server_api.get(key))
    response = ast.literal_eval(response.text)
    if key == 'token':
        field = dict(
            t=response.get('access_token'),
            e=response.get('expires_in')+int(time.time())
        )
    elif key in ("js_ticket", "api_ticket"):
        field = dict(
            t=response.get('ticket'),
            e=response.get('expires_in')+int(time.time())-300
        )
    else:
        field = {"t": False}
    try:
        redis_cli = redis.StrictRedis(connection_pool=connect_pool)
        redis_cli.hmset(key, field)
        return field.get("t", False)
    except:
        False

# 从redis中读取已经存入的数据
def read_db(key):
    try:
        redis_cli = redis.StrictRedis(connection_pool=connect_pool)
        t, e = redis_cli.hmget(key, 't', 'e')
        return t.decode(), int(e.decode())
    except:
        return None, 0


# t表示token/ticket。e表示expires_in
class Token(Resource):
    def get(self, key):
        if key not in ("token", "js_ticket", "api_ticket"):
            return 404
        t, e = read_db(key)
        if t and e > int(time.time()):
            return {"t": t, "status": "success"},200
        else:
            t = save_db(key)
            if t:
                return {"t": t, "status": "success"},200
            else:
                return {"message": "no token"},200

api.add_resource(Token, '/t/<string:key>')