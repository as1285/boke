# -*- coding: utf-8 -*-
"""
JWT调试脚本
"""

import sys
sys.path.insert(0, 'backend')

from flask_jwt_extended import create_access_token, decode_token
from app import create_app

app = create_app()

with app.app_context():
    # 创建测试Token
    user_id = 1
    token = create_access_token(identity=user_id)
    print(f"生成的Token: {token[:50]}...")
    print(f"Token长度: {len(token)}")
    
    # 解码Token查看内容
    try:
        decoded = decode_token(token)
        print(f"\nToken解码成功:")
        print(f"  sub (identity): {decoded.get('sub')}")
        print(f"  exp: {decoded.get('exp')}")
        print(f"  iat: {decoded.get('iat')}")
        print(f"  jti: {decoded.get('jti')}")
        print(f"  type: {decoded.get('type')}")
    except Exception as e:
        print(f"\nToken解码失败: {e}")
    
    # 检查JWT密钥
    print(f"\nJWT配置:")
    print(f"  JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY', 'Not Set')[:20]}...")
    print(f"  JWT_ACCESS_TOKEN_EXPIRES: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES')}")
