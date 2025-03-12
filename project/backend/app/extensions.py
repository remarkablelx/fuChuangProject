from flask_cors import CORS

# 扩展对象初始化
cors = CORS(resources={r"/api/*": {"origins": "*"}})