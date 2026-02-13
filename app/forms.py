# -*- coding: utf-8 -*-
"""
表单验证模块
使用Flask-WTF进行表单验证，包含用户认证、文章管理、评论等表单
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user

# 导入模型（用于验证唯一性）
from app.models import User, Category


class LoginForm(FlaskForm):
    """
    用户登录表单
    验证用户名和密码
    """
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码')
    ])
    remember_me = BooleanField('记住我')
    
    def validate_username(self, field):
        """
        验证用户名是否存在
        
        Args:
            field: 用户名字段
            
        Raises:
            ValidationError: 用户不存在时抛出
        """
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError('用户名或密码错误')
        if not user.is_active:
            raise ValidationError('该账户已被禁用')


class RegistrationForm(FlaskForm):
    """
    用户注册表单
    验证用户名、邮箱和密码
    """
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱'),
        Email(message='请输入有效的邮箱地址')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=6, message='密码长度至少为6个字符')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    
    def validate_username(self, field):
        """
        验证用户名是否已存在
        
        Args:
            field: 用户名字段
            
        Raises:
            ValidationError: 用户名已存在时抛出
        """
        # 验证用户名格式
        is_valid, error_msg = User.validate_username(field.data)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用')
    
    def validate_email(self, field):
        """
        验证邮箱是否已存在
        
        Args:
            field: 邮箱字段
            
        Raises:
            ValidationError: 邮箱已存在时抛出
        """
        # 验证邮箱格式
        is_valid, error_msg = User.validate_email(field.data)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')


class EditProfileForm(FlaskForm):
    """
    编辑用户资料表单
    允许用户修改个人资料
    """
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱'),
        Email(message='请输入有效的邮箱地址')
    ])
    bio = TextAreaField('个人简介', validators=[
        Optional(),
        Length(max=500, message='个人简介不能超过500个字符')
    ])
    website = StringField('个人网站', validators=[
        Optional(),
        Length(max=200, message='网站地址不能超过200个字符')
    ])
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        """
        初始化表单，保存原始用户名和邮箱
        
        Args:
            original_username: 原始用户名
            original_email: 原始邮箱
        """
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, field):
        """
        验证用户名是否可用
        
        Args:
            field: 用户名字段
            
        Raises:
            ValidationError: 用户名已被其他用户使用
        """
        if field.data != self.original_username:
            is_valid, error_msg = User.validate_username(field.data)
            if not is_valid:
                raise ValidationError(error_msg)
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('该用户名已被使用')
    
    def validate_email(self, field):
        """
        验证邮箱是否可用
        
        Args:
            field: 邮箱字段
            
        Raises:
            ValidationError: 邮箱已被其他用户使用
        """
        if field.data != self.original_email:
            is_valid, error_msg = User.validate_email(field.data)
            if not is_valid:
                raise ValidationError(error_msg)
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('该邮箱已被注册')


class ChangePasswordForm(FlaskForm):
    """
    修改密码表单
    允许用户修改登录密码
    """
    old_password = PasswordField('当前密码', validators=[
        DataRequired(message='请输入当前密码')
    ])
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='请输入新密码'),
        Length(min=6, message='密码长度至少为6个字符')
    ])
    new_password2 = PasswordField('确认新密码', validators=[
        DataRequired(message='请确认新密码'),
        EqualTo('new_password', message='两次输入的密码不一致')
    ])
    
    def validate_old_password(self, field):
        """
        验证当前密码是否正确
        
        Args:
            field: 当前密码字段
            
        Raises:
            ValidationError: 密码不正确时抛出
        """
        if not current_user.check_password(field.data):
            raise ValidationError('当前密码不正确')


class PostForm(FlaskForm):
    """
    文章编辑表单
    用于创建和编辑文章
    """
    title = StringField('标题', validators=[
        DataRequired(message='请输入文章标题'),
        Length(min=1, max=200, message='标题长度必须在1-200个字符之间')
    ])
    summary = TextAreaField('摘要', validators=[
        Optional(),
        Length(max=500, message='摘要不能超过500个字符')
    ])
    content = TextAreaField('内容', validators=[
        DataRequired(message='请输入文章内容')
    ])
    category_id = SelectField('分类', coerce=int, validators=[
        Optional()
    ])
    tags = StringField('标签', validators=[
        Optional(),
        Length(max=200, message='标签不能超过200个字符')
    ])
    is_published = BooleanField('立即发布')
    
    def __init__(self, *args, **kwargs):
        """
        初始化表单，加载分类选项
        """
        super(PostForm, self).__init__(*args, **kwargs)
        # 动态加载分类选项
        self.category_id.choices = [(0, '无分类')] + [
            (c.id, c.name) for c in Category.query.order_by(Category.name).all()
        ]
    
    def validate_category_id(self, field):
        """
        验证分类ID是否有效
        
        Args:
            field: 分类ID字段
            
        Raises:
            ValidationError: 分类不存在时抛出
        """
        if field.data and field.data != 0:
            category = Category.query.get(field.data)
            if not category:
                raise ValidationError('所选分类不存在')


class CategoryForm(FlaskForm):
    """
    分类管理表单
    用于创建和编辑分类
    """
    name = StringField('分类名称', validators=[
        DataRequired(message='请输入分类名称'),
        Length(min=1, max=50, message='分类名称长度必须在1-50个字符之间')
    ])
    description = TextAreaField('分类描述', validators=[
        Optional(),
        Length(max=200, message='描述不能超过200个字符')
    ])
    
    def __init__(self, original_name=None, *args, **kwargs):
        """
        初始化表单
        
        Args:
            original_name: 原始分类名称（用于编辑时验证）
        """
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
    
    def validate_name(self, field):
        """
        验证分类名称是否已存在
        
        Args:
            field: 分类名称字段
            
        Raises:
            ValidationError: 分类名称已存在时抛出
        """
        if self.original_name and field.data == self.original_name:
            return
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('该分类名称已存在')


class CommentForm(FlaskForm):
    """
    评论表单
    用于提交文章评论
    """
    content = TextAreaField('评论内容', validators=[
        DataRequired(message='请输入评论内容'),
        Length(min=1, max=2000, message='评论内容长度必须在1-2000个字符之间')
    ])
    parent_id = HiddenField('回复ID', default=0)
    
    def validate_parent_id(self, field):
        """
        验证父评论ID是否有效
        
        Args:
            field: 父评论ID字段
            
        Raises:
            ValidationError: 父评论不存在时抛出
        """
        if field.data and int(field.data) > 0:
            from app.models import Comment
            parent = Comment.query.get(int(field.data))
            if not parent:
                raise ValidationError('回复的评论不存在')


class SearchForm(FlaskForm):
    """
    搜索表单
    用于搜索文章
    """
    keyword = StringField('搜索', validators=[
        DataRequired(message='请输入搜索关键词'),
        Length(min=1, max=100, message='搜索关键词长度必须在1-100个字符之间')
    ])


class ContactForm(FlaskForm):
    """
    联系表单
    用于访客联系网站管理员
    """
    name = StringField('姓名', validators=[
        DataRequired(message='请输入姓名'),
        Length(min=1, max=50, message='姓名长度必须在1-50个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱'),
        Email(message='请输入有效的邮箱地址')
    ])
    subject = StringField('主题', validators=[
        DataRequired(message='请输入主题'),
        Length(min=1, max=100, message='主题长度必须在1-100个字符之间')
    ])
    message = TextAreaField('内容', validators=[
        DataRequired(message='请输入内容'),
        Length(min=10, max=2000, message='内容长度必须在10-2000个字符之间')
    ])
