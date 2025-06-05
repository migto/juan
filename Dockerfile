FROM python:3.10-slim

WORKDIR /app

# 优化构建速度：先复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 80

# 使用Gunicorn作为生产环境WSGI服务器
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "4", "--timeout", "120", "run:app"]