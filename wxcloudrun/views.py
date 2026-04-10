from flask import Blueprint, request, send_file, jsonify
import base64
import os
import uuid
from datetime import datetime
from pdf2docx import Converter

# 创建蓝图
api = Blueprint('api', __name__)

# 配置
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

@api.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "service": "PDF转Word",
        "timestamp": datetime.now().isoformat()
    })

@api.route('/convert/base64', methods=['POST'])
def convert_pdf_base64():
    """
    Base64格式的PDF转Word接口
    """
    try:
        data = request.get_json()
        
        if 'pdf_base64' not in data:
            return jsonify({"error": "缺少 'pdf_base64' 字段"}), 400
        
        pdf_base64 = data['pdf_base64']
        filename = data.get('filename', 'document.pdf')
        
        # 解码Base64
        try:
            pdf_bytes = base64.b64decode(pdf_base64)
        except Exception as e:
            return jsonify({"error": f"Base64解码失败: {str(e)}"}), 400
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = os.path.splitext(filename)[0]
        
        pdf_path = os.path.join(UPLOAD_DIR, f"{file_id}_{timestamp}.pdf")
        word_path = os.path.join(OUTPUT_DIR, f"{file_id}_{timestamp}.docx")
        
        # 保存PDF文件
        with open(pdf_path, 'wb') as f:
            f.write(pdf_bytes)
        
        # 执行转换
        cv = Converter(pdf_path)
        cv.convert(word_path, layout_mode='raw')
        cv.close()
        
        # 返回Word文件
        return send_file(
            word_path,
            as_attachment=True,
            download_name=f"{original_name}.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        return jsonify({"error": f"转换失败: {str(e)}"}), 500
