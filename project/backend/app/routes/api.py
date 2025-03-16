# api.py
# 作用:定义API相关路由
# 当前状态：仅有一个测试接口/api/frames

import os
import re
from flask import Blueprint, jsonify,request
from flask_cors import cross_origin
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



@api_bp.route('/password_login', methods=['POST'])
def login():
    data = request.get_json()

    # 基础参数校验
    if not data or 'phone' not in data or 'type' not in data:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400

    phone = data['phone']
    login_type = data['type']

    # 手机号格式验证
    if not re.match(r'^(?:(?:\+|00)86)?1[3-9]\d{9}$', phone):
        return jsonify({'success': False, 'message': '手机号格式错误'}), 400

    # 密码登录逻辑
    if login_type == 'password':
        if 'password' not in data:
            return jsonify({'success': False, 'message': '缺少密码参数'}), 400

        # 模拟数据库验证（正式环境需替换为真实查询）
        if phone == "13812345678" and data['password'] == "password123":
            return jsonify({'success': True, 'message': '登录成功'})
        else:
            return jsonify({'success': False, 'message': '手机号或密码错误'}), 401

    # 验证码登录逻辑
    elif login_type == 'sms':
        if 'sms_code' not in data:
            return jsonify({'success': False, 'message': '缺少验证码参数'}), 400

        # 模拟验证码验证（正式环境需替换为缓存/数据库查询）
        if data['sms_code'] == "123456":
            return jsonify({'success': True, 'message': '登录成功'})
        else:
            return jsonify({'success': False, 'message': '验证码错误'}), 401

    else:
        return jsonify({'success': False, 'message': '无效的登录类型'}), 400

@api_bp.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    phone = data.get('phone')

    # 手机号格式验证
    if not re.match(r'^(?:(?:\+|00)86)?1[3-9]\d{9}$', phone):
        return jsonify({'success': False, 'message': '手机号格式错误'}), 400

    # 模拟发送验证码（正式环境需接入短信服务商API）
    print(f"模拟发送验证码至 {phone}: 123456")  # 控制台输出模拟验证码
    return jsonify({'success': True, 'message': '验证码已发送'})