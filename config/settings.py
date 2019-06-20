# in this file, write some config of the server


# write you sql in the attr. 
# please don't change the keys name
# the second key of sql is the name of your sql with title type
# like "Redis", "MongoDB", "Oracle", "MySQL" eg.
SQL = {
    # "server_sql": "to save some token information, default use redis",
    # "back_sql": "to save some information what the user sent to you server, default use mysql"
    "server_sql": {
        "sql": 'Redis',
        "host": '127.0.0.1',
        "post": 6379,
        "db": 8,
        "uesr": '',
        "password": '',
    },
    "back_sql": {
        "sql": 'MySQL',
        "host": '60.205.223.23',
        "post": 3306,
        "db": "WeChat",
        "user": "wechat",
        "password": "wechat",
    }
}