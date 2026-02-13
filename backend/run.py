# -*- coding: utf-8 -*-
"""
后端启动入口
"""

import os
from app import create_app, db
from app.models import User, Post, Category, Tag, Comment

app = create_app(os.getenv('FLASK_CONFIG') or 'development')


@app.shell_context_processor
def make_shell_context():
    """Flask Shell上下文"""
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Category': Category,
        'Tag': Tag,
        'Comment': Comment
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
