# -*- coding: utf-8 -*-
"""
前端开发服务器
使用Flask提供前端静态文件服务，替代Node.js/npm
"""

from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='frontend/dist')

# CORS配置
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 代理API请求到后端
import requests

BACKEND_URL = "http://localhost:5000"

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_api(path):
    """代理API请求到后端服务器"""
    url = f"{BACKEND_URL}/api/{path}"
    method = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    return method.content, method.status_code, method.headers.items()

@app.route('/')
def index():
    """首页"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask博客系统</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f5f5f5;
            }
            .header {
                background: #fff;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 15px 0;
            }
            .header-content {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0 20px;
