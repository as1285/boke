# -*- coding: utf-8 -*-
"""
后台管理路由模块
包含文章管理、分类管理、用户管理等后台功能路由
"""

from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from functools import wraps
from markdown import markdown
import bleach

from app.routes import admin_bp
from app.models import Post, Category, Tag, Comment, User
from app.forms import PostForm, CategoryForm
from app import db


# 管理员权限装饰器
def admin_required(f):
    """
    管理员权限装饰器
    确保只有管理员可以访问某些路由
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# 作者或管理员权限装饰器
def author_or_admin_required(f):
    """
    作者或管理员权限装饰器
    确保只有文章作者或管理员可以编辑/删除文章
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if not (current_user.is_admin or current_user.id == kwargs.get('user_id')):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """
    后台管理首页
    展示统计数据概览
    """
    # 统计数据
    stats = {
        'total_posts': Post.query.count(),
        'published_posts': Post.query.filter_by(is_published=True).count(),
        'draft_posts': Post.query.filter_by(is_published=False).count(),
        'total_users': User.query.count(),
        'total_comments': Comment.query.count(),
        'total_categories': Category.query.count(),
        'total_tags': Tag.query.count()
    }
    
    # 最近发布的文章
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    # 最近的评论
    recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_posts=recent_posts,
                         recent_comments=recent_comments)


# ==================== 文章管理 ====================

