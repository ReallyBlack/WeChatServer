from flask import Blueprint, request
from flask_restful import reqparse, abort, Api, Resource
# import requests

cgi_api = Blueprint('cgi', __name__)
api = Api(cgi_api)


'''
# 自定义菜单接口
# 创建菜单 https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
    请求方式： post

# 查询菜单 https://api.weixin.qq.com/cgi-bin/menu/get?access_token=ACCESS_TOKEN
    请求方式： get

# 删除菜单 https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=ACCESS_TOKEN
    请求方式： get
'''
class menu(Resource):

    def post(self):
        """
        创建自定义菜单
        """
        pass
    
    def get(self):
        """
        查询自定义菜单
        """
        pass
    
    def delete(self):
        """
        删除自定义菜单
        """
        pass