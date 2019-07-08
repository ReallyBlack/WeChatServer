from flask import Blueprint, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

import time

from WeChatServer.tools import db
#from WeChatServer.tools.auth import create_pwd, verify_password, generate_token, certify_token, remove_token
from WeChatServer.application.models import admin_list
from WeChatServer.tools.auth import create_uid, generate_auth_token
from WeChatServer.tools.verify import login_required

admin_api = Blueprint('admin', __name__)
api = Api(admin_api)

class admin_register(Resource):
    def post(self):

        # 从请求中获取表单数据
        mobel = request.form.get('mobel')
        password = request.form.get('password')
        username = request.form.get('username')

        # 当传入的mobel和password都不为空时，进行注册操作，否则返回错误信息
        if mobel and password:
            user = admin_list.query.filter_by(mobel=mobel).first()
            # 如果用户不存在则注册
            if user is None:
                # 生成用户唯一凭证
                id_code = create_uid(mobel)
                # 将用户基本信息存入到内存中
                user = admin_list(
                    username=username,
                    id_code=id_code,
                    mobel=mobel,
                )
                user.hash_password(password)
                try:
                # 用户信息存储成功，返回注册成功信息，并返回token，进入登录状态
                    db.session.add(user)
                    db.session.commit()
                    token=generate_auth_token(id_code)
                    response = dict(
                        errcode=0,
                        token=token,
                        code="success",
                        message="注册成功"
                    )
                except Exception as e:
                    # 未正常存储用户信息，返回异常提示
                    print(e)
                    response = dict(
                        errcode=1,
                        code="faild",
                        message="未知错误，请稍后重试"
                    )
                else:
                    # 未能正常生成salt，id_code， salt_password，返回异常提示
                    response = dict(
                        errcode=1,
                        code="faild",
                        message="未知错误，请稍后重试"
                    )
            # 如果用户已存在，提示用户已注册
            else:
                response = dict(
                    errcode=-1,
                    code="faild",
                    message="用户已注册，请更换手机号码"
                )
        elif mobel is None:
            response = dict(
                errcode=2,
                code="faild",
                message="请输入手机号"
            )
        elif password is None:
            response = dict(
                errcode=3,
                code="faild",
                message="请输入密码"
            )
        else:
            response = dict(
                errcode=500,
                code="faild",
                message="系统繁忙，请稍后重试"
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
            id_code = user.id_code
            if user.verify_password(password):
                # 密码验证成功
                token = generate_auth_token(id_code)
                response = dict(
                    errcode=0,
                    token=token,
                    code="success",
                    message="登录成功"
                )
            else:
                response = dict(
                    errcode=1,
                    code="faild",
                    message="手机号或密码错误"
                )
        else:
            response = dict(
                errcode=-1,
                code="faild",
                message="该手机号未注册管理员用户"
            )
        return jsonify(response)


class logout(Resource):
    #method_decorators = {'post': [login_required]}
    @login_required
    def post(self):
        response=dict(
            status=True,
            code=0,
            message='退出登录'
        )
        return jsonify(response)


api.add_resource(admin, '/admin/<string:ID>')
api.add_resource(manager, '/manager/admin/<string:ID>')
api.add_resource(manager_list, '/manager/admin')
api.add_resource(admin_register, '/admin/register')
api.add_resource(login, '/admin/login')
api.add_resource(logout, '/admin/logout')