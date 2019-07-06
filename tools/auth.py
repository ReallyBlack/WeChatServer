import redis

from flask import request

from functools import wraps
import os, hashlib, binascii, uuid, time, base64, hmac
#import itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 使用db2存储用户登录token信息
connect_pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db='3')


def create_pwd(mobel=None, password=None):
    """
    用于用户注册时生成加盐密码
    :param mobel:用户注册的手机号码，需要编码成bytes类型传入
    :param password:用户注册时的密码，需要编码成bytes类型传入
    :return salt:用户密码盐，bytes类型
    :return id_code:用户识别码id_code，bytes类型
    :return salt_password:用户加盐密码，bytes类型
    """
    if mobel and password:
        h = hashlib.sha1()
        # 生成加密盐
        salt = binascii.hexlify(os.urandom(32))

        # 生成用户id_code
        uu_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, mobel))
        uu_id = ''.join(uu_id.split('-'))
        id_code = uu_id.encode()+salt

        # 生成加密密码salt_password
        h.update(id_code)
        h.update(salt)
        h.update(password)
        salt_password = h.digest()
        return salt, id_code, salt_password
    else:
        return None, None, None


def verify_password(password, salt, id_code, salt_password):
    """
    用户登录密码验证
    :param password:用户登录密码，需要编码成bytes类型传入
    :param salt:用户密码盐，需要编码成bytes类型传入
    :param id_code:用户唯一识别码，需要编码成bytes类型传入
    :param salt_password:用户加盐密码， str类型，从数据库读取后直接传入即可
    :return :认证正确返回True，认证错误返回False
    """
    hash = hashlib.sha1()
    hash.update(id_code)
    hash.update(salt)
    hash.update(password)
    verify_password = hash.digest()
    if str(verify_password) == salt_password:
        return True
    else:
        return False


def generate_token(id_code, TYPE='access_token'):
    """
    生成用户登录token
    :param id_code:用户唯一识别码，需要编码为bytes类型传入
    :param TYPE:生成access_token，默认值为access_token，当为token时，生成用户登录状态token
    :return token:加密后的token信息
    """
    if TYPE == 'token':
        # 用于验证用户身份的token信息，在用户登录后15天内有效
        ts = str(time.time()+60*60*24*15).encode()
    else:
        # 用于验证用户请求的access_token信息，有效期为2小时
        ts = str(time.time()+3600).encode()
    # 加密
    # 将用户唯一识别码与过期时间进行加密，生成验证信息
    sha1_tshexstr = hmac.new(id_code,ts,'sha1').hexdigest()
    token = "{}:{}:{}".format(id_code.decode(), ts.decode(), sha1_tshexstr)

    # 将token存入redis
    redis_cli = redis.StrictRedis(connection_pool=connect_pool)
    redis_cli.hset(TYPE, id_code, token )

    # 返回加密后的token
    return base64.urlsafe_b64encode(token.encode()).decode()


def certify_token(token, TYPE='access_token'):
    """
    验证token有效性及更新token信息
    :param token:要进行验证的token
    :param TYPE:默认值为‘access_token’，当为‘token’时，验证用户登录状态信息
    :return :token正确或已更新返回token，错误时返回False
    """
    try:
        # token数据解码
        token = base64.urlsafe_b64decode(token).decode()
        token_list = token.split(':')
        # token数据不正常
        if len(token_list) != 3:
            return False
        id_code = token_list[0]
        # token正常，从redis中取出正确的token比较
        redis_cli = redis.StrictRedis(connection_pool=connect_pool)
        token_true = redis_cli.hget(TYPE, id_code).decode()

        if token_true == token:
        # token信息正确，未被篡改
  
            # token数据正确，验证时长
            if float(token_list[1]) < time.time():
                # token 过期，返回False
                return False
            # token即将过期，则更新token信息
            elif float(token_list[1]) - float(time.time()) < 60:
                token = generate_token(id_code)
            return token
        return False # cookie被篡改。
    except:
        return False # 数据错误


def remove_token(id_code, TYPE='access_token'):
    """
    用户退出后删除用户token
    :param id_code:用户唯一标识，用于查找用户token
    :param TYPE:默认查找哈希表access_token，指定为token时查找token表
    :return :True,正常删除token；False，异常情况
    """
    try:
        redis_cli = redis.StrictRedis(connection_pool=connect_pool)
        result = redis_cli.hdel(TYPE, id_code)
        if result == 1:
            return True
        else:
            raise Exception
    except Exception as e:
        return False
