import os
import hashlib
import binascii
import uuid


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