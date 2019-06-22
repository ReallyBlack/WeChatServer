from flask import Flask
from .settings import config

from .tools import db
from .api.server_api import token_api
from WeChatServer.api.back_api import admin_api
from .wms import wms

def create_app():
    app = Flask('WeChatServer')
    # 配置数据库信息
    app.config.from_object(config)

    # 注册蓝图及api
    app.register_blueprint(token_api, url_prefix='/api/server/api')  # 服务器端访问接口
    app.register_blueprint(wms, url_prefix='/wms')  # 后台系统蓝图
    app.register_blueprint(admin_api, url_prefix='/api/back/api')  # 后台系统访问接口


    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    return app
