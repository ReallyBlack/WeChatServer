from WeChatServer.tools.db import db


class admin_list(db.Model):
    __tablename__ = 'admin_list'

    id_code = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    salt_password = db.Column(db.String(100), nullable=False)
    phone_num = db.Column(db.String(11), nullable=False)
    wechat = db.Column(db.String(20))
    nick_name = db.Column(db.String(20))
    permission_user = db.Column(db.Boolean, default=False)
    permission_message = db.Column(db.Boolean, default=False)
    permission_article = db.Column(db.Boolean, default=False)
    is_root = db.Column(db.Boolean, default=False)
    toekn = db.Column(db.String(100))