# -*- coding: utf-8 -*-
"""
管理后台路由 - 日志、接口文档、用户管理
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from app import db
from app.models import User, APILog, LoginLog
from app.schemas import UserSchema

admin_bp = Blueprint('admin', __name__)

user_schema = UserSchema()


def api_response(code=200, msg='操作成功', data=None):
    """统一API响应格式"""
    return {'code': code, 'msg': msg, 'data': data}


def check_admin():
    """检查是否为管理员"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    return user and user.is_admin


# ==================== 日志模块 ====================

@admin_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    """获取API调用日志（仅管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    method = request.args.get('method')  # 按HTTP方法筛选
    status_code = request.args.get('status_code', type=int)  # 按状态码筛选
    user_id = request.args.get('user_id', type=int)  # 按用户筛选
    
    query = APILog.query
    
    if method:
        query = query.filter_by(method=method.upper())
    if status_code:
        query = query.filter_by(status_code=status_code)
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    pagination = query.order_by(APILog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    logs = [log.to_dict() for log in pagination.items]
    
    return api_response(200, '获取成功', {
        'items': logs,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@admin_bp.route('/logs/stats', methods=['GET'])
@jwt_required()
def get_logs_stats():
    """获取日志统计（仅管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    # 总请求数
    total_requests = APILog.query.count()
    
    # 今日请求数
    from datetime import datetime, timedelta
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_requests = APILog.query.filter(APILog.created_at >= today).count()
    
    # 按HTTP方法统计
    method_stats = db.session.query(
        APILog.method,
        func.count(APILog.id).label('count')
    ).group_by(APILog.method).all()
    
    # 按状态码统计
    status_stats = db.session.query(
        APILog.status_code,
        func.count(APILog.id).label('count')
    ).group_by(APILog.status_code).all()
    
    # 平均响应时间
    avg_response_time = db.session.query(func.avg(APILog.response_time)).scalar() or 0
    
    return api_response(200, '获取成功', {
        'total_requests': total_requests,
        'today_requests': today_requests,
        'method_stats': [{'method': m.method, 'count': m.count} for m in method_stats],
        'status_stats': [{'status_code': s.status_code, 'count': s.count} for s in status_stats],
        'avg_response_time': round(avg_response_time, 4)
    })


# ==================== 接口文档模块 ====================

