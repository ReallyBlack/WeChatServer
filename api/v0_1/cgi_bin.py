# -*- coding='utf-8' -*-
import json

import requests
from flask import Blueprint, request, jsonify
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


class user_tags(Resource):
    """
    用户与用户标签管理
    # 拉去特定标签下的用户列表 https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=ACCESS_TOKEN
        请求方式 get
    # 批量为用户打标签 https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token=ACCESS_TOKEN
        请求方式 post
    # 批量为用户取消标签 https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token=ACCESS_TOKEN
        请求方式 post
    # 获取用户身上的标签列表 https://api.weixin.qq.com/cgi-bin/tags/getidlist?access_token=ACCESS_TOKEN
        请求方式 post 
    """
    def get(self):
        """
        1.当url参数中携带tagid时，表示查询对应tag下的用户列表
        2.当url参数中不携带tagid但是携带openid时，表示查询用户所拥有的标签
        3.当url参数中不携带tagid和openid时，提醒错误，缺失参数
        """
        token = Token.get_token('access_token')
        openid = request.args.get('openid', '')
        tagid = request.args.get('tagid', '')
        if tagid != '':
            body = {"tagid": tagid, "next_openid": openid}
            body = json.dumps(body)
            print(body)
            response = requests.post(
                'https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token={}'.format(token),
                body,
                json=True
            )
            return response.json()
        elif openid != '':
            body = {"openid" :  openid}
            response = requests.post(
                'https://api.weixin.qq.com/cgi-bin/tags/getidlist?access_token={}'.format(token),
                body.encode(),
                json=True
            )
            return response.json()
        else:
            response = dict(
                errcode=-1,
                errmsg="参数缺失或提供了错误的参数"
            )
            return jsonify(response)
    
    def put(self):
        openid_list = request.args.get('openid_list')
        tagid = request.args.get('tagsid')
        token = Token.get_token('access_token')
        body = {
            "openid_list": openid_list,
            "tagid": tagid
        }
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token={}'.format(token),
            json.dumps(body),
            json=True
        )
        return response.json()

    def delete(self):
        openid_list = request.args.get('openid_list')
        tagid = request.args.get('tagsid')
        token = Token.get_token('access_token')
        body = {
            "openid_list": openid_list,
            "tagid": tagid
        }
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token={}'.format(token),
            json.dumps(body),
            json=True
        )
        return response.json()


class user_remark(Resource):
    """
    用户备注
    # https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token=ACCESS_TOKEN
        请求方式post
        ！该功能只能微信认证的服务号使用
    """
    def put(self):
        openid = request.args.get('openid')
        remark = request.args.get('remark')
        token = Token.get_token('access_token')
        body = dict(
            openid=openid,
            remark=remark
        )
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token={}'.format(token),
            json.dumps(body),
            json=True
        )
        return response.json()

api.add_resource(menu, '/menu')
api.add_resource(tags, '/tags')
api.add_resource(user_tags, '/user/tags')
api.add_resource(user_remark, '/user/remark')