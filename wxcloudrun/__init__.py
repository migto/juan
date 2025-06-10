from flask import Flask
from flask_cors import CORS
import logging
from wxcloudrun.model import db

def create_app():
    """
    创建Flask应用实例
    :return: Flask应用实例
    """
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 初始化日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    # 初始化CORS
    CORS(app)

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    from wxcloudrun.views import bp
    app.register_blueprint(bp)

    return app
