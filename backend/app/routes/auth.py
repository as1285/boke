# -*- coding: utf-8 -*-
"""
用户认证路由
"""

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.models import User, LoginLog
from app.schemas import UserSchema, UserLoginSchema

auth_bp = Blueprint('auth', __name__)

user_schema = UserSchema()
login_schema = UserLoginSchema()


def api_response(code=200, msg='操作成功', data=None):
    """统一API响应格式"""
    return {'code': code, 'msg': msg, 'data': data}


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    json_data = request.get_json()
    if not json_data:
        return api_response(400, '无效的请求数据'), 400
    
    try:
        # 验证数据
        data = user_schema.load(json_data)
        
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=data['username']).first():
            return api_response(400, '用户名已存在'), 400
        if User.query.filter_by(email=data['email']).first():
            return api_response(400, '邮箱已存在'), 400
        
        # 创建用户
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # 生成Token（identity必须是字符串）
        access_token = create_access_token(identity=str(user.id))
        
        return api_response(200, '注册成功', {
            'token': access_token,
            'user': user.to_dict()
        })
        
    except ValidationError as err:
        return api_response(400, '数据验证失败', err.messages), 400
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'注册失败: {str(e)}'), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    json_data = request.get_json()
    if not json_data:
        return api_response(400, '无效的请求数据'), 400
    
    try:
        data = login_schema.load(json_data)
        
        # 查找用户
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return api_response(400, '用户名或密码错误'), 400
        
        if not user.is_active:
            return api_response(400, '账户已被禁用'), 400
        
        # 更新最后登录时间
        user.last_seen = db.func.now()
        
        # 生成Token（identity必须是字符串）
        access_token = create_access_token(identity=str(user.id))
        
        # 记录登录日志
        login_log = LoginLog(
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None,
            login_type='password',
            login_status='success'
        )
        db.session.add(login_log)
        db.session.commit()
        
        return api_response(200, '登录成功', {
            'token': access_token,
            'user': user.to_dict()
        })
        
    except ValidationError as err:
        return api_response(400, '数据验证失败', err.messages), 400
    except Exception as e:
        return api_response(500, f'登录失败: {str(e)}'), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户退出（前端清除Token即可）"""
    return api_response(200, '退出成功')


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前登录用户信息"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return api_response(401, '用户不存在'), 401
    
    return api_response(200, '获取成功', user.to_dict())
