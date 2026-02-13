# -*- coding: utf-8 -*-
"""
日志模型
"""

from datetime import datetime
from app import db


class APILog(db.Model):
    """API调用日志"""
    __tablename__ = 'api_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10), nullable=False)  # GET/POST/PUT/DELETE
    path = db.Column(db.String(200), nullable=False)   # 请求路径
    ip_address = db.Column(db.String(50))              # IP地址
    user_agent = db.Column(db.String(500))             # 用户代理
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 用户ID
    status_code = db.Column(db.Integer)                # 响应状态码
    response_time = db.Column(db.Float)                # 响应时间(秒)
    request_data = db.Column(db.Text)                  # 请求数据(JSON)
    response_data = db.Column(db.Text)                 # 响应数据(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    user = db.relationship('User', backref='api_logs', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'method': self.method,
            'path': self.path,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'status_code': self.status_code,
            'response_time': self.response_time,
            'request_data': self.request_data,
            'response_data': self.response_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
