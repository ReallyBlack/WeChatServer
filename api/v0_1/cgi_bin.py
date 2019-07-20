# -*- coding='utf-8' -*-
import json

import requests
from flask import Blueprint, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

from WeChatServer.tools import Token, db
from WeChatServer.application.models import fancy_list
from WeChatServer.tools.verify import verify_permission
from WeChatServer.tools.func_tools import create_or_update_fancy

# 特殊lambda函数
unicode_2_utf8 = lambda s: s.encode('unicode_escape').decode()
new_fancy = lambda openid: fancy_list(openid=openid) if not fancy_list.query.filter_by(openid=openid).first() else None


cgi_api = Blueprint('cgi', __name__)
api = Api(cgi_api)

class menu(Resource):
    __permission__ = 'menu'

    # method_decorators = {'get':[verify_permission]}
    '''
    # 自定义菜单接口
    # 创建菜单 https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
        请求方式： post

    # 查询菜单 https://api.weixin.qq.com/cgi-bin/menu/get?access_token=ACCESS_TOKEN
        请求方式： get

    # 删除菜单 https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=ACCESS_TOKEN
        请求方式： get
    '''

    @verify_permission
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

    @verify_permission
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

    @verify_permission
    def delete(self):
        """
        删除自定义菜单
        """
        token = Token.get_token('access_token')
        response = requests.get('https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={}'.format(token))
        return response.json()


class tags(Resource):
    __permission__ = 'tags'
    # method_decorators = [verifyPermission]
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

    @verify_permission
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

    @verify_permission
    def get(self):
        token = Token.get_token('access_token')
        response = requests.get('https://api.weixin.qq.com/cgi-bin/tags/get?access_token={}'.format(token))
        return response.json()

    @verify_permission
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

    @verify_permission
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
    __permission__ = 'tags'
    # method_decorators = [verifyPermission]
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

    @verify_permission
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

    @verify_permission
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

    @verify_permission
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
    __permission__ = 'user'
    # method_decorators = [verifyPermission]
    """
    用户备注
        # https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token=ACCESS_TOKEN
        请求方式post
        ！该功能只能微信认证的服务号使用
    """

    @verify_permission
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


class user_info(Resource):
    __permission__ = 'user'
    # method_decorators = [verifyPermission]
    # 获取用户信息
    # 从用户列表中直接获取用户信息
    def get_data(f, detaile=False):
        if detaile:
            return dict(
                    subscribe=f.subscribe,
                    nickname=f.get_nickname(),
                    sex='男' if f.sex == '1' else '女' if f.sex == '2' else '未知',
                    city=f.city,
                    country=f.country,
                    province=f.province,
                    language=f.language,
                    headimgurl=f.headimgurl,
                    subscribe_time=f.subscribe_time,
                    remark=f.remark,
                    groupid=f.groupid,
                    tagid_list=f.tagid_list,
                    subscribe_scene=f.subscribe_scene,
                    qr_scene=f.qr_scene,
                    qr_scene_str=f.qr_scene_str,
            )
        else:
            return dict(
                subscribe=f.subscribe,
                nickname=f.get_nickname(),
                sex='男' if f.sex == '1' else '女' if f.sex == '2' else '未知',
                city=f.city,
                country=f.country,
                province=f.province,
                remark=f.remark,
                tagid_list=f.tagid_list,
            )

    @verify_permission
    def get(self):
        openid = request.args.get('openid')
        details = request.args.get('details')
        user = fancy_list.query.filter_by(openid=openid).first()
        if not openid:
            response=dict(
                status=False,
                errmsg="miss the openid，nothing can get"
            )
        if user:
            if details:
                data = self.get_data(user, details)
            else: 
                data = self.get_data(user)
            return jsonify(dict(
                status=True,
                data=data
            ))
        else:
            return jsonify(dict(
                status=False,
                errmsg="openid was falsed"
            ))

    # 刷新用户信息
    # 从微信服务器获得用户信息，更新到数据库并返回数据到前端
    @verify_permission
    def put(self):
        token = Token.get_token('access_token')
        openid = request.values.get('openid')
        if openid:
            if create_or_update_fancy(openid):
                fancy = fancy_list.query.filter_by(openid=openid).first()
                data = self.get_data(fancy)
                return jsonify(dict(
                    status=True,
                    data=data
                ))
            else:
                return jsonify(dict(
                    status=False,
                    errmsg="Error with server, please try again later"
                ))
        else:
            return jsonify(dict(
                status=False,
                errmsg="without openid"
            ))

class user_list(Resource):

    def get(self):
        token = Token.get_token('access_token')
        next_openid = request.args.get('next_openid')
        if not next_openid:
            next_openid=''
        response = requests.get('https://api.weixin.qq.com/cgi-bin/user/get?access_token={}&next_openid={}'.format(token, next_openid))
        return response.json()

    def put(self):
        token = Token.get_token('access_token')
        next_openid = request.args.get('next_openid')
        if not next_openid:
            next_openid = ''
        response = requests.get('https://api.weixin.qq.com/cgi-bin/user/get?access_token={}&next_openid={}'.format(token, next_openid))
        data = response.json()['data']['openid']
        openid_list = [new_fancy(openid) for openid in data if new_fancy(openid)]
        try:
            db.session.add_all(openid_list)
            db.session.commit()
        except Exception as e:
            return jsonify(dict(
                errmsg=str(e)
            ))
        else:
            return jsonify(dict(data=data))


api.add_resource(menu, '/menu')
api.add_resource(tags, '/tags')
api.add_resource(user_tags, '/user/tags')
api.add_resource(user_remark, '/user/remark')
api.add_resource(user_info, '/user/info')
api.add_resource(user_list, '/user/list')