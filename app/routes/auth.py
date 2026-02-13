# -*- coding: utf-8 -*-
"""
用户认证路由模块
包含登录、注册、退出等用户认证相关路由
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.routes import auth_bp
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm
from app import db


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录路由
    处理用户登录逻辑
    """
    # 如果用户已登录，重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # 验证密码
        if user and user.check_password(form.password.data):
            # 登录用户
            login_user(user, remember=form.remember_me.data)
            # 更新最后登录时间
            user.update_last_seen()
            
            flash(f'欢迎回来，{user.username}！', 'success')
            
            # 如果有下一页参数，重定向到该页面
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册路由
    处理用户注册逻辑
    """
    # 如果用户已登录，重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # 创建新用户
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！请登录。', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """
    用户退出路由
    处理用户退出登录
    """
    logout_user()
    flash('您已成功退出登录。', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """
    用户个人资料页面
    展示用户的基本信息和发布的文章
    """
    # 获取用户的文章
    posts = current_user.posts.order_by(Post.created_at.desc()).all()
    
    return render_template('auth/profile.html', user=current_user, posts=posts)


@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    编辑个人资料路由
    允许用户修改个人资料
    """
    form = EditProfileForm(
        original_username=current_user.username,
        original_email=current_user.email
    )
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.website = form.website.data
        
        db.session.commit()
        flash('个人资料已更新。', 'success')
        return redirect(url_for('auth.profile'))
    
    # 预填充表单数据
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.website.data = current_user.website
    
    return render_template('auth/edit_profile.html', form=form)


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    修改密码路由
    允许用户修改登录密码
    """
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # 设置新密码
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        flash('密码修改成功！', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html', form=form)


# 导入Post模型（放在最后避免循环导入）
from app.models import Post
