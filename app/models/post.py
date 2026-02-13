# -*- coding: utf-8 -*-
"""
文章模型模块
定义文章、分类、标签相关的数据模型
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import re

# 从app导入db实例
from app import db

# 文章-标签关联表（多对多关系）
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Category(db.Model):
    """
    文章分类模型
    用于对文章进行分类管理
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    
    def __init__(self, **kwargs):
        """初始化分类对象，自动生成slug"""
        super(Category, self).__init__(**kwargs)
        if self.name and not self.slug:
            self.slug = self.generate_slug(self.name)
    
    def __repr__(self):
        """返回分类对象的字符串表示"""
        return f'<Category {self.name}>'
    
    @staticmethod
    def generate_slug(name):
        """
        根据分类名称生成slug
        将中文转换为拼音或保留英文，去除特殊字符
        
        Args:
            name: 分类名称
            
        Returns:
            str: 生成的slug
        """
        # 简单的slug生成：转为小写，替换空格为连字符，去除特殊字符
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:50]
    
    def get_post_count(self):
        """获取该分类下的已发布文章数量"""
        return self.posts.filter_by(is_published=True).count()
    
    def to_dict(self):
        """
        将分类对象转换为字典
        
        Returns:
            dict: 分类信息的字典表示
        """
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'post_count': self.get_post_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Tag(db.Model):
    """
    文章标签模型
    用于给文章打标签，支持多对多关联
    """
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    slug = db.Column(db.String(30), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系（多对多）
    posts = db.relationship('Post', secondary=post_tags,
                           backref=db.backref('tags', lazy='dynamic'),
                           lazy='dynamic')
    
    def __init__(self, **kwargs):
        """初始化标签对象，自动生成slug"""
        super(Tag, self).__init__(**kwargs)
        if self.name and not self.slug:
            self.slug = self.generate_slug(self.name)
    
    def __repr__(self):
        """返回标签对象的字符串表示"""
        return f'<Tag {self.name}>'
    
    @staticmethod
    def generate_slug(name):
        """
        根据标签名称生成slug
        
        Args:
            name: 标签名称
            
        Returns:
            str: 生成的slug
        """
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:30]
    
    @staticmethod
    def get_or_create(name):
        """
        获取或创建标签
        如果标签已存在则返回现有标签，否则创建新标签
        
        Args:
            name: 标签名称
            
        Returns:
            Tag: 标签对象
        """
        tag = Tag.query.filter_by(name=name).first()
        if tag:
            return tag
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return tag
    
    def get_post_count(self):
        """获取使用该标签的已发布文章数量"""
        return self.posts.filter_by(is_published=True).count()
    
    def to_dict(self):
        """
        将标签对象转换为字典
        
        Returns:
            dict: 标签信息的字典表示
        """
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'post_count': self.get_post_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Post(db.Model):
    """
    文章模型
    博客系统的核心模型，包含文章内容、元数据和相关关联
    """
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 文章基本信息
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    summary = db.Column(db.Text, default='')
    content = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text)  # Markdown渲染后的HTML
    
    # 外键关联
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # 文章状态
    is_published = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # 关联关系
    comments = db.relationship('Comment', backref='post', lazy='dynamic',
                              cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        """
        初始化文章对象
        自动生成slug，设置发布时间
        """
        super(Post, self).__init__(**kwargs)
        if self.title and not self.slug:
            self.slug = self.generate_slug(self.title)
        if self.is_published and not self.published_at:
            self.published_at = datetime.utcnow()
    
    def __repr__(self):
        """返回文章对象的字符串表示"""
        return f'<Post {self.title}>'
    
    @staticmethod
    def generate_slug(title):
        """
        根据文章标题生成slug
        用于URL中的文章标识
        
        Args:
            title: 文章标题
            
        Returns:
            str: 生成的slug
        """
        # 简单的slug生成
        slug = title.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # 添加时间戳避免重复
        timestamp = datetime.utcnow().strftime('%Y%m%d')
        return f"{slug[:50]}-{timestamp}"
    
    def publish(self):
        """发布文章，设置发布状态和时间"""
        self.is_published = True
        self.published_at = datetime.utcnow()
        db.session.commit()
    
    def unpublish(self):
        """取消发布文章"""
        self.is_published = False
        db.session.commit()
    
    def increment_view_count(self):
        """增加文章浏览次数"""
        self.view_count += 1
        db.session.commit()
    
    def get_comment_count(self):
        """获取文章评论数量"""
        return self.comments.count()
    
    def get_related_posts(self, limit=5):
        """
        获取相关文章
        基于相同分类或标签推荐相关文章
        
        Args:
            limit: 返回文章数量限制
            
        Returns:
            list: 相关文章列表
        """
        # 获取相同分类的文章
        related = Post.query.filter(
            Post.id != self.id,
            Post.is_published == True,
            Post.category_id == self.category_id
        ).order_by(Post.published_at.desc()).limit(limit).all()
        
        # 如果数量不足，补充相同标签的文章
        if len(related) < limit:
            tag_ids = [tag.id for tag in self.tags]
            if tag_ids:
                additional = Post.query.filter(
                    Post.id != self.id,
                    Post.is_published == True,
                    Post.id.notin_([p.id for p in related])
                ).join(Post.tags).filter(Tag.id.in_(tag_ids)).group_by(Post.id).order_by(
                    db.func.count(Post.id).desc()
                ).limit(limit - len(related)).all()
                related.extend(additional)
        
        return related
    
    def set_tags(self, tag_names):
        """
        设置文章标签
        支持传入标签名称列表，自动创建不存在的标签
        
        Args:
            tag_names: 标签名称列表
        """
        # 清除现有标签
        self.tags = []
        
        # 添加新标签
        for name in tag_names:
            if name.strip():
                tag = Tag.get_or_create(name.strip())
                self.tags.append(tag)
        
        db.session.commit()
    
    def get_tags_list(self):
        """
        获取文章标签列表
        
        Returns:
            list: 标签名称列表
        """
        return [tag.name for tag in self.tags]
    
    @staticmethod
    def get_published_posts(page=1, per_page=10, category_id=None, tag_id=None):
        """
        获取已发布的文章列表（支持分页和筛选）
        
        Args:
            page: 页码
            per_page: 每页数量
            category_id: 分类ID筛选
            tag_id: 标签ID筛选
            
        Returns:
            Pagination: 分页对象
        """
        query = Post.query.filter_by(is_published=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if tag_id:
            query = query.join(Post.tags).filter(Tag.id == tag_id)
        
        return query.order_by(Post.published_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @staticmethod
    def search_posts(keyword, page=1, per_page=10):
        """
        搜索文章
        根据标题或内容关键词搜索
        
        Args:
            keyword: 搜索关键词
            page: 页码
            per_page: 每页数量
            
        Returns:
            Pagination: 分页对象
        """
        search_pattern = f'%{keyword}%'
        return Post.query.filter(
            Post.is_published == True,
            db.or_(
                Post.title.ilike(search_pattern),
                Post.content.ilike(search_pattern)
            )
        ).order_by(Post.published_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    def to_dict(self, include_content=False):
        """
        将文章对象转换为字典
        
        Args:
            include_content: 是否包含完整内容
            
        Returns:
            dict: 文章信息的字典表示
        """
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'summary': self.summary,
            'is_published': self.is_published,
            'view_count': self.view_count,
            'comment_count': self.get_comment_count(),
            'tags': self.get_tags_list(),
            'category': self.category.name if self.category else None,
            'author': self.author.username if self.author else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
        
        if include_content:
            data['content'] = self.content
            data['content_html'] = self.content_html
        
        return data
