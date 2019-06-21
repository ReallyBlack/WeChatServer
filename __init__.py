from flask import Flask
from .settings import config

from .tools import verify, db
from .api.server_api import token_api
from .wms import wms

def create_app():
    app = Flask('WeChatServer')
    # 配置数据库信息
    app.config.from_object(config)

    # 注册蓝图信息
    app.register_blueprint(token_api, url_prefix='/api/server/api')
    app.register_blueprint(wms, url_prefix='/wms')

    return app