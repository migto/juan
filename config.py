import os

class Config:
    # 是否开启debug模式
    DEBUG = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/flask_demo'.format(
        os.environ.get("MYSQL_USERNAME", 'root'),
        os.environ.get("MYSQL_PASSWORD", 'root'),
        os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        os.environ.get("MYSQL_USERNAME"),
        os.environ.get("MYSQL_PASSWORD"),
        os.environ.get("MYSQL_ADDRESS"),
        os.environ.get("MYSQL_DATABASE", 'flask_app')
    )
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key'
    LOG_LEVEL = 'INFO'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
