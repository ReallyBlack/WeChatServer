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
        return b'null', b'null', b'null'


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


# 创建token
def generate_token(id_code, TYPE='access_token'):
    """
    生成用户登录token
    :param id_code:用户唯一识别码，需要编码为bytes类型传入
    :param TYPE:生成access_token，默认值为access_token，当为token时，生成用户登录状态token
    """
    if TYPE == 'token':
        # 用于验证用户身份的token信息，在用户登录后15天内有效
        ts = str(time.time()+60*60*24*15).encode()
    else:
        # 用于验证用户请求的access_token信息，有效期为2小时
        ts = str(time.time()+3600).encode()
    # 加密
    sha1_tshexstr = hmac.new(id_code,ts,'sha1').hexdigest()
    token = "{}:{}:{}".format(id_code, ts.decode(), sha1_tshexstr)
    # 将token存入redis
    redis_cli = redis.StrictRedis(connection_pool=connect_pool)
    if f:
        redis_cli.hmset("token", { id_code: token })
    else:
        redis_cli.hmset("access_tokens", { id_code: token })
    return base64.urlsafe_b64encode(token.encode()).decode()



# 认证失败返回False，None数据
# 认证成功返回True， token数据
def certify_token(token, user):
    try:
        # token数据解码
        token = base64.urlsafe_b64decode(token).decode()
        token_list = token.split(':')
        # token数据不正常
        if len(token_list) != 3:
            return False, None
        id_code = token_list[0]
        if id_code == user:
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
        return False, None # cookie被篡改。
    except:
        return False, None # 数据错误

# 用户登录认证
def verify_login(func):
    @wraps(func)
    def wrapper():
        token = request.cookies.get('token', None)
        user = request.cookies.get('user', None)
        f, t = certify_token(token, user)
        return func(is_login=f, token=t if token!=t else None)
    return wrapper
