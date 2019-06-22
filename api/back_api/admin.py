from flask import Blueprint, request
from flask_restful import reqparse, abort, Api, Resource

import time

from WeChatServer.tools import db
from WeChatServer.tools.encryption import create_pwd, verify_password, generate_token, certify_token
from WeChatServer.wms.models import admin_list


admin_api = Blueprint('admin', __name__)
api = Api(admin_api)

class admin_register(Resource):
    def post(self):

        # 从请求中获取表单数据
        mobel = request.form.get('mobel')
        password = request.form.get('password')
        username = request.form.get('username')

        user = admin_list.query.filter_by(mobel=mobel).first()
        # 如果用户不存在则注册
        if user is None:
            salt, id_code, salt_password = create_pwd(mobel, password)
            token = generate_token(id_code)
            user = admin_list(
                username=username,
                id_code=id_code,
                salt_password=salt_password,
                mobel=mobel,
                salt=salt,
            )
            try:
                db.session.add(user)
                db.session.commit()
                return {"token": token, "code": "200", "info": "register success"},200
            except:
                return {"info": "register failed", "code": "500"},500
        return {"info": "The mobel had registered", "code": "406"},406


class admin(Resource):
    # 获取管理员用户信息
    def get(self):
        # 管理员用户姓名
        # 管理员用户昵称
        # 管理员用户手机号
        # 管理员用户微信号
        # 管理员用户权限
        pass

    # 更新管理员用户基本信息
    def put(self):
        # 管理员的昵称
        # 管理员的手机号
        # 管理员的微信号
        # 管理员的密码
        pass


class manager(Resource):

    # 超级管理员获取管理员信息
    def get(self, ID):
        pass

    # 超级管理员修改管理员权限
    def put(self, ID):
        pass
        

    # 超级管理员封禁普通管理员
    def delete(self, ID):
        pass
        


class manager_list(Resource):
    def get(self):
        pass



api.add_resource(admin, '/admin/<string:ID>')
api.add_resource(manager, '/manager/admin/<string:ID>')
api.add_resource(manager_list, '/manager/admin')
api.add_resource(admin_register, '/admin/register')