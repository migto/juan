import os

class Config:
    # 是否开启debug模式
    DEBUG = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/flask_demo'.format(
        os.environ.get("MYSQL_USERNAME", 'root'),
        os.environ.get("MYSQL_PASSWORD", 'root'),
        os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
