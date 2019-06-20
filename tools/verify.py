# 定义一些认证方法的装饰器
from flask import request

import hashlib
from functools import wraps

from config import auth

AppInfo = auth.APPINFO


# 服务器消息认证装饰器，用来判断消息是否来自微信服务器
def isServer(f):
    @wraps(f)
    def wrapper():
        data = sorted([AppInfo['token'], str(request.args.get('timestamp')), str(request.args.get('nonce'))])
        hashcode = hashlib.sha1(''.join(data).encode('utf-8')).hexdigest()
        if request.args.get('signature') == hashcode:
            verifycode = request.args.get('echostr')
        else:
            verifycode = 'The request not come from wexin server'
        return f(verifycode)
    return wrapper