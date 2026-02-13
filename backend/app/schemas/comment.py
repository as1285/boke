# -*- coding: utf-8 -*-
"""
评论序列化器
"""

from marshmallow import Schema, fields


class CommentSchema(Schema):
    """评论序列化器"""
    id = fields.Integer(dump_only=True)
    content = fields.String(required=True)
    content_html = fields.String(dump_only=True)
    is_approved = fields.Boolean(dump_only=True)
    
    author = fields.Dict(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
