# -*- coding: utf-8 -*-
"""
标签和分类管理路由（管理员）
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.models import Tag, Category, User
from app.schemas import TagSchema, CategorySchema

tags_bp = Blueprint('tags', __name__)

tag_schema = TagSchema()
category_schema = CategorySchema()


def api_response(code=200, msg='操作成功', data=None):
    """统一API响应格式"""
    return {'code': code, 'msg': msg, 'data': data}


def check_admin():
    """检查是否为管理员"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    return user and user.is_admin


# ========== 分类管理 ==========

@tags_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """创建分类（管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    json_data = request.get_json()
    try:
        data = category_schema.load(json_data)
        
        if Category.query.filter_by(name=data['name']).first():
            return api_response(400, '分类名称已存在'), 400
        
        category = Category(name=data['name'], description=data.get('description', ''))
        db.session.add(category)
        db.session.commit()
        
        return api_response(200, '创建成功', category.to_dict())
        
    except ValidationError as err:
        return api_response(400, '数据验证失败', err.messages), 400
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'创建失败: {str(e)}'), 500


@tags_bp.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    """更新分类（管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    category = Category.query.get_or_404(id)
    json_data = request.get_json()
    
    try:
        data = category_schema.load(json_data, partial=True)
        
        if 'name' in data:
            existing = Category.query.filter_by(name=data['name']).first()
            if existing and existing.id != id:
                return api_response(400, '分类名称已存在'), 400
            category.name = data['name']
        
        if 'description' in data:
            category.description = data['description']
        
        db.session.commit()
        return api_response(200, '更新成功', category.to_dict())
        
    except ValidationError as err:
        return api_response(400, '数据验证失败', err.messages), 400
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'更新失败: {str(e)}'), 500


@tags_bp.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    """删除分类（管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    category = Category.query.get_or_404(id)
    
    try:
        # 将该分类下的文章设为无分类
        from app.models import Post
        Post.query.filter_by(category_id=id).update({'category_id': None})
        
        db.session.delete(category)
        db.session.commit()
        return api_response(200, '删除成功')
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'删除失败: {str(e)}'), 500


# ========== 标签管理 ==========

@tags_bp.route('/tags', methods=['POST'])
@jwt_required()
def create_tag():
    """创建标签（管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    json_data = request.get_json()
    try:
        data = tag_schema.load(json_data)
        
        if Tag.query.filter_by(name=data['name']).first():
            return api_response(400, '标签名称已存在'), 400
        
        tag = Tag(name=data['name'])
        db.session.add(tag)
        db.session.commit()
        
        return api_response(200, '创建成功', tag.to_dict())
        
    except ValidationError as err:
        return api_response(400, '数据验证失败', err.messages), 400
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'创建失败: {str(e)}'), 500


@tags_bp.route('/tags/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_tag(id):
    """删除标签（管理员）"""
    if not check_admin():
        return api_response(403, '无权限操作'), 403
    
    tag = Tag.query.get_or_404(id)
    
    try:
        db.session.delete(tag)
        db.session.commit()
        return api_response(200, '删除成功')
    except Exception as e:
        db.session.rollback()
        return api_response(500, f'删除失败: {str(e)}'), 500
