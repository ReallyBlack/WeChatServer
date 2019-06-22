import redis

from flask import request

from functools import wraps
import os, hashlib, binascii, uuid, time, base64, hmac
#import itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 使用db2存储用户登录token信息
connect_pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db='3')


# 传入注册时的手机号和用户密码
# 返回用户的salt， id_code 和 salt_password
def create_pwd(mobel=None, password=None):
    if mobel and password:
        hash = hashlib.sha512()
        # 生成加密盐
        salt = binascii.hexlify(os.urandom(32))

        # 生成用户id_code
        uu_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, mobel))
        uu_id = ''.join(uu_id.split('-'))
        id_code = uu_id.encode()+salt

        # 生成加密密码salt_password
        hash.update(id_code)
        hash.update(salt)
        hash.update(password)
        salt_password = hash.digest()

        return salt, id_code, salt_password
    else:
        return None, None, None


# 验证用户密码，如果密码正确，则返回True，否则返回False
def verify_password(password, salt, id_code, salt_password):
    hash = hashlib.sha512()
    hash.update(id_code)
    hash.update(salt)
    hash.update(password)
    verify_password = hash.digest()
    if verify_password == salt_password:
        return True
    else:
        return False


# 创建token
def generate_token(id_code):
    # 创建过期时间戳
    ts = str(time.time()+3600).encode()
    # 加密
    sha1_tshexstr = hmac.new(id_code.encode(),ts,'sha1').hexdigest()
    token = "{}:{}:{}".format(id_code, ts.decode(), sha1_tshexstr)
    # 将token存入redis
    redis_cli = redis.StrictRedis(connection_pool=connect_pool)
    redis_cli.hmset("tokens", { id_code: token})
    return base64.urlsafe_b64encode(token.encode()).decode()



# 认证失败返回False，None数据
# 认证成功返回True， token数据
def certify_token(token):
    # token数据解码
    token = base64.urlsafe_b64decode(token).decode()
    token_list = token.split(':')
    # token数据不正常
    if len(token_list) != 3:
        return False, None
    id_code = token_list[0]
    # 从redis查找token，若不存在或不同，则认证失败
    redis_cli = redis.StrictRedis(connection_pool=connect_pool)
    token_true = redis_cli.hmget("tokens", id_code).decode()[0]

    if token_true == token:
        # token数据正确，验证时长
        if float(token_list[1]) < time.time():
        # token 过期
            return False, None
        # token即将过期，则更新token信息
        elif float(token_list[1]) - float(time.time()) < 60:
            token = generate_token(id_code)
        return True, token


# 用户登录认证
def verify_login(func):
    @wraps(func)
    def wrapper():
        pass
