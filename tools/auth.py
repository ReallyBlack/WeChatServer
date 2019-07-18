import os, hashlib, binascii, uuid, time, base64, hmac
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from functools import wraps

import redis
from flask import request
from flask import current_app as app

# 使用db2存储用户登录token信息
connect_pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db='3')


def create_uid(mobel):
    salt = binascii.hexlify(os.urandom(8))
    uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, mobel))
    uid = ''.join(uid.split('-'))
    return (salt+uid.encode()).decode()


def generate_auth_token(id_code, expiration=60*60*24*15):
    """
    签发用户认证token
    :param id_code:用户唯一凭证
    :param expriation:token过期时间，默认为15天
    :return token:返回用户token
    """
    from flask import current_app as app
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': id_code}).decode()


def verifyToken(token):
    """
    验证用户认证token
    :param token:要验证的token
    :return :token正确返回字典，包含status和data信息，错误token额外包含errcode
    """
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        return dict(
            data=data['id'],
            status=True
        )
    except SignatureExpired:
        return dict(
            errcode=1,
            data='token has expired, please login again',
            status=False
        )
    except BadSignature:
        return dict(
            errcode=2,
            data='token not allow use',
            status=False
        )
    except Exception as e:
        return dict(
            errcode=3,
            data=e,
            status=False
        )