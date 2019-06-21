from flask import request

from WeChatServer.wms.models import admin
from WeChatServer.tools import verify
from WeChatServer import create_app

app = create_app()

@app.route('/')
@verify.isServer
def index(echostr, code):
    if request.method == 'GET':
        # todo:返回给服务器特定的响应认证
        if code:
            return echostr
        else:
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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
