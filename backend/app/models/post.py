# -*- coding: utf-8 -*-
"""
文章、分类、标签模型
"""

from datetime import datetime
import re
import unicodedata
from app import db


def slugify(text):
    """
    将文本转换为slug
    支持中文：使用拼音或保留中文字符
    """
    if not text:
        return ""
    
    # 转换为小写
    text = text.lower()
    
    # 将中文字符保留，其他特殊字符替换为-
    # 允许中文、英文、数字、空格、连字符
    text = re.sub(r'[^\u4e00-\u9fa5a-z0-9\s-]', '', text)
    
    # 将空格替换为连字符
    text = re.sub(r'[\s]+', '-', text)
    
    # 移除连续的连字符
    text = re.sub(r'-+', '-', text)
    
    # 移除首尾的连字符
    text = text.strip('-')
    
    return text


# 文章-标签关联表
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Category(db.Model):
    """分类模型"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)
        if self.name and not self.slug:
            self.slug = self._generate_slug(self.name)
    
    @staticmethod
    def _generate_slug(name):
        """生成slug"""
        slug = slugify(name)
        # 如果slug为空（全是特殊字符），使用id占位
        if not slug:
            slug = f"category-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        return slug[:50]
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'post_count': self.posts.filter_by(is_published=True).count()
        }


class Tag(db.Model):
    """标签模型"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    slug = db.Column(db.String(30), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', secondary=post_tags,
                           backref=db.backref('tags', lazy='dynamic'),
                           lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
        if self.name and not self.slug:
            self.slug = self._generate_slug(self.name)
    
    @staticmethod
    def _generate_slug(name):
        """生成slug"""
        slug = slugify(name)
        if not slug:
            slug = f"tag-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        return slug[:30]
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'post_count': self.posts.filter_by(is_published=True).count()
        }


class Post(db.Model):
    """文章模型"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    summary = db.Column(db.Text, default='')
    content = db.Column(db.Text, nullable=False)  # Markdown原文
    content_html = db.Column(db.Text)  # 渲染后的HTML
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    is_published = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    comments = db.relationship('Comment', backref='post', lazy='dynamic',
                              cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        if self.title and not self.slug:
            self.slug = self._generate_slug(self.title)
        if self.is_published and not self.published_at:
            self.published_at = datetime.utcnow()
    
    @staticmethod
    def _generate_slug(title):
        """生成slug"""
        slug = slugify(title)
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        # 如果slug为空，使用时间戳
        if not slug:
            slug = f"post-{timestamp}"
        else:
            slug = f"{slug[:50]}-{timestamp}"
        return slug
    
    def increment_view_count(self):
        """增加浏览次数"""
        self.view_count += 1
        db.session.commit()
    
    def get_comment_count(self):
        """获取评论数"""
        return self.comments.count()
    
    def get_tags_list(self):
        """获取标签列表"""
        return [tag.name for tag in self.tags]
    
    def to_dict(self, include_content=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'summary': self.summary,
            'is_published': self.is_published,
            'view_count': self.view_count,
            'comment_count': self.get_comment_count(),
            'tags': [tag.to_dict() for tag in self.tags],
            'category': self.category.to_dict() if self.category else None,
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'avatar': self.author.avatar
            } if self.author else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
        
        if include_content:
            data['content'] = self.content
            data['content_html'] = self.content_html
        
        return data
