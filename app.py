from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    if request.methods == 'GET':
        # todo:返回给服务器特定的响应认证
    elif request.methods == 'POST':
        # todo:根据响应类型进行特定的响应处理
    else:
        # todo:反正错误响应代码
 

if __name__ == "__main__":
    app.run()
