# -*- coding: utf-8 -*-
"""
博客系统配置文件
包含开发环境和生产环境的配置
"""

import os
from datetime import timedelta

# 获取项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    基础配置类
    包含所有环境通用的配置项
    """
    # 密钥配置（用于session、CSRF等）
    # 生产环境应使用更复杂的随机字符串
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # 分页配置
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 20
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大16MB
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Session配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # 管理员邮箱列表
    ADMIN_EMAILS = ['admin@example.com']
    
    @staticmethod
    def init_app(app):
        """
        初始化应用配置
        可以在这里添加日志配置等
        """
        pass


class DevelopmentConfig(Config):
    """
    开发环境配置
    启用调试模式，使用本地MySQL数据库
    """
    DEBUG = True
    
    # 开发环境数据库配置
    # 已配置为本地MySQL数据库
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '3306'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or '123456'
    DB_NAME = os.environ.get('DB_NAME') or 'flask_blog'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'


class ProductionConfig(Config):
    """
    生产环境配置
    关闭调试模式，使用生产环境数据库
    """
    DEBUG = False
    
    # 生产环境数据库配置（建议通过环境变量设置）
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:password@localhost:3306/flask_blog?charset=utf8mb4'
    
    # 生产环境使用更严格的session配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """
    测试环境配置
    使用内存数据库，便于快速测试
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    POSTS_PER_PAGE = 5


# 配置映射字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
