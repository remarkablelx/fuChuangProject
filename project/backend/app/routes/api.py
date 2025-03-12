# 作用:定义API相关路由
# 当前状态：仅有一个测试接口/api/frames

from flask import Blueprint, jsonify
import os
from ..config import BaseConfig

api_bp = Blueprint('api', __name__)


@api_bp.route('/frames')
def get_frames():
    """获取所有帧数据接口"""
    frame_dir = os.path.join(BaseConfig.FRAME_FOLDER)

    try:
        files = sorted([
            f for f in os.listdir(frame_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])
    except FileNotFoundError:
        return jsonify({"error": "帧目录不存在"}), 404

    return jsonify({
        "total": len(files),
        "prefix": "/frame/",  # 与静态路由一致
        "files": files,
        "fps": 30
    })