# 创建应用实例
import sys

from wxcloudrun import create_app

app = create_app()

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
