# -*- coding: utf-8 -*-
"""
模型包初始化文件
导出所有模型类，方便其他模块导入
"""

# 延迟导入，避免循环引用
def get_user_model():
    from .user import User
    return User

def get_post_model():
    from .post import Post
    return Post

def get_category_model():
    from .post import Category
    return Category

def get_tag_model():
    from .post import Tag
    return Tag

def get_comment_model():
    from .comment import Comment
    return Comment

# 为了兼容性，仍然导出类（在应用上下文中有）
try:
    from .user import User
    from .post import Post, Category, Tag, post_tags
    from .comment import Comment
except ImportError:
    # 如果导入失败（循环引用），使用延迟导入
    pass

__all__ = ['User', 'Post', 'Category', 'Tag', 'Comment', 'post_tags']
