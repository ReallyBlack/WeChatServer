import hashlib
from functools import wraps

# 定义一些认证方法的装饰器
from flask import request, jsonify

#from config import auth
from WeChatServer.config import auth
from WeChatServer.tools.auth import certify_token

AppInfo = auth.APPINFO


# 服务器消息认证装饰器，用来判断消息是否来自微信服务器
def isServer(f):
    @wraps(f)
    def wrapper():
        data = sorted([AppInfo['token'], str(request.args.get('timestamp')), str(request.args.get('nonce'))])
        hashcode = hashlib.sha1(''.join(data).encode('utf-8')).hexdigest()
        if request.args.get('signature') == hashcode:
            verifycode = request.args.get('echostr')
            is_server = True
        else:
            verifycode = 'The request not come from wexin server'
            is_server = False
        return f(echostr=verifycode, code=is_server)
    return wrapper


def access_token():
    return request.headers.get('access_token')

def token():
    if request.authorization:
        return request.authorization
    else:
        return request.headers.get('token')


def verifyToken(func):
    @wraps(func)
    def wrapper():
        # 先验证access_token，如果access_token正确，进行后面的操作
        # 如果access_token错误或过期，验证token是否正确
        # 当token正确时，重新获得access_token
        # 如果token过期，则提醒用户重新登录
        access_token = certify_token(access_token())
        # access_token过期状态
        if not access_token:
            # 验证用户token是否过期，如果未过期，则重新签发access_token
            # 如果过期，返回重新登录提醒
            token = certify_token(token(), TYPE='token')
            if not token:
                # token 过期，返回重新登录提醒
                return jsonify({"errcode": 1, "errmsg": "token expires, please login again"})
            else:
                pass

