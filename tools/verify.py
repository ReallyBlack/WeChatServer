import hashlib
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

# 定义一些认证方法的装饰器
from flask import request, jsonify
#from flask_httpauth import HTTPTokenAuth

from WeChatServer.config import auth
from WeChatServer.application.models import admin_list
from .minifun import str_to_list as str2list

AppInfo = auth.APPINFO

#authToken = HTTPTokenAuth()

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
        token = request.headers.get('Authorization').split(" ")
        print(token)
        return request.headers.get('token')


def login_required(func):
    
    @wraps(func)
    def wrapper(self):
        from flask import current_app as app
        token = request.headers.get('authorization')
        if token is not None:
            token = token.split(' ')[1]
            s = Serializer(app.config['SECRET_KEY'])
            try:
                # 尝试读取token中的信息
                data = s.loads(token)
                return func(self)
            except SignatureExpired:
                return jsonify(dict(
                    errcode=1,
                    errmsg="token has expired, please login again"
                ))
            except BadSignature:
                return jsonify(dict(
                    errcode=2,
                    errmsg="token not allow use"
                ))
            except Exception as e:
                print(e)
                return jsonify(dict(
                    errcode=3,
                    errmsg=''
                ))
        else:
            return jsonify(dict(
                errcode=-1,
                errmsg="not allow without log in"
            ))
    return wrapper


def verifyToken(func):
    """
    token鉴权验证，用于确认用户登录的合法性
    """
    @wraps(func)
    def wrapper(self):
        # 从请求中获得token
        token = request.headers.get('authorization').split(' ')[1]
        from flask import current_app as app
        s = Serializer(app.config['SECRET_KEY'])
        try:
            # 尝试读取token中的信息
            data = s.loads(token)
        except SignatureExpired:
            return dict(
                errcode=1,
                errmsg="token has expired, please login again"
            )
        except BadSignature:
            return dict(
                errcode=2,
                errmsg="token not allow use"
            )
        try:
            user = admin_list.query.filter_by(id_code=data['id']).first()
            print(user)
            return func(self, user.is_root, str2list(user.permission_list))
        except Exception as e:
            print(e)
            return jsonify(dict(errcode=-1, errmsg='unknown error'))
    return wrapper


def verifyPermission(func):
    @wraps(func)
    @verifyToken
    def wrapper(self, is_root=0, permission_list=[]):
        if is_root == 1:
            return func()
        elif self.__permission__ in permission_list:
            return func()
        else:
            return jsonify(dict(errcode=1, errmsg='no access '))
    return wrapper