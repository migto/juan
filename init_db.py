from wxcloudrun import create_app
from wxcloudrun.model import db

app = create_app()
with app.app_context():
    db.create_all()
    print('数据库表结构初始化完成') 