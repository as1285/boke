# -*- coding: utf-8 -*-
"""
登录日志模型
"""

from datetime import datetime
from app import db


class LoginLog(db.Model):
    """用户登录日志"""
    __tablename__ = 'login_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(50))              # IP地址
    user_agent = db.Column(db.String(500))             # 用户代理
    login_type = db.Column(db.String(20), default='password')  # 登录方式：password, token
    login_status = db.Column(db.String(20), default='success')  # 登录状态：success, failed
    fail_reason = db.Column(db.String(200))            # 失败原因
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    user = db.relationship('User', backref='login_logs', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'login_type': self.login_type,
            'login_status': self.login_status,
            'fail_reason': self.fail_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
