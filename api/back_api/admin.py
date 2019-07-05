from flask import Blueprint, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

import time

from WeChatServer.tools import db
from WeChatServer.tools.auth import create_pwd, verify_password, generate_token, certify_token
from WeChatServer.application.models import admin_list


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
            salt, id_code, salt_password = create_pwd(mobel, password.encode())
            print(salt_password)
            token = generate_token(id_code)
            user = admin_list(
                username=username,
                id_code=id_code.decode(),
                salt_password=str(salt_password),
                mobel=mobel,
                salt=salt.decode(),
            )
            try:
                print(user)
                db.session.add(user)
                db.session.commit()
                response = dict(
                    errcode=0,
                    token=token,
                    code="success",
                    message="注册成功"
                )
            except Exception as e:
                print(e)
                response = dict(
                    errcode=1,
                    code="faild",
                    message="未知错误，请稍后重试"
                )
        else:
            response = dict(
                errcode=-1,
                code=500,
                message="用户已注册，请更换手机号码"
            )
        return jsonify(response)


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


class login(Resource):
    def post(self):
        password = request.form.get('password')
        mobel = request.form.get('mobel')
        user = admin_list.query.filter_by(mobel=mobel).first()
        if user is not None:  # 手机号正确
            id_code = user.id_code.encode()
            salt = user.salt.encode()
            salt_password = user.salt_password
            if verify_password(password.encode(), salt, id_code, salt_password):
                token = generate_token(id_code)
                response = dict(
                    errcode=0,
                    token=token,
                    code="success",
                    message="登录成功"
                )
            else:
                response = dict(
                    errcode=500,
                    code="faild",
                    message="手机号或密码错误"
                )
        else:
            response = dict(
                errcode=505,
                code="faild",
                message="该手机号未注册管理员用户"
            )
        return jsonify(response)

api.add_resource(admin, '/admin/<string:ID>')
api.add_resource(manager, '/manager/admin/<string:ID>')
api.add_resource(manager_list, '/manager/admin')
api.add_resource(admin_register, '/admin/register')
api.add_resource(login, '/admin/login')