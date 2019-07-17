# -*- coding='utf-8' -*-
import json

import requests
from flask import Blueprint, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

from WeChatServer.tools import Token, db
from WeChatServer.application.models import fancy_list
from WeChatServer.tools.verify import verify_permission

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
                response = dict(
                    errcode=0,
                    subscribe=user.subscribe,
                    nickname=user.get_nickname(),
                    sex='男' if user.sex == '1' else '女' if user.sex == '2' else '未知',
                    city=user.city,
                    country=user.country,
                    province=user.province,
                    language=user.language,
                    headimgurl=user.headimgurl,
                    subscribe_time=user.subscribe_time,
                    remark=user.remark,
                    groupid=user.groupid,
                    tagid_list=user.tagid_list,
                    subscribe_scene=user.subscribe_scene,
                    qr_scene=user.qr_scene,
                    qr_scene_str=user.qr_scene_str,
                )
            else: 
                response=dict(
                    errcode=0,
                    subscribe=user.subscribe,
                    nickname=user.get_nickname(),
                    sex='男' if user.sex == '1' else '女' if user.sex == '2' else '未知',
                    city=user.city,
                    country=user.country,
                    province=user.province,
                    remark=user.remark,
                    tagid_list=user.tagid_list,
                )
            return jsonify(dict(
                status=True,
                data=response
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
        user = fancy_list.query.filter_by(openid=openid).first()
        if openid:
            response = requests.get(
                'https://api.weixin.qq.com/cgi-bin/user/info?access_token={}&openid={}&lang=zh_CN'.format(token, openid),
                json=True
            )

            data = response.json()
            data['nickname'] = data['nickname'].encode('unicode_escape').decode()
            data['tagid_list'] = str(data['tagid_list'])
            print(data)
            if user:
                user.subscribe = data['subscribe']
                user.nickname = data['nickname']                     
                user.sex = data['sex']
                user.language = data['language']
                user.city = data['city']
                user.province = data['province']
                user.country = data['country']
                user.headimgurl = data['headimgurl']
                user.subscribe_time = data['subscribe_time']
                user.remark = data['remark']
                user.groupid = data['groupid']
                user.tagid_list = data['tagid_list']
                user.subscribe_scene = data['subscribe_scene']
                user.qr_scene = data['qr_scene']
                user.qr_scene_str = data['qr_scene_str']
            else:
                user = fancy_list(
                    openid=data['openid'],
                    subscribe=data['subscribe'],
                    nickname=data['nickname'],
                    sex=data['sex'],
                    city=data['city'],
                    country=data['country'],
                    province=data['province'],
                    language=data['language'],
                    headimgurl=data['headimgurl'],
                    subscribe_time=data['subscribe_time'],
                    # data['unionid'],
                    remark=data['remark'],
                    groupid=data['groupid'],
                    tagid_list=data['tagid_list'],
                    subscribe_scene=data['subscribe_scene'],
                    qr_scene=data['qr_scene'],
                    qr_scene_str=data['qr_scene_str']
                )
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify(dict(
                    errcode=2,
                    errmsg='异常错误，请稍后重试',
                ))
            else:
                data['sex'] = '男' if int(data['sex']) == 1 else '女' if int(data['sex']) == 2 else '未知' 
                data['nickname'] = data['nickname'].encode().decode('unicode_escape')
                return jsonify(dict(
                    status=True,
                    data=data
                ))
        else:
            return jsonify(dict(
                status=False,
                errmsg="without openid"
            ))


api.add_resource(menu, '/menu')
api.add_resource(tags, '/tags')
api.add_resource(user_tags, '/user/tags')
api.add_resource(user_remark, '/user/remark')
api.add_resource(user_info, '/user/info')