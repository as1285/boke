# -*- coding: utf-8 -*-
"""
评论路由
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from markdown import markdown
import bleach

from app import db
from app.models import Comment, Post, User
from app.schemas import CommentSchema

comments_bp = Blueprint('comments', __name__)
comment_schema = CommentSchema()


def api_response(code=200, msg='操作成功', data=None):
    """统一API响应格式"""
    return {'code': code, 'msg': msg, 'data': data}


def render_markdown(content):
    """渲染Markdown为HTML"""
    html = markdown(content, extensions=['extra'])
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'code', 'pre', 'a']
    allowed_attrs = {'a': ['href', 'title']}
    return bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)


@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """获取文章评论列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    post = Post.query.get_or_404(post_id)
    
    pagination = Comment.query.filter_by(
        post_id=post_id,
        parent_id=None,
        is_approved=True
    ).order_by(Comment.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    comments = [comment.to_dict() for comment in pagination.items]
    
    return api_response(200, '获取成功', {
        'items': comments,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@comments_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    """创建评论（需要登录）"""
    user_id = int(get_jwt_identity())
    post = Post.query.get_or_404(post_id)
    
    json_data = request.get_json()
    if not json_data:
        return api_response(400, '无效的请求数据'), 400
    
    try:
        data = comment_schema.load(json_data)
        
        # 渲染Markdown
        content_html = render_markdown(data['content'])
        
        comment = Comment(
            content=data['content'],
            content_html=content_html,
            post_id=post_id,
            user_id=user_id,
            parent_id=data.get('parent_id')
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return api_response(200, '评论成功', comment.to_dict())
        
    except ValidationError as err:
        return api_response(400, '数据验证失败', err.messages), 400
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'评论失败: {str(e)}'), 500


@comments_bp.route('/comments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    """删除评论（需要管理员或评论作者）"""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    comment = Comment.query.get_or_404(id)
    
    # 检查权限
    if not user.is_admin and comment.user_id != user_id:
        return api_response(403, '无权限操作'), 403
    
    try:
        db.session.delete(comment)
        db.session.commit()
        return api_response(200, '删除成功')
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'删除失败: {str(e)}'), 500
