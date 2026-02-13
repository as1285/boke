# -*- coding: utf-8 -*-
"""
应用包初始化文件
创建Flask应用实例，初始化扩展和注册蓝图
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# 初始化扩展（先创建实例，稍后绑定到应用）
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name='default'):
    """
    应用工厂函数
    创建并配置Flask应用实例
    
    Args:
        config_name: 配置环境名称（development/production/testing）
        
    Returns:
        Flask: 配置好的Flask应用实例
    """
    from config import config
    
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # 配置登录管理器
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录以访问此页面。'
    login_manager.login_message_category = 'info'
    
    # 注册蓝图
    from app.routes import main_bp, auth_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    # 注册模板过滤器
    from app.utils import markdown_filter, timesince_filter
    app.add_template_filter(markdown_filter, 'markdown')
    app.add_template_filter(timesince_filter, 'timesince')
    
    # 创建数据库表（仅在开发环境）
    with app.app_context():
        # 导入模型以确保表被创建
        from app.models import User, Post, Category, Tag, Comment
        db.create_all()
    
    return app


# 用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    """
    根据用户ID加载用户对象
    用于Flask-Login管理用户会话
    
    Args:
        user_id: 用户ID
        
    Returns:
        User: 用户对象
    """
    from app.models import User
    return User.query.get(int(user_id))
