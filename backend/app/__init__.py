# -*- coding: utf-8 -*-
"""
Flask应用初始化
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()


def create_app(config_name='default'):
    """应用工厂函数"""
    from app.config import config
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    
    # 配置CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', '*'),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.posts import posts_bp
    from app.routes.tags import tags_bp
    from app.routes.comments import comments_bp
    from app.routes.admin import admin_bp
    from app.routes.tech import tech_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(posts_bp, url_prefix='/api')
    app.register_blueprint(tags_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(tech_bp, url_prefix='/api')
    
    # 注册日志中间件
    from app.utils.logger import APILogger
    app.before_request(APILogger.before_request)
    app.after_request(APILogger.after_request)
    
    # 创建数据库表并初始化数据
    with app.app_context():
        from app.models import User, Post, Category, Tag, Comment, APILog, TestTechResource, init_test_tech_resources, LoginLog
        db.create_all()
        # 初始化测试技术资源数据
        init_test_tech_resources()
    
    # JWT错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'code': 401, 'msg': 'Token已过期', 'data': None}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'code': 401, 'msg': '无效的Token', 'data': None}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'code': 401, 'msg': '缺少Token', 'data': None}, 401
    
    # 全局错误处理
    @app.errorhandler(404)
    def not_found(error):
        return {'code': 404, 'msg': '资源不存在', 'data': None}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'code': 500, 'msg': '服务器内部错误', 'data': None}, 500
    
    return app
