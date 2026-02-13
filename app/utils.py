# -*- coding: utf-8 -*-
"""
工具函数模块
包含模板过滤器和其他辅助函数
"""

from datetime import datetime
from markdown import markdown
import bleach


def markdown_filter(text):
    """
    Markdown转HTML模板过滤器
    
    Args:
        text: Markdown格式的文本
        
    Returns:
        str: 渲染后的HTML
    """
    if not text:
        return ''
    
    # 允许的HTML标签
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img'
    ]
    allowed_attributes = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title']
    }
    
    # 渲染Markdown
    html = markdown(
        text,
        extensions=['extra', 'codehilite', 'toc']
    )
    
    # 清理HTML，防止XSS
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes
    )
    
    return clean_html


def timesince_filter(dt):
    """
    时间差过滤器
    显示距离现在的时间差（如：2小时前、3天前）
    
    Args:
        dt: 日期时间对象
        
    Returns:
        str: 时间差描述
    """
    if not dt:
        return ''
    
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return '刚刚'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes}分钟前'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours}小时前'
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f'{days}天前'
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f'{weeks}周前'
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f'{months}个月前'
    else:
        years = int(seconds / 31536000)
        return f'{years}年前'
