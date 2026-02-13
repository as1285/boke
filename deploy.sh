#!/bin/bash
# -*- coding: utf-8 -*-
"""
部署脚本
一键构建和部署Docker容器
"""

set -e

echo "=========================================="
echo "Flask博客系统 - Docker部署脚本"
echo "=========================================="

# 检查Docker和Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

echo "✅ Docker环境检查通过"

# 创建数据目录
mkdir -p data nginx/ssl

# 停止旧容器
echo ""
echo "【1/5】停止旧容器..."
docker-compose down --remove-orphans 2>/dev/null || true

# 构建镜像
echo ""
echo "【2/5】构建Docker镜像..."
docker-compose build --no-cache

# 启动服务
echo ""
echo "【3/5】启动服务..."
docker-compose up -d

# 等待服务启动
echo ""
echo "【4/5】等待服务启动..."
sleep 5

# 检查服务状态
echo ""
echo "【5/5】检查服务状态..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ 服务启动成功！"
    echo ""
    echo "访问地址："
    echo "  前端: http://localhost"
    echo "  后端: http://localhost:5000"
    echo ""
    echo "查看日志："
    echo "  docker-compose logs -f"
    echo ""
    echo "停止服务："
    echo "  docker-compose down"
else
    echo "❌ 服务启动失败，请检查日志："
    echo "  docker-compose logs"
    exit 1
fi

echo "=========================================="
echo "部署完成！"
echo "=========================================="
