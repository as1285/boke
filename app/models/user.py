# -*- coding: utf-8 -*-
"""
用户模型模块
定义用户相关的数据模型和认证方法
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re

# 从app导入db实例
from app import db


class User(UserMixin, db.Model):
    """
    用户模型
    包含用户基本信息、认证方法和权限控制
    """
    __tablename__ = 'users'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 用户基本信息
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 用户资料
    avatar = db.Column(db.String(200), default='default_avatar.png')
    bio = db.Column(db.Text, default='')
    website = db.Column(db.String(200), default='')
    
    # 权限和状态
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    posts = db.relationship('Post', backref='author', lazy='dynamic',
                           cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic',
                              cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        """
        初始化用户对象
        支持通过关键字参数设置属性
        """
        super(User, self).__init__(**kwargs)
    
    def __repr__(self):
        """返回用户对象的字符串表示"""
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """
        设置用户密码
        使用Werkzeug的generate_password_hash进行哈希加密
        
        Args:
            password: 明文密码
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        验证用户密码
        使用Werkzeug的check_password_hash进行验证
        
        Args:
            password: 明文密码
            
        Returns:
            bool: 密码是否正确
        """
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def validate_username(username):
        """
        验证用户名格式
        规则：3-20个字符，只能包含字母、数字、下划线
        
        Args:
            username: 待验证的用户名
            
        Returns:
            tuple: (是否有效, 错误信息)
        """
        if not username:
            return False, '用户名不能为空'
        if len(username) < 3 or len(username) > 20:
            return False, '用户名长度必须在3-20个字符之间'
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, '用户名只能包含字母、数字和下划线'
        return True, None
    
    @staticmethod
    def validate_email(email):
        """
        验证邮箱格式
        使用正则表达式验证邮箱格式
        
        Args:
            email: 待验证的邮箱
            
        Returns:
            tuple: (是否有效, 错误信息)
        """
        if not email:
            return False, '邮箱不能为空'
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, '邮箱格式不正确'
        return True, None
    
    @staticmethod
    def validate_password(password):
        """
        验证密码强度
        规则：至少6个字符
        
        Args:
            password: 待验证的密码
            
        Returns:
            tuple: (是否有效, 错误信息)
        """
        if not password:
            return False, '密码不能为空'
        if len(password) < 6:
            return False, '密码长度至少为6个字符'
        return True, None
    
    def can_edit_post(self, post):
        """
        检查用户是否有权限编辑文章
        管理员或文章作者可以编辑
        
        Args:
            post: 文章对象
            
        Returns:
            bool: 是否有权限
        """
        return self.is_admin or self.id == post.user_id
    
    def can_delete_post(self, post):
        """
        检查用户是否有权限删除文章
        管理员或文章作者可以删除
        
        Args:
            post: 文章对象
            
        Returns:
            bool: 是否有权限
        """
        return self.is_admin or self.id == post.user_id
    
    def can_delete_comment(self, comment):
        """
        检查用户是否有权限删除评论
        管理员、评论作者或文章作者可以删除
        
        Args:
            comment: 评论对象
            
        Returns:
            bool: 是否有权限
        """
        return (self.is_admin or 
                self.id == comment.user_id or 
                self.id == comment.post.user_id)
    
    def update_last_seen(self):
        """更新用户最后登录时间"""
        self.last_seen = datetime.utcnow()
        db.session.commit()
    
    def get_post_count(self):
        """获取用户发布的文章数量"""
        return self.posts.filter_by(is_published=True).count()
    
    def get_comment_count(self):
        """获取用户发表的评论数量"""
        return self.comments.count()
    
    def to_dict(self):
        """
        将用户对象转换为字典
        用于API响应或序列化
        
        Returns:
            dict: 用户信息的字典表示
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'bio': self.bio,
            'website': self.website,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'post_count': self.get_post_count(),
            'comment_count': self.get_comment_count()
        }
