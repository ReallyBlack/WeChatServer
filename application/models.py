from passlib.apps import custom_app_context as pwd_context

from WeChatServer.tools.db import db

utf8_2_unicode = lambda s: s.encode().decode('unicode_escape')
str_to_list = lambda s: s.replace("[","").replace("]","").replace("'","").replace('"', '').split(",")


class admin_list(db.Model):
    __tablename__ = 'admin_list'

    id_code = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    mobel = db.Column(db.String(11), nullable=False, unique=True)
    wechat = db.Column(db.String(20))
    nick_name = db.Column(db.String(20))
    # 权限列表:['fancy', 'message', 'article', ... ],拥有的权限在列表中显示，当is_root为true时，不验证该列表
    permission_list = db.Column(db.String(100),default=0)  # 管理员用户权限列表
    is_root = db.Column(db.Boolean, default=False)
    # toekn = db.Column(db.String(100))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    
    def verify_password(self, password):
        """
        验证用户密码
        :param password:请求中携带的用户密码
        :return :如果密码验证正确返回True， 否则返回False
        """
        return pwd_context.verify(password, self.password_hash)
    
    def get_permission_list(self):
        return str_to_list(self.permission_list)


class fancy_list(db.Model):
    __tablename__ = 'fancy_list'

    openid = db.Column(db.String(100), primary_key=True)
    subscribe = db.Column(db.String(1))  # 订阅标识，0为未关注
    nickname = db.Column(db.String(100))  # 用户的昵称
    sex = db.Column(db.String(1))  # 用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
    city = db.Column(db.String(20))  # 用户所在城市
    country = db.Column(db.String(20))  # 用户所在国家
    province = db.Column(db.String(20))  # 用户所在省份
    language = db.Column(db.String(20))  # 用户的语言，简体中文为zh_CN
    headimgurl = db.Column(db.String(200))  
    # 用户头像，最后一个数值代表正方形头像大小
    #（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空。
    # 若用户更换头像，原有头像URL将失效。
    subscribe_time = db.Column(db.String(50))  # 用户关注时间，为时间戳。如果用户曾多次关注，则取最后关注时间
    unionid = db.Column(db.String(100), default='')  # 只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。
    remark = db.Column(db.String(50))  # 公众号运营者对粉丝的备注，公众号运营者可在微信公众平台用户管理界面对粉丝添加备注
    groupid = db.Column(db.String(10))  # 用户所在的分组ID（兼容旧的用户分组接口）
    tagid_list = db.Column(db.String(500))  # 用户被打上的标签ID列表
    subscribe_scene = db.Column(db.String(50))  
    # 返回用户关注的渠道来源，ADD_SCENE_SEARCH 公众号搜索，
    # ADD_SCENE_ACCOUNT_MIGRATION 公众号迁移，ADD_SCENE_PROFILE_CARD 名片分享，
    # ADD_SCENE_QR_CODE 扫描二维码，ADD_SCENEPROFILE LINK 图文页内名称点击，
    # ADD_SCENE_PROFILE_ITEM 图文页右上角菜单，ADD_SCENE_PAID 支付后关注，
    # ADD_SCENE_OTHERS 其他
    qr_scene = db.Column(db.String(50))  # 二维码扫码场景（开发者自定义）
    qr_scene_str = db.Column(db.String(50))  # 二维码扫码场景描述（开发者自定义）
    '''
    def __init__(self, openid, subscribe, nickname, sex, city, country, province, language, headimgurl, subscribe_time, remark, groupid, tagid_list, subscribe_scene, qr_scene, qr_scene_str):
        self.openid = openid
        self.subscribe = subscribe
        self.nickname = nickname
        self.sex = sex
        self.city = city
        self.country = country
        self.province = province
        self.language = language
        self.headimgurl = headimgurl
        self.subscribe_time = subscribe_time
        self.remark = remark
        self.groupid = groupid
        self.tagid_list = tagid_list
        self.subscribe_scene = subscribe_scene
        self.qr_scene = qr_scene
        self.qr_scene_str = qr_scene_str
    '''
    def get_nickname(self):
        return utf8_2_unicode(self.nickname)