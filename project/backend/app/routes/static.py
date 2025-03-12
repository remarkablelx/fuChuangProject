# 作用：处理静态文件请求
# 当前状态：主要服务前端资源文件

from flask import Blueprint, send_from_directory
from ..config import BaseConfig

static_bp = Blueprint('static', __name__)

@static_bp.route('/')
@static_bp.route('/<path:path>')
def serve_frontend(path=''):
    return send_from_directory(BaseConfig.STATIC_FOLDER, 'index.html')

@static_bp.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(f'{BaseConfig.STATIC_FOLDER}/assets', filename)

@static_bp.route('/frame/<path:filename>')
def serve_frames(filename):
    """服务帧图片文件"""
    return send_from_directory(
        BaseConfig.FRAME_FOLDER,  # 使用专用帧目录
        filename
    )