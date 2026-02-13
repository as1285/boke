# -*- coding: utf-8 -*-
"""
用户序列化器
"""

from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    """用户序列化器"""
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=20))
    email = fields.Email(required=True)
    password = fields.String(load_only=True, validate=validate.Length(min=6), required=True)
    avatar = fields.String(dump_only=True)
    bio = fields.String()
    website = fields.String()
    is_admin = fields.Boolean(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    last_seen = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    """用户登录序列化器"""
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
