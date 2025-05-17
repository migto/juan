from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from config import Config

# 因MySQLDB不支持Python3，使用pymysql扩展库代替MySQLDB库
pymysql.install_as_MySQLdb()

# 初始化数据库
db = SQLAlchemy()

def create_app():
    """
    创建Flask应用实例
    :return: Flask应用实例
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # 注册蓝图
    from wxcloudrun.views import bp
    app.register_blueprint(bp)

    return app
