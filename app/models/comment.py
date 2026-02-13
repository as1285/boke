# -*- coding: utf-8 -*-
"""
评论模型模块
定义评论相关的数据模型
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# 从app导入db实例
from app import db


class Comment(db.Model):
    """
    评论模型
    支持文章评论的增删改查
    """
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 评论内容
    content = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text)  # Markdown渲染后的HTML
    
    # 外键关联
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 回复功能（自关联）
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]),
                             lazy='dynamic', cascade='all, delete-orphan')
    
    # 状态
    is_approved = db.Column(db.Boolean, default=True)  # 是否通过审核
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        """初始化评论对象"""
        super(Comment, self).__init__(**kwargs)
    
    def __repr__(self):
        """返回评论对象的字符串表示"""
        return f'<Comment {self.id} by {self.author.username if self.author else "Anonymous"}>'
    
    def approve(self):
        """通过评论审核"""
        self.is_approved = True
        db.session.commit()
    
    def disapprove(self):
        """拒绝评论审核"""
        self.is_approved = False
        db.session.commit()
    
    def get_replies_count(self):
        """获取回复数量"""
        return self.replies.filter_by(is_approved=True).count()
    
    @staticmethod
    def get_post_comments(post_id, page=1, per_page=20, include_unapproved=False):
        """
        获取文章的评论列表
        
        Args:
            post_id: 文章ID
            page: 页码
            per_page: 每页数量
            include_unapproved: 是否包含未审核的评论
            
        Returns:
            Pagination: 分页对象
        """
        query = Comment.query.filter_by(post_id=post_id, parent_id=None)
        
        if not include_unapproved:
            query = query.filter_by(is_approved=True)
        
        return query.order_by(Comment.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @staticmethod
    def get_user_comments(user_id, page=1, per_page=20):
        """
        获取用户的评论列表
        
        Args:
            user_id: 用户ID
            page: 页码
            per_page: 每页数量
            
        Returns:
            Pagination: 分页对象
        """
        return Comment.query.filter_by(user_id=user_id).order_by(
            Comment.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
    
    def to_dict(self, include_replies=False):
        """
        将评论对象转换为字典
        
        Args:
            include_replies: 是否包含回复列表
            
        Returns:
            dict: 评论信息的字典表示
        """
        data = {
            'id': self.id,
            'content': self.content,
            'content_html': self.content_html,
            'is_approved': self.is_approved,
            'post_id': self.post_id,
            'author': {
                'id': self.author.id if self.author else None,
                'username': self.author.username if self.author else 'Anonymous',
                'avatar': self.author.avatar if self.author else 'default_avatar.png'
            },
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_replies:
            replies = self.replies.filter_by(is_approved=True).order_by(
                Comment.created_at.asc()
            ).all()
            data['replies'] = [reply.to_dict() for reply in replies]
            data['replies_count'] = len(replies)
        
        return data
