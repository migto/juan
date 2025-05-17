from flask import Blueprint, request, send_file
from wxcloudrun.response import make_succ_response, make_err_response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random
import io
from flask_cors import CORS

# 初始化蓝图
bp = Blueprint('api', __name__)
CORS(bp)  # 启用CORS支持

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
