# -*- coding: utf-8 -*-
"""
测试技术资源序列化器
"""

from marshmallow import Schema, fields


class TestTechResourceSchema(Schema):
    """测试技术资源序列化器"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True)
    description = fields.Str()
    category = fields.Str(required=True)
    icon = fields.Str()
    is_recommended = fields.Bool()
    sort_order = fields.Int()
    created_at = fields.DateTime(dump_only=True)
