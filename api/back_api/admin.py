from flask import Blueprint
from flask_restful import reqparse, abort, Api, Resource

admin_api = Blueprint('admin', __name__)
api = Api(admin_api)


class admin(Resource):
    # 获取管理员用户信息
    def get(self):
        # 管理员用户姓名
        # 管理员用户昵称
        # 管理员用户手机号
        # 管理员用户微信号
        # 管理员用户权限

    # 新管理员用户注册
    def post(self):
        # 获得传入的用户数据
        # 1.username，管理员姓名，对应数据库admin字段
        # 2.password，管理员注册密码，经过加盐后存入到数据库中
        # 3.phone_number,管理员注册手机号，可用于登录账户，密码找回唯一凭证
        # 4.wechat，管理员注册时微信号
        # 5.其他权限为0，可与超级管理员申请获得某权限

    # 更新管理员用户基本信息
    def put(self):
        # 管理员的昵称
        # 管理员的手机号
        # 管理员的微信号
        # 管理员的密码


class manager(Resource):

    # 超级管理员获取管理员信息
    def get(self, ID):

    # 超级管理员修改管理员权限
    def put(self, ID):
        

    # 超级管理员封禁普通管理员
    def delete(self, ID):
        


class manager_list(Resource):
    def get(self):



api.add_resource(admin, '/admin/<string:ID>')
api.add_resource(manager, '/manager/admin/<string:ID>')
api.add_resource(manager_list, '/manager/admin')