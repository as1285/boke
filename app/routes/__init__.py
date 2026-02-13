# -*- coding: utf-8 -*-
"""
路由包初始化文件
注册所有蓝图路由
"""

from flask import Blueprint

# 创建主蓝图
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 导入路由模块（放在最后避免循环导入）
from . import main, auth, admin
