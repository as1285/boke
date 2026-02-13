# -*- coding: utf-8 -*-
"""
应用启动入口
用于启动Flask开发服务器
"""

import os
from app import create_app, db
from app.models import User, Post, Category, Tag, Comment

# 创建应用实例（使用开发环境配置）
app = create_app(os.getenv('FLASK_CONFIG') or 'development')


@app.shell_context_processor
def make_shell_context():
    """
    配置Flask Shell上下文
    方便在命令行中操作数据库模型
    """
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Category': Category,
        'Tag': Tag,
        'Comment': Comment
    }


if __name__ == '__main__':
    # 启动开发服务器
    # host='0.0.0.0' 允许外部访问
    # debug=True 启用调试模式（开发环境）
    app.run(host='0.0.0.0', port=5000, debug=True)
