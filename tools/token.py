import ast

import redis, requests, xmltodict

from WeChatServer.config import auth


appinfo = auth.APPINFO

server_api = {
    "token": 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appinfo.get('appID'),appinfo.get('appsecret')),
    "js_ticket": 'None',
    "api_ticket": 'None',
}

class Token():
    _connect_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)
    _t = None  # 存储token或ticket的变量
    _e = None  # 凭证过期时间
    _server_api = dict(
        access_token='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appinfo.get('appID'), appinfo.get('appsecret'))
    )

    @classmethod
    def get_token(cls, key):
        """
        返回方法服务器必须的token值

        :param key: 想要获取的token名称，例如'access_token'
        :return: 需要的token值
        """
        cls._verify(key)
        return cli._t

    
    def _set_access_token(cls, key):
        """
        从服务器获得需要存储的token,并将token/ticket存储到本地的redis中
        其中key为访问的关键字，t为要存储的token/ticket，e为过期时间

        :param key: 需要获得的token名称， 例如'access_token'
        """
        response = requests.get(cls._server_api.get(key))
        response = ast.literal_eval(response.text)
        field = dict(
            t=response.get('access_token'),
            e=response.get('expires_in')+int(time.time())
        )
        redis_cli = redis.StrictRedis(connection_pool=cls._connect_pool)
        redis_cli.hmset(key, field)
        cls._access_token = field.get('t')
        cls._expires_in = field.get('e')

    def _read_access_token(cls, key):
        """
        从本地redis获取想要使用的token/ticket.

        :param key: 想要访问的token/ticket名称，如'access_token'
        """
        redis_cli = redis.StrictRedis(connection_pool=cls._connect_pool)
        t, e = redis_cli.hmget(key, 't', 'e')
        cls.t = t.decode()
        cls.e = int(e.decode())
    
    def _verify(cls, key):
        cls._read_access_token(key)

        if cls._t and cls._e > int(time.time()):
            pass
        
        else:
            cls._set_access_token(key)