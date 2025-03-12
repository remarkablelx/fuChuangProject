# 服务外包项目（后端文件）

[![Flask](https://img.shields.io/badge/Flask-2.0.x-blue)](https://flask.palletsprojects.com/)
[![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen)](https://vuejs.org/)

## 技术栈

**后端服务**  
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0.x-blue?logo=flask)
![Flask-CORS](https://img.shields.io/badge/Flask--CORS-3.0.x-lightgrey)

**前端服务**  
![Vue3](https://img.shields.io/badge/Vue-3.x-brightgreen?logo=vue.js)
![Vite](https://img.shields.io/badge/Vite-4.x-purple?logo=vite)
![Axios](https://img.shields.io/badge/Axios-1.x-blueviolet)

### 🌐 API 开发    
1. **添加新路由**
  文件：`app/routes/api.py`
  ```python
# 简单GET示例
@api_bp.route('/test', methods=['GET'])
def test_api():
    return jsonify({"status": "ok"})

# 带参数POST示例
@api_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')  # 获取上传文件
    return jsonify({"filename": file.filename})
  ```
2. **处理请求参数**
  文件：`app/routes/api.py`
  ```python
from flask import request

# Query参数示例
@api_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('q')  # 获取?q=xxx
    return jsonify({"result": keyword})

# JSON参数示例
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.json  # 获取JSON body
    username = data.get('username')
    return jsonify({"user": username})
  ```
3. **错误处理**
  文件：`app/errors.py`
  ```python
@api_bp.errorhandler(404)
def handle_404(error):
    return jsonify({"error": "Not found"}), 404
  ```
4. **测试API**
  ```bash
# bash
# GET测试
curl http://localhost:5000/api/test

# POST测试
curl -X POST -F "file=@test.jpg" http://localhost:5000/api/upload
  ```
### 🔧 测试方法
