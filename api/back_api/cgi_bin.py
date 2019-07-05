# -*- coding='utf-8' -*-
import json

import requests
from flask import Blueprint, request
from flask_restful import reqparse, abort, Api, Resource

from WeChatServer.tools import Token

cgi_api = Blueprint('cgi', __name__)
api = Api(cgi_api)


class menu(Resource):
    '''
    # 自定义菜单接口
    # 创建菜单 https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
        请求方式： post

    # 查询菜单 https://api.weixin.qq.com/cgi-bin/menu/get?access_token=ACCESS_TOKEN
        请求方式： get

    # 删除菜单 https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=ACCESS_TOKEN
        请求方式： get
    '''
    def post(self):
        """
        创建自定义菜单
        """
        token = Token.get_token('access_token')
        data = request.data.decode().encode()
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}'.format(token),
            data,
            json=True
        )
        return response.json()
    
    def get(self):
        """
        查询自定义菜单
        """
        token = Token.get_token('access_token')
        response = requests.get('https://api.weixin.qq.com/cgi-bin/menu/get?access_token={}'.format(token))
        # response = response.json()
        # response = json.dumps(response, separators=(',', ':'), ensure_ascii=False)
        # print(response)
        return response.json()    
    
    def delete(self):
        """
        删除自定义菜单
        """
        token = Token.get_token('access_token')
        response = requests.get('https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={}'.format(token))
        return response.json()


class tags(Resource):
    """
    用户标签管理
    # 创建标签： https://api.weixin.qq.com/cgi-bin/tags/create?access_token=ACCESS_TOKEN
        请求方式 post
    # 获取标签： https://api.weixin.qq.com/cgi-bin/tags/get?access_token=ACCESS_TOKEN
        请求方式 get
    # 修改标签： https://api.weixin.qq.com/cgi-bin/tags/update?access_token=ACCESS_TOKEN
        请求方式 post
    # 删除标签： https://api.weixin.qq.com/cgi-bin/tags/delete?access_token=ACCESS_TOKEN
        请求方式 post
    """
    def post(self):
        name = request.args.get('name')
        body = {"tag": {"name": name }}
        token = Token.get_token('access_token')
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/tags/create?access_token={}'.format(token),
            body.encode(),
            json=True
        )
        return response.json()

    def get(self):
        token = Token.get_token('access_token')
        response = requests.get('https://api.weixin.qq.com/cgi-bin/tags/get?access_token={}'.format(token))
        return response.json()
    
    def put(self):
        tag_id = request.args.get('id')
        name = request.args.get('name')
        body = {"tag": {"id": tag_id, "name": name}}
        token = Token.get_token('access_token')
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/tags/update?access_token={}'.format(token),
            body.encode(),
            json=True
        )
        return response.json()
    
    def delete(self):
        tag_id = request.args.get('id')
        body = {"tag":{"id": tag_id}}
        token = Token.get_token('access_token')
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/tags/delete?access_token={}'.format(token),
            body.encode(),
            json=True
        )
        return response.json()

api.add_resource(menu, '/menu')
api.add_resource(tags, '/tags')