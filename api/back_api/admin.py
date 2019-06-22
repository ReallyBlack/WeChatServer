from flask import Blueprint
from flask_restful import reqparse, abort, Api, Resource



admin_api = Blueprint('admin', __name__)
api = Api(admin_api)

salt = 'This is a salt for password'


class admin_register(Resource):

    def post(self):




class admin(Resource):
    # 获取管理员用户信息
    def get(self):
        # 管理员用户姓名
        # 管理员用户昵称
        # 管理员用户手机号
        # 管理员用户微信号
        # 管理员用户权限

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
