# -*- coding: utf-8 -*-
"""
创建测试文章脚本
"""

import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import User, Post, Category, Tag

app = create_app()

with app.app_context():
    # 创建管理员用户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✓ 创建管理员用户: admin / admin123")
    
    # 创建分类
    category = Category.query.filter_by(name='技术').first()
    if not category:
        category = Category(name='技术', description='技术文章')
        db.session.add(category)
        db.session.commit()
        print("✓ 创建分类: 技术")
    
    # 创建标签
    tag = Tag.query.filter_by(name='Python').first()
    if not tag:
        tag = Tag(name='Python')
        db.session.add(tag)
        db.session.commit()
        print("✓ 创建标签: Python")
    
    # 创建测试文章
    post = Post.query.filter_by(title='欢迎使用 Flask + Vue 博客系统').first()
    if not post:
        post = Post(
            title='欢迎使用 Flask + Vue 博客系统',
            content='''# 欢迎使用 Flask + Vue 博客系统

这是一个基于 **Flask** 和 **Vue 3** 开发的前后端分离博客系统。

## 功能特性

- ✅ 用户注册、登录、JWT认证
- ✅ 文章发布、编辑、删除
- ✅ Markdown编辑器支持
- ✅ 文章分类和标签
- ✅ 评论系统
- ✅ 响应式设计

## 技术栈

### 后端
- Flask 3.0
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Marshmallow

### 前端
- Vue 3 + Vite
- Element Plus
- mavon-editor
- Pinia

## 开始使用

1. 注册账号
2. 登录系统
3. 在后台管理创建文章
4. 使用Markdown编写内容

> 这是一个引用示例

```python
print("Hello, World!")
```

**加粗文本** 和 *斜体文本*

- 列表项1
- 列表项2
- 列表项3

[链接示例](http://localhost:5174/)
''',
            content_html='<h1>欢迎使用 Flask + Vue 博客系统</h1><p>这是一个基于 <strong>Flask</strong> 和 <strong>Vue 3</strong> 开发的前后端分离博客系统。</p>',
            summary='这是一个基于 Flask 和 Vue 3 开发的前后端分离博客系统，支持Markdown编辑、文章管理、评论等功能。',
            user_id=admin.id,
            category_id=category.id,
            is_published=True
        )
        post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        print("✓ 创建测试文章")
    
    print("\n" + "="*50)
    print("初始化完成！")
    print("="*50)
    print("\n管理员账号: admin / admin123")
    print("访问地址: http://localhost:5174/")
    print("\n后台管理: http://localhost:5174/admin")
