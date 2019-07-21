import xmltodict
import requests

from .func_tools import create_or_update_fancy

def event(request):
    data = xmltodict.parse(str(request.data, encoding='utf-8'))['xml']
    if data['MsgType'] == 'event':
        # 用户关注事件
        if data['Event'] == 'subscribe':
            openid = data['FromUserName']
            # 关注成功，执行关注后的推送事件
            if create_or_update_fancy(openid):
                print("有人关注，openid：{}".format(openid))
                pass
            pass
        pass
    pass