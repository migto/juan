# 创建应用实例
import sys
import os

from wxcloudrun import create_app

app = create_app()

# 启动Flask Web服务
if __name__ == '__main__':
    # 仅在本地开发时使用Flask开发服务器
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(host='0.0.0.0', port=801, debug=True)
    else:
        # 生产环境提示
        print("生产环境请使用 gunicorn 启动，如: gunicorn run:app")
