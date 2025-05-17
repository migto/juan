from datetime import datetime
from flask import render_template, request, Blueprint, send_file
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random
import io
from flask_cors import CORS

# 初始化蓝图
bp = Blueprint('api', __name__)
CORS(bp)  # 启用CORS支持

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)

def generate_addition_questions(n):
    """
    生成加法练习题
    :param n: 题目数量
    :return: 题目列表
    """
    questions = []
    for _ in range(min(n, 99)):
        a = random.randint(1, 99)
        b = random.randint(1, 99)
        questions.append(f"{a} + {b} =    ")
    return questions

def create_pdf(questions):
    """
    创建PDF文件
    :param questions: 题目列表
    :return: PDF文件缓冲区
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 30  # 适当边距
    cols = 3
    rows = max(1, (len(questions) + cols - 1) // cols)  # 确保至少1行
    col_width = (width - 2 * margin) / cols
    row_height = (height - 2 * margin) / rows
    font_size = int(row_height * 0.6)  # 字体高度为行高的60%
    c.setFont("Helvetica", font_size)
    x_positions = [margin + i * col_width for i in range(cols)]
    y_start = height - margin
    for idx, q in enumerate(questions):
        col = idx % cols
        row = idx // cols
        x = x_positions[col]
        y = y_start - row * row_height
        c.drawString(x, y, q)
    c.save()
    buffer.seek(0)
    return buffer

@bp.route('/api/preview', methods=['GET'])
def preview_pdf():
    """
    预览PDF
    :return: PDF文件流
    """
    try:
        n = int(request.args.get('n', 99))
        questions = generate_addition_questions(n)
        pdf_buffer = create_pdf(questions)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=False,
            download_name='addition_practice.pdf'
        )
    except Exception as e:
        return make_err_response(str(e))

@bp.route('/api/download', methods=['GET'])
def download_pdf():
    """
    下载PDF
    :return: PDF文件流
    """
    try:
        n = int(request.args.get('n', 99))
        questions = generate_addition_questions(n)
        pdf_buffer = create_pdf(questions)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='addition_practice.pdf'
        )
    except Exception as e:
        return make_err_response(str(e))
