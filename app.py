from flask import Flask, request

from tools import verify

app = Flask(__name__)



@app.route('/')
@verify.isServer
def index(echostr):
    if request.method == 'GET':
        # todo:返回给服务器特定的响应认证
        print(echostr)
        return "code:200"
    elif request.method == 'POST':
        # todo:根据响应类型进行特定的响应处理
        return "code:202"
    else:
        # todo:反正错误响应代码
        return "code:404"


if __name__ == "__main__":
    app.run()
