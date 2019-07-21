import requests
import xmltodict

from .db import db
from .token import Token
from WeChatServer.application.models import fancy_list

unicode_2_utf8 = lambda s: s.encode('unicode_escape').decode('utf-8')


def create_or_update_fancy(openid):
    '''
    创建或更新粉丝信息
    用于用户订阅公众号时存储用户信息或手动更新用户信息时执行刷新操作
    :param openid:被创建或更新的粉丝对于公众号指定的ID码
    :return :正常返回True，错误返回False
    '''
    user = fancy_list.query.filter_by(openid=openid).first()
    token = Token.get_token('access_token')
    data = requests.get('https://api.weixin.qq.com/cgi-bin/user/info?access_token={}&openid={}&lang=zh_CN'.format(token, openid)).json()
    data['nickname'] = unicode_2_utf8(data['nickname'])
    data['tagid_list'] = str(data['tagid_list'])
    if user:
        user.subscribe = data['subscribe']
        user.nickname = unicode_2_utf8(data['nickname'])                     
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
            nickname=unicode_2_utf8(data['nickname']),
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
        return False
    else:
        return True