@admin_bp.route('/posts')
@login_required
@admin_required
def post_list():
    """
    文章列表页面
    支持按状态筛选和分页
    """
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = Post.query
    
    # 按状态筛选
    if status == 'published':
        query = query.filter_by(is_published=True)
    elif status == 'draft':
        query = query.filter_by(is_published=False)
    
    pagination = query.order_by(Post.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    
    return render_template('admin/post_list.html',
                         posts=posts,
                         pagination=pagination,
                         status=status)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_post():
    """
    创建新文章
    处理文章创建表单
    """
    form = PostForm()
    
    if form.validate_on_submit():
        # 处理Markdown内容
        content_html = markdown(
            form.content.data,
            extensions=['extra', 'codehilite', 'toc']
        )
        # 清理HTML
        content_html = bleach.clean(
            content_html,
            tags=['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                  'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img'],
            attributes={'a': ['href', 'title'], 'img': ['src', 'alt', 'title']}
        )
        
        post = Post(
            title=form.title.data,
            summary=form.summary.data,
            content=form.content.data,
            content_html=content_html,
            user_id=current_user.id,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
            is_published=form.is_published.data
        )
        
        db.session.add(post)
        db.session.commit()
        
        # 处理标签
        if form.tags.data:
            tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            post.set_tags(tag_names)
        
        if form.is_published.data:
            flash('文章已发布！', 'success')
        else:
            flash('文章已保存为草稿。', 'info')
        
        return redirect(url_for('admin.post_list'))
    
    return render_template('admin/post_form.html', form=form, title='新建文章')


@admin_bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    """
    编辑文章
    处理文章编辑表单
    
    Args:
        id: 文章ID
    """
    post = Post.query.get_or_404(id)
    
    # 检查权限
    if not current_user.can_edit_post(post):
        abort(403)
    
    form = PostForm()
    
    if form.validate_on_submit():
        # 处理Markdown内容
        content_html = markdown(
            form.content.data,
            extensions=['extra', 'codehilite', 'toc']
        )
        content_html = bleach.clean(
            content_html,
            tags=['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                  'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img'],
            attributes={'a': ['href', 'title'], 'img': ['src', 'alt', 'title']}
        )
        
        post.title = form.title.data
        post.summary = form.summary.data
        post.content = form.content.data
        post.content_html = content_html
        post.category_id = form.category_id.data if form.category_id.data != 0 else None
        
        # 处理发布状态
        if form.is_published.data and not post.is_published:
            post.publish()
        elif not form.is_published.data and post.is_published:
            post.unpublish()
        
        # 处理标签
        if form.tags.data:
            tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            post.set_tags(tag_names)
        else:
            post.tags = []
        
        db.session.commit()
        
        flash('文章已更新！', 'success')
        return redirect(url_for('admin.post_list'))
    
    # 预填充表单数据
    elif request.method == 'GET':
        form.title.data = post.title
        form.summary.data = post.summary
        form.content.data = post.content
        form.category_id.data = post.category_id or 0
        form.is_published.data = post.is_published
        form.tags.data = ', '.join(post.get_tags_list())
    
    return render_template('admin/post_form.html', form=form, title='编辑文章', post=post)


@admin_bp.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    """
    删除文章
    
    Args:
        id: 文章ID
    """
    post = Post.query.get_or_404(id)
    
    # 检查权限
    if not current_user.can_delete_post(post):
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    
    flash('文章已删除。', 'success')
    return redirect(url_for('admin.post_list'))


# ==================== 分类管理 ====================

@admin_bp.route('/categories')
@login_required
@admin_required
def category_list():
    """分类列表页面"""
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/category_list.html', categories=categories)


@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_category():
    """创建新分类"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        
        flash('分类已创建！', 'success')
        return redirect(url_for('admin.category_list'))
    
    return render_template('admin/category_form.html', form=form, title='新建分类')


@admin_bp.route('/category/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(id):
    """
    编辑分类
    
    Args:
        id: 分类ID
    """
    category = Category.query.get_or_404(id)
    form = CategoryForm(original_name=category.name)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        
        flash('分类已更新！', 'success')
        return redirect(url_for('admin.category_list'))
    
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
    
    return render_template('admin/category_form.html', form=form, title='编辑分类')


@admin_bp.route('/category/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    """
    删除分类
    
    Args:
        id: 分类ID
    """
    category = Category.query.get_or_404(id)
    
    # 将该分类下的文章设为无分类
    Post.query.filter_by(category_id=id).update({'category_id': None})
    
    db.session.delete(category)
    db.session.commit()
    
    flash('分类已删除。', 'success')
    return redirect(url_for('admin.category_list'))


# ==================== 评论管理 ====================

@admin_bp.route('/comments')
@login_required
@admin_required
def comment_list():
    """评论列表页面"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = Comment.query
    
    if status == 'approved':
        query = query.filter_by(is_approved=True)
    elif status == 'pending':
        query = query.filter_by(is_approved=False)
    
    pagination = query.order_by(Comment.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    
    return render_template('admin/comment_list.html',
                         comments=comments,
                         pagination=pagination,
                         status=status)


@admin_bp.route('/comment/<int:id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_comment(id):
    """
    通过评论审核
    
    Args:
        id: 评论ID
    """
    comment = Comment.query.get_or_404(id)
    comment.approve()
    
    flash('评论已通过审核。', 'success')
    return redirect(url_for('admin.comment_list'))


@admin_bp.route('/comment/<int:id>/delete', methods=['POST'])
@login_required
def delete_comment(id):
    """
    删除评论
    
    Args:
        id: 评论ID
    """
    comment = Comment.query.get_or_404(id)
    
    # 检查权限
    if not current_user.can_delete_comment(comment):
        abort(403)
    
    db.session.delete(comment)
    db.session.commit()
    
    flash('评论已删除。', 'success')
    return redirect(url_for('admin.comment_list'))


# ==================== 用户管理 ====================

@admin_bp.route('/users')
@login_required
@admin_required
def user_list():
    """用户列表页面"""
    page = request.args.get('page', 1, type=int)
    
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    users = pagination.items
    
    return render_template('admin/user_list.html',
                         users=users,
                         pagination=pagination)


@admin_bp.route('/user/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(id):
    """
    切换用户管理员权限
    
    Args:
        id: 用户ID
    """
    user = User.query.get_or_404(id)
    
    # 不能修改自己的权限
    if user.id == current_user.id:
        flash('不能修改自己的权限。', 'danger')
        return redirect(url_for('admin.user_list'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    if user.is_admin:
        flash(f'{user.username} 已被设为管理员。', 'success')
    else:
        flash(f'{user.username} 的管理员权限已被取消。', 'info')
    
    return redirect(url_for('admin.user_list'))


@admin_bp.route('/user/<int:id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_active(id):
    """
    切换用户激活状态
    
    Args:
        id: 用户ID
    """
    user = User.query.get_or_404(id)
    
    # 不能禁用自己的账户
    if user.id == current_user.id:
        flash('不能禁用自己的账户。', 'danger')
        return redirect(url_for('admin.user_list'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    if user.is_active:
        flash(f'{user.username} 的账户已激活。', 'success')
    else:
        flash(f'{user.username} 的账户已被禁用。', 'info')
    
    return redirect(url_for('admin.user_list'))
