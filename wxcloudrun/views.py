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

COUNT_LEVEL_MAP = {1: 33, 2: 66, 3: 99}
DIFFICULTY_MAP = {
    1: {'min': 1, 'max': 20, 'ops': ['+']},
    2: {'min': 1, 'max': 20, 'ops': ['+', '-']},
    3: {'min': 1, 'max': 99, 'ops': ['+']},
    4: {'min': 1, 'max': 99, 'ops': ['+', '-']}
}

# 生成加减法题目

def generate_math_questions(count, difficulty):
    cfg = DIFFICULTY_MAP[difficulty]
    questions = []
    for _ in range(count):
        op = random.choice(cfg['ops'])
        a = random.randint(cfg['min'], cfg['max'])
        b = random.randint(cfg['min'], cfg['max'])
        if op == '-':
            if a < b:
                a, b = b, a
        # 补空格对齐，保证每个数字宽度为2
        q = f"{str(a).rjust(2)} {op} {str(b).rjust(2)} =    "
        questions.append(q)
    return questions

# 动态排版生成PDF

def create_pdf(questions):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 30  # 页边距
    cols = 3
    total = len(questions)
    rows = total // cols
    max_font_size = 36
    min_font_size = 10
    font_name = "Courier"
    # 动态调整字体大小，保证三列不重叠且间距达标
    for font_size in range(max_font_size, min_font_size - 1, -1):
        c.setFont(font_name, font_size)
        sample_q = "99 + 99 =    "
        q_width = c.stringWidth(sample_q, font_name, font_size)
        min_col_gap = q_width / 3
        total_width = 3 * q_width + 2 * min_col_gap
        if total_width <= (width - 2 * margin):
            break
    else:
        font_size = min_font_size
        c.setFont(font_name, font_size)
        q_width = c.stringWidth(sample_q, font_name, font_size)
        min_col_gap = q_width / 3
        total_width = 3 * q_width + 2 * min_col_gap
    # 居中排布
    left = margin + ((width - 2 * margin) - total_width) / 2
    x_positions = [left + i * (q_width + min_col_gap) for i in range(cols)]
    row_height = (height - 2 * margin) / rows
    y_start = height - margin
    # 按列优先分布
    for col in range(cols):
        for row in range(rows):
            idx = col * rows + row
            if idx >= total:
                break
            x = x_positions[col]
            y = y_start - row * row_height
            c.drawString(x, y, questions[idx])
    c.save()
    buffer.seek(0)
    return buffer

# 参数解析和校验

def parse_params():
    count_level = request.args.get('count_level', '3')
    difficulty = request.args.get('difficulty', '4')
    if not count_level.isdigit() or int(count_level) not in COUNT_LEVEL_MAP:
        return None, None, make_err_response('参数 count_level 必须为1、2或3', code=400)
    if not difficulty.isdigit() or int(difficulty) not in DIFFICULTY_MAP:
        return None, None, make_err_response('参数 difficulty 必须为1、2、3或4', code=400)
    return int(count_level), int(difficulty), None

@bp.route('/api/preview', methods=['GET'])
def preview_pdf():
    """
    预览PDF
    :return: PDF文件流
    """
    try:
        count_level, difficulty, err = parse_params()
        if err:
            return err
        count = COUNT_LEVEL_MAP[count_level]
        questions = generate_math_questions(count, difficulty)
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
        count_level, difficulty, err = parse_params()
        if err:
            return err
        count = COUNT_LEVEL_MAP[count_level]
        questions = generate_math_questions(count, difficulty)
        pdf_buffer = create_pdf(questions)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='addition_practice.pdf'
        )
    except Exception as e:
        return make_err_response(str(e))
