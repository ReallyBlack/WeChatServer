from .config import settings

SQL = settings.SQL.get('back_sql')


class config():
    SECRET_KEY = "saldifwnk23425@!#!kfa"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = '{}+pymysql://{}:{}@{}:{}/{}'.format(
        SQL.get('sql').lower(),
        SQL.get('user'),
        SQL.get('password'),
        SQL.get('host'),
        SQL.get('port'),
        SQL.get('db')
    )