# 创建应用实例
import sys
import os

from wxcloudrun import app

# 创建上传和输出目录
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 导入PDF转换路由
from views import api
app.register_blueprint(api, url_prefix='/api')

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
