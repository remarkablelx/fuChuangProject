# 作用:导出API和静态文件路由蓝图
# 说明:作为路由模块的入口文件,集中管理所有路由蓝图

from .api import api_bp
from .static import static_bp

__all__ = ['api_bp', 'static_bp']