from flask import Flask, request
from WeChatServer.settings import config

from WeChatServer.api.server_api import token_api
from WeChatServer.api.back_api import admin_api
from WeChatServer.api.v0_1 import cgi_api
from WeChatServer.tools import verify, db
from WeChatServer.application import server


def create_app():
    app = Flask('WeChatServer')
    # 配置数据库信息
    app.config.from_object(config)

    # 注册蓝图及api
    app.register_blueprint(token_api, url_prefix='/api/server/api')  # 服务器端访问接口
    app.register_blueprint(server, url_prefix='/server')  # 后台系统蓝图
    app.register_blueprint(admin_api, url_prefix='/api/back/api')  # 后台系统访问接口
    # 注册cgi，版本v0.1
    app.register_blueprint(cgi_api, url_prefix='/api/v0.1/cgi-bin')


    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    @verify.isServer
    def index(echostr, code):
        if request.method == 'GET':
            # todo:返回给服务器特定的响应认证
            return echostr
        elif request.method == 'POST':
            # todo:根据响应类型进行特定的响应处理
            # 1.验证消息来源，如果是来自微信服务器，则对数据进行处理
            if code:
                # todo:
                return "code:200"
            # 2.如果消息不是来自微信服务器，则返回错误码
            return "code: 503"
        else:
            # todo:反正错误响应代码
            return "code:404"

    return app
