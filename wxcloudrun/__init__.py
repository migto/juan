from flask import Flask
# from config import Config

def create_app():
    """
    创建Flask应用实例
    :return: Flask应用实例
    """
    app = Flask(__name__)
    # app.config.from_object(Config)

    # 注册蓝图
    from wxcloudrun.views import bp
    app.register_blueprint(bp)

    return app
