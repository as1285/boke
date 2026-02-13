# -*- coding: utf-8 -*-
"""
测试技术资源路由
"""

from flask import Blueprint, request

from app import db
from app.models import TestTechResource
from app.schemas import TestTechResourceSchema

tech_bp = Blueprint('tech', __name__)

tech_resource_schema = TestTechResourceSchema()
tech_resources_schema = TestTechResourceSchema(many=True)


def api_response(code=200, msg='操作成功', data=None):
    """统一API响应格式"""
    return {'code': code, 'msg': msg, 'data': data}


@tech_bp.route('/test-tech-resources', methods=['GET'])
def get_test_tech_resources():
    """获取测试技术资源列表（公开）"""
    category = request.args.get('category')
    is_recommended = request.args.get('is_recommended', type=lambda x: x.lower() == 'true')
    
    query = TestTechResource.query
    
    if category:
        query = query.filter_by(category=category)
    if is_recommended is not None:
        query = query.filter_by(is_recommended=is_recommended)
    
    # 按分类和排序号排序
    resources = query.order_by(
        TestTechResource.category,
        TestTechResource.sort_order
    ).all()
    
    # 按分类分组
    result = {}
    for resource in resources:
        cat = resource.category
        if cat not in result:
            result[cat] = {
                'category': cat,
                'resources': []
            }
        result[cat]['resources'].append(resource.to_dict())
    
    return api_response(200, '获取成功', list(result.values()))


@tech_bp.route('/test-tech-resources/categories', methods=['GET'])
def get_categories():
    """获取所有分类（公开）"""
    categories = db.session.query(TestTechResource.category).distinct().all()
    return api_response(200, '获取成功', [c[0] for c in categories])


@tech_bp.route('/test-tech-resources/<int:id>', methods=['GET'])
def get_resource(id):
    """获取单个资源详情（公开）"""
    resource = TestTechResource.query.get_or_404(id)
    return api_response(200, '获取成功', resource.to_dict())
