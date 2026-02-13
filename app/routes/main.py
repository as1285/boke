# -*- coding: utf-8 -*-
"""
主路由模块
包含首页、文章展示、搜索等公开页面路由
"""

from flask import render_template, request, flash, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
from markdown import markdown
import bleach

from app.routes import main_bp
from app.models import Post, Category, Tag, Comment
from app.forms import CommentForm, SearchForm
from app import db


# 配置Markdown扩展和允许的HTML标签
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'title']
}


@main_bp.route('/')
def index():
    """
    首页路由
    展示文章列表，支持分页
    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.get_published_posts(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE']
    )
    posts = pagination.items
    
    # 获取所有分类和标签用于侧边栏
    categories = Category.query.all()
    tags = Tag.query.all()
    
    return render_template('index.html',
                         posts=posts,
                         pagination=pagination,
                         categories=categories,
                         tags=tags)


@main_bp.route('/post/<slug>')
def post_detail(slug):
    """
    文章详情页路由
    展示单篇文章的完整内容
    
    Args:
        slug: 文章的唯一标识符
    """
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # 检查文章是否已发布，未发布文章只有作者和管理员可见
    if not post.is_published:
        if not current_user.is_authenticated:
            abort(404)
        if not (current_user.is_admin or current_user.id == post.user_id):
            abort(404)
    
    # 增加浏览次数
    post.increment_view_count()
    
    # 获取相关文章
    related_posts = post.get_related_posts(limit=5)
    
    # 获取评论
    page = request.args.get('page', 1, type=int)
    comments_pagination = Comment.get_post_comments(
        post_id=post.id,
        page=page,
        per_page=current_app.config['COMMENTS_PER_PAGE']
    )
    comments = comments_pagination.items
    
    # 评论表单
    form = CommentForm()
    
    return render_template('post_detail.html',
                         post=post,
                         related_posts=related_posts,
                         comments=comments,
                         pagination=comments_pagination,
                         form=form)


@main_bp.route('/post/<slug>/comment', methods=['POST'])
@login_required
def add_comment(slug):
    """
    添加评论路由
    处理文章评论的提交
    
    Args:
        slug: 文章的唯一标识符
    """
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # 检查文章是否已发布
    if not post.is_published:
        abort(404)
    
    form = CommentForm()
    if form.validate_on_submit():
        # 处理Markdown内容
        content_html = markdown(
            form.content.data,
            extensions=['extra', 'codehilite', 'toc']
        )
        # 清理HTML，防止XSS攻击
        content_html = bleach.clean(
            content_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES
        )
        
        comment = Comment(
            content=form.content.data,
            content_html=content_html,
            post_id=post.id,
            user_id=current_user.id,
            parent_id=int(form.parent_id.data) if form.parent_id.data else None
        )
        
        db.session.add(comment)
        db.session.commit()
        
        flash('评论发布成功！', 'success')
    else:
        for error in form.content.errors:
            flash(error, 'danger')
    
    return redirect(url_for('main.post_detail', slug=slug))


@main_bp.route('/category/<slug>')
def category_posts(slug):
    """
    分类文章列表路由
    展示特定分类下的所有文章
    
    Args:
        slug: 分类的唯一标识符
    """
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    pagination = Post.get_published_posts(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        category_id=category.id
    )
    posts = pagination.items
    
    return render_template('category.html',
                         category=category,
                         posts=posts,
                         pagination=pagination)


@main_bp.route('/tag/<slug>')
def tag_posts(slug):
    """
    标签文章列表路由
    展示特定标签下的所有文章
    
    Args:
        slug: 标签的唯一标识符
    """
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    pagination = Post.get_published_posts(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        tag_id=tag.id
    )
    posts = pagination.items
    
    return render_template('tag.html',
                         tag=tag,
                         posts=posts,
                         pagination=pagination)


@main_bp.route('/search')
def search():
    """
    搜索路由
    根据关键词搜索文章
    """
    form = SearchForm()
    keyword = request.args.get('keyword', '')
    
    if not keyword:
        return render_template('search.html', posts=[], keyword='', pagination=None)
    
    page = request.args.get('page', 1, type=int)
    pagination = Post.search_posts(
        keyword=keyword,
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE']
    )
    posts = pagination.items
    
    return render_template('search.html',
                         posts=posts,
                         keyword=keyword,
                         pagination=pagination,
                         form=form)


@main_bp.route('/about')
def about():
    """关于页面路由"""
    return render_template('about.html')


@main_bp.route('/archives')
def archives():
    """
    归档页面路由
    按时间顺序展示所有文章
    """
    posts = Post.query.filter_by(is_published=True).order_by(
        Post.published_at.desc()
    ).all()
    
    # 按年月分组
    archives_dict = {}
    for post in posts:
        if post.published_at:
            year_month = post.published_at.strftime('%Y年%m月')
            if year_month not in archives_dict:
                archives_dict[year_month] = []
            archives_dict[year_month].append(post)
    
    return render_template('archives.html', archives=archives_dict)


@main_bp.app_errorhandler(404)
def page_not_found(error):
    """404错误处理"""
    return render_template('errors/404.html'), 404


@main_bp.app_errorhandler(500)
def internal_error(error):
    """500错误处理"""
    db.session.rollback()
    return render_template('errors/500.html'), 500
