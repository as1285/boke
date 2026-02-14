# -*- coding: utf-8 -*-
"""
文章路由
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from markdown import markdown
import bleach

from app import db
from app.models import Post, Category, Tag, User
from app.schemas import PostSchema

posts_bp = Blueprint('posts', __name__)
post_schema = PostSchema()


def api_response(code=200, msg='操作成功', data=None):
    """统一API响应格式"""
    return {'code': code, 'msg': msg, 'data': data}


def render_markdown(content):
    """渲染Markdown为HTML"""
    html = markdown(content, extensions=['extra', 'codehilite'])
    allowed_tags = ['p', 'br', 'strong', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                   'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img']
    allowed_attrs = {'a': ['href', 'title'], 'img': ['src', 'alt', 'title']}
    return bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)


@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    """获取文章列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    tag_id = request.args.get('tag_id', type=int)
    keyword = request.args.get('keyword', '')
    
    query = Post.query.filter_by(is_published=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    if tag_id:
        query = query.join(Post.tags).filter(Tag.id == tag_id)
    if keyword:
        query = query.filter(
            db.or_(
                Post.title.ilike(f'%{keyword}%'),
                Post.content.ilike(f'%{keyword}%')
            )
        )
    
    pagination = query.order_by(Post.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    posts = [post.to_dict() for post in pagination.items]
    
    return api_response(200, '获取成功', {
        'items': posts,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@posts_bp.route('/posts/<slug>', methods=['GET'])
def get_post(slug):
    """获取文章详情"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # 增加浏览次数
    post.increment_view_count()
    
    return api_response(200, '获取成功', post.to_dict(include_content=True))


@posts_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    """创建文章（需要管理员权限）"""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    
    if not user or not user.is_admin:
        return api_response(403, '无权限操作'), 403
    
    json_data = request.get_json()
    if not json_data:
        return api_response(400, '无效的请求数据'), 400
    
    try:
        data = post_schema.load(json_data)
        
        # 渲染Markdown
        content_html = render_markdown(data['content'])
        
        post = Post(
            title=data['title'],
            content=data['content'],
            content_html=content_html,
            summary=data.get('summary', ''),
            is_published=data.get('is_published', False),
            user_id=user_id,
            category_id=data.get('category_id')
        )
        
        db.session.add(post)
        db.session.commit()
        
        # 处理标签
        if 'tag_ids' in data:
            for tag_id in data['tag_ids']:
                tag = db.session.get(Tag, tag_id)
                if tag:
                    post.tags.append(tag)
            db.session.commit()
        
        return api_response(200, '创建成功', post.to_dict())
        
    except ValidationError as err:
        return api_response(400, '数据验证失败', err.messages), 400
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'创建失败: {str(e)}'), 500


@posts_bp.route('/posts/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    """更新文章（需要管理员权限）"""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    
    if not user or not user.is_admin:
        return api_response(403, '无权限操作'), 403
    
    post = Post.query.get_or_404(id)
    json_data = request.get_json()
    
    try:
        data = post_schema.load(json_data, partial=True)
        
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
            post.content_html = render_markdown(data['content'])
        if 'summary' in data:
            post.summary = data['summary']
        if 'is_published' in data:
            post.is_published = data['is_published']
            if data['is_published'] and not post.published_at:
                post.published_at = db.func.now()
        if 'category_id' in data:
            post.category_id = data['category_id']
        
        # 更新标签
        if 'tag_ids' in data:
            post.tags = []
            for tag_id in data['tag_ids']:
                tag = db.session.get(Tag, tag_id)
                if tag:
                    post.tags.append(tag)
        
        db.session.commit()
        return api_response(200, '更新成功', post.to_dict())
        
    except ValidationError as err:
        return api_response(400, '数据验证失败', err.messages), 400
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'更新失败: {str(e)}'), 500


@posts_bp.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    """删除文章（需要管理员权限）"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or not user.is_admin:
        return api_response(403, '无权限操作'), 403
    
    post = Post.query.get_or_404(id)
    
    try:
        db.session.delete(post)
        db.session.commit()
        return api_response(200, '删除成功')
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'删除失败: {str(e)}'), 500


@posts_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有分类"""
    categories = Category.query.all()
    return api_response(200, '获取成功', [c.to_dict() for c in categories])


@posts_bp.route('/tags', methods=['GET'])
def get_tags():
    """获取所有标签"""
    tags = Tag.query.all()
    return api_response(200, '获取成功', [t.to_dict() for t in tags])