@admin_bp.route('/api-docs', methods=['GET'])
@jwt_required()
def get_api_docs():
    """获取博客接口文档（仅管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    api_docs = {
        'auth': {
            'name': '用户认证模块',
            'description': '用户注册、登录、认证相关接口',
            'endpoints': [
                {
                    'method': 'POST',
                    'path': '/api/auth/register',
                    'name': '用户注册',
                    'description': '注册新用户账号',
                    'params': {
                        'username': '用户名（3-20字符）',
                        'email': '邮箱地址',
                        'password': '密码（至少6位）'
                    },
                    'response': {
                        'token': 'JWT Token',
                        'user': '用户信息'
                    },
                    'permission': '公开'
                },
                {
                    'method': 'POST',
                    'path': '/api/auth/login',
                    'name': '用户登录',
                    'description': '用户登录获取Token',
                    'params': {
                        'username': '用户名',
                        'password': '密码'
                    },
                    'response': {
                        'token': 'JWT Token',
                        'user': '用户信息'
                    },
                    'permission': '公开'
                },
                {
                    'method': 'GET',
                    'path': '/api/auth/me',
                    'name': '获取当前用户',
                    'description': '获取当前登录用户信息',
                    'params': {},
                    'response': '用户信息对象',
                    'permission': '登录用户'
                }
            ]
        },
        'posts': {
            'name': '文章模块',
            'description': '文章发布、编辑、查询相关接口',
            'endpoints': [
                {
                    'method': 'GET',
                    'path': '/api/posts',
                    'name': '文章列表',
                    'description': '获取文章列表，支持分页、搜索、筛选',
                    'params': {
                        'page': '页码（默认1）',
                        'per_page': '每页数量（默认10）',
                        'keyword': '搜索关键词',
                        'category_id': '分类ID筛选',
                        'tag_id': '标签ID筛选'
                    },
                    'response': '文章列表（含分页信息）',
                    'permission': '公开'
                },
                {
                    'method': 'GET',
                    'path': '/api/posts/{slug}',
                    'name': '文章详情',
                    'description': '获取单篇文章详情',
                    'params': {
                        'slug': '文章slug'
                    },
                    'response': '文章详情（含内容）',
                    'permission': '公开'
                },
                {
                    'method': 'POST',
                    'path': '/api/posts',
                    'name': '创建文章',
                    'description': '创建新文章',
                    'params': {
                        'title': '文章标题',
                        'content': 'Markdown内容',
                        'summary': '文章摘要',
                        'is_published': '是否发布',
                        'category_id': '分类ID',
                        'tag_ids': '标签ID数组'
                    },
                    'response': '创建的文章信息',
                    'permission': '管理员'
                },
                {
                    'method': 'PUT',
                    'path': '/api/posts/{id}',
                    'name': '更新文章',
                    'description': '更新文章信息',
                    'params': {
                        'title': '文章标题（可选）',
                        'content': 'Markdown内容（可选）',
                        'summary': '文章摘要（可选）',
                        'is_published': '是否发布（可选）'
                    },
                    'response': '更新后的文章信息',
                    'permission': '管理员'
                },
                {
                    'method': 'DELETE',
                    'path': '/api/posts/{id}',
                    'name': '删除文章',
                    'description': '删除文章',
                    'params': {},
                    'response': '删除成功消息',
                    'permission': '管理员'
                }
            ]
        },
        'categories': {
            'name': '分类/标签模块',
            'description': '文章分类和标签管理',
            'endpoints': [
                {
                    'method': 'GET',
                    'path': '/api/categories',
                    'name': '分类列表',
                    'description': '获取所有分类',
                    'params': {},
                    'response': '分类列表',
                    'permission': '公开'
                },
                {
                    'method': 'GET',
                    'path': '/api/tags',
                    'name': '标签列表',
                    'description': '获取所有标签',
                    'params': {},
                    'response': '标签列表',
                    'permission': '公开'
                },
                {
                    'method': 'POST',
                    'path': '/api/categories',
                    'name': '创建分类',
                    'description': '创建新分类',
                    'params': {
                        'name': '分类名称',
                        'description': '分类描述'
                    },
                    'response': '创建的分类信息',
                    'permission': '管理员'
                },
                {
                    'method': 'POST',
                    'path': '/api/tags',
                    'name': '创建标签',
                    'description': '创建新标签',
                    'params': {
                        'name': '标签名称'
                    },
                    'response': '创建的标签信息',
                    'permission': '管理员'
                }
            ]
        },
        'comments': {
            'name': '评论模块',
            'description': '文章评论相关接口',
            'endpoints': [
                {
                    'method': 'GET',
                    'path': '/api/posts/{id}/comments',
                    'name': '评论列表',
                    'description': '获取文章评论列表',
                    'params': {
                        'page': '页码',
                        'per_page': '每页数量'
                    },
                    'response': '评论列表',
                    'permission': '公开'
                },
                {
                    'method': 'POST',
                    'path': '/api/posts/{id}/comments',
                    'name': '发表评论',
                    'description': '发表文章评论',
                    'params': {
                        'content': '评论内容'
                    },
                    'response': '创建的评论信息',
                    'permission': '登录用户'
                },
                {
                    'method': 'DELETE',
                    'path': '/api/comments/{id}',
                    'name': '删除评论',
                    'description': '删除评论',
                    'params': {},
                    'response': '删除成功消息',
                    'permission': '管理员/评论作者'
                }
            ]
        }
    }
    
    return api_response(200, '获取成功', api_docs)


# ==================== 用户管理模块 ====================

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """获取所有用户信息（仅管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    users = []
    for user in pagination.items:
        user_data = user.to_dict()
        # 添加统计信息
        user_data['post_count'] = user.posts.count()
        user_data['comment_count'] = user.comments.count()
        user_data['last_log'] = None
        
        # 获取最近登录日志（从LoginLog表中获取）
        last_login = LoginLog.query.filter_by(user_id=user.id, login_status='success').order_by(LoginLog.created_at.desc()).first()
        if last_login:
            user_data['last_log'] = {
                'ip_address': last_login.ip_address,
                'created_at': last_login.created_at.isoformat()
            }
        
        users.append(user_data)
    
    return api_response(200, '获取成功', {
        'items': users,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@admin_bp.route('/users/stats', methods=['GET'])
@jwt_required()
def get_users_stats():
    """获取用户统计（仅管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    # 总用户数
    total_users = User.query.count()
    
    # 管理员数
    admin_count = User.query.filter_by(is_admin=True).count()
    
    # 今日注册
    from datetime import datetime, timedelta
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_registered = User.query.filter(User.created_at >= today).count()
    
    # 活跃用户（最近7天有登录）
    week_ago = datetime.utcnow() - timedelta(days=7)
    active_users = User.query.filter(User.last_seen >= week_ago).count()
    
    return api_response(200, '获取成功', {
        'total_users': total_users,
        'admin_count': admin_count,
        'today_registered': today_registered,
        'active_users': active_users
    })


@admin_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    """删除用户（仅管理员，不能删除自己）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    current_user_id = int(get_jwt_identity())
    if id == current_user_id:
        return api_response(400, '不能删除当前登录用户'), 400
    
    user = User.query.get_or_404(id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        return api_response(200, '删除成功')
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'删除失败: {str(e)}'), 500


@admin_bp.route('/users/<int:id>/toggle-admin', methods=['PUT'])
@jwt_required()
def toggle_user_admin(id):
    """切换用户管理员权限（仅管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    current_user_id = int(get_jwt_identity())
    if id == current_user_id:
        return api_response(400, '不能修改自己的权限'), 400
    
    user = User.query.get_or_404(id)
    
    try:
        user.is_admin = not user.is_admin
        db.session.commit()
        return api_response(200, '修改成功', {'is_admin': user.is_admin})
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'修改失败: {str(e)}'), 500
