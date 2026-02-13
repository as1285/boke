#!/bin/bash
# -*- coding: utf-8 -*-
"""
服务器自动部署脚本
由GitHub Actions调用或手动执行
"""

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 项目配置
PROJECT_DIR="/opt/flask-blog"
BACKUP_DIR="/opt/backups"
LOG_FILE="/var/log/blog-deploy.log"

# 记录日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 备份当前版本
backup_current() {
    log "备份当前版本..."
    
    if [[ -d "$PROJECT_DIR" ]]; then
        local backup_name="blog_$(date +%Y%m%d_%H%M%S).tar.gz"
        mkdir -p "$BACKUP_DIR"
        
        cd "$PROJECT_DIR"
        tar -czf "${BACKUP_DIR}/${backup_name}" data 2>/dev/null || true
        
        log "备份完成: ${backup_name}"
        
        # 保留最近10个备份
        ls -t ${BACKUP_DIR}/blog_*.tar.gz 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null || true
    fi
}

# 拉取最新代码
pull_code() {
    log "拉取最新代码..."
    
    cd "$PROJECT_DIR"
    
    # 保存本地修改（如果有）
    git stash 2>/dev/null || true
    
    # 拉取最新代码
    git pull origin master
    
    log "代码更新完成"
}

# 部署服务
deploy_services() {
    log "开始部署服务..."
    
    cd "$PROJECT_DIR"
    
    # 停止旧服务
    log "停止旧服务..."
    docker-compose down
    
    # 拉取最新镜像
    log "拉取最新镜像..."
    docker-compose pull
    
    # 构建新镜像
    log "构建新镜像..."
    docker-compose build --no-cache
    
    # 启动服务
    log "启动服务..."
    docker-compose up -d
    
    # 清理旧镜像
    log "清理旧镜像..."
    docker image prune -f
    
    log "服务部署完成"
}

# 健康检查
health_check() {
    log "执行健康检查..."
    
    local max_attempts=30
    local attempt=1
    local backend_ok=false
    local frontend_ok=false
    
    while [ $attempt -le $max_attempts ]; do
        # 检查后端
        if ! $backend_ok && curl -s http://localhost:5000/api/posts > /dev/null 2>&1; then
            backend_ok=true
            log "✅ 后端服务正常"
        fi
        
        # 检查前端
        if ! $frontend_ok && curl -s http://localhost > /dev/null 2>&1; then
            frontend_ok=true
            log "✅ 前端服务正常"
        fi
        
        # 都正常则退出
        if $backend_ok && $frontend_ok; then
            log "✅ 所有服务运行正常"
            return 0
        fi
        
        log "等待服务启动... ($attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    log "❌ 健康检查失败"
    return 1
}

# 发送通知（可选）
send_notification() {
    local status=$1
    local message=$2
    
    log "发送通知: $status - $message"
    
    # 这里可以添加钉钉、企业微信、Slack等通知
    # 示例：钉钉机器人
    # curl -X POST "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN" \
    #   -H "Content-Type: application/json" \
    #   -d "{\"msgtype\": \"text\", \"text\": {\"content\": \"部署$status: $message\"}}"
}

# 回滚功能
rollback() {
    log "开始回滚..."
    
    # 找到最新的备份
    local latest_backup=$(ls -t ${BACKUP_DIR}/blog_*.tar.gz 2>/dev/null | head -1)
    
    if [[ -f "$latest_backup" ]]; then
        log "使用备份: $latest_backup"
        
        cd "$PROJECT_DIR"
        docker-compose down
        
        # 恢复数据
        tar -xzf "$latest_backup" -C "$PROJECT_DIR"
        
        # 重新部署
        docker-compose up -d
        
        log "回滚完成"
    else
        log "❌ 没有找到备份文件"
        return 1
    fi
}

# 主函数
main() {
    log "=========================================="
    log "开始自动部署"
    log "=========================================="
    
    local start_time=$(date +%s)
    
    # 执行部署步骤
    if backup_current && pull_code && deploy_services && health_check; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        log "=========================================="
        log "✅ 部署成功！耗时: ${duration}秒"
        log "=========================================="
        
        send_notification "成功" "部署完成，耗时${duration}秒"
        
        return 0
    else
        log "=========================================="
        log "❌ 部署失败"
        log "=========================================="
        
        send_notification "失败" "部署过程中出现错误"
        
        # 询问是否回滚
        read -p "是否回滚到上一版本? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rollback
        fi
        
        return 1
    fi
}

# 执行主函数
main "$@"
