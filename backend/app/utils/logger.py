# -*- coding: utf-8 -*-
"""
日志工具模块
"""

import time
import json
from flask import request, g
from app.models.log import APILog
from app import db


class APILogger:
    """API日志记录器"""
    
    @staticmethod
    def before_request():
        """请求前处理"""
        g.start_time = time.time()
    
    @staticmethod
    def after_request(response):
        """请求后处理"""
        try:
            # 计算响应时间
            response_time = time.time() - g.get('start_time', time.time())
            
            # 获取当前用户ID
            user_id = None
            if hasattr(g, 'user_id'):
                user_id = g.user_id
            
            # 获取请求数据
            request_data = None
            if request.is_json:
                try:
                    request_data = json.dumps(request.get_json(), ensure_ascii=False)
                except:
                    pass
            
            # 获取响应数据
            response_data = None
            if response.is_json:
                try:
                    response_data = json.dumps(response.get_json(), ensure_ascii=False)
                except:
                    pass
            
            # 创建日志记录
            log = APILog(
                method=request.method,
                path=request.path,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string if request.user_agent else None,
                user_id=user_id,
                status_code=response.status_code,
                response_time=round(response_time, 4),
                request_data=request_data[:1000] if request_data else None,  # 限制长度
                response_data=response_data[:1000] if response_data else None
            )
            
            db.session.add(log)
            db.session.commit()
            
        except Exception as e:
            # 日志记录失败不影响正常请求
            db.session.rollback()
            print(f"日志记录失败: {e}")
        
        return response
