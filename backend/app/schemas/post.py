# -*- coding: utf-8 -*-
"""
文章、分类、标签序列化器
"""

from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    """分类序列化器"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    slug = fields.String(dump_only=True)
    description = fields.String()
    post_count = fields.Integer(dump_only=True)


class TagSchema(Schema):
    """标签序列化器"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=30))
    slug = fields.String(dump_only=True)
    post_count = fields.Integer(dump_only=True)


class PostSchema(Schema):
    """文章序列化器"""
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=200))
    slug = fields.String(dump_only=True)
    summary = fields.String()
    content = fields.String(load_only=True)  # 仅用于反序列化（创建/更新）
    content_html = fields.String(dump_only=True)  # 仅用于序列化（返回）
    is_published = fields.Boolean()
    view_count = fields.Integer(dump_only=True)
    comment_count = fields.Integer(dump_only=True)
    
    # 嵌套关系
    category = fields.Nested(CategorySchema, dump_only=True)
    category_id = fields.Integer(load_only=True)
    tags = fields.Nested(TagSchema, many=True, dump_only=True)
    tag_ids = fields.List(fields.Integer(), load_only=True)
    
    author = fields.Dict(dump_only=True)
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    published_at = fields.DateTime(dump_only=True)
