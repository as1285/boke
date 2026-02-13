#!/bin/bash
# -*- coding: utf-8 -*-
"""
服务器一键部署脚本
在服务器上执行此脚本即可自动部署整个博客系统
"""

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
PROJECT_NAME="flask-blog"
GITHUB_REPO="https://github.com/as1285/boke.git"
INSTALL_DIR="/opt/${PROJECT_NAME}"
BACKUP_DIR="/opt/backups"

# 打印带颜色的信息
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

# 检查是否为root用户
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "请使用 root 用户执行此脚本"
        exit 1
    fi
}

# 检查系统要求
check_requirements() {
    print_info "检查系统要求..."
    
    # 检查操作系统
    if [[ ! -f /etc/os-release ]]; then
        print_error "无法识别操作系统"
        exit 1
    fi
    
    source /etc/os-release
    print_info "操作系统: $NAME $VERSION_ID"
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        print_warning "Docker未安装，正在安装..."
        install_docker
    else
        print_success "Docker已安装: $(docker --version)"
    fi
    
    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_warning "Docker Compose未安装，正在安装..."
        install_docker_compose
    else
        print_success "Docker Compose已安装: $(docker-compose --version)"
    fi
    
    # 检查Git
    if ! command -v git &> /dev/null; then
        print_warning "Git未安装，正在安装..."
        apt-get update && apt-get install -y git
    else
        print_success "Git已安装: $(git --version)"
    fi
    
    # 检查端口
    check_ports
}

# 安装Docker
install_docker() {
    print_info "安装Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    usermod -aG docker $SUDO_USER 2>/dev/null || true
    print_success "Docker安装完成"
}

# 安装Docker Compose
install_docker_compose() {
    print_info "安装Docker Compose..."
    DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    print_success "Docker Compose安装完成"
}

# 检查端口占用
check_ports() {
    print_info "检查端口占用..."
    local ports=(80 443 5000)
    for port in "${ports[@]}"; do
        if netstat -tuln | grep -q ":$port "; then
            print_warning "端口 $port 已被占用"
            read -p "是否继续部署? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        else
            print_success "端口 $port 可用"
        fi
    done
}

# 备份现有数据
backup_existing() {
    if [[ -d "$INSTALL_DIR" ]]; then
        print_warning "发现现有安装，正在备份..."
        mkdir -p "$BACKUP_DIR"
        local backup_name="${PROJECT_NAME}_$(date +%Y%m%d_%H%M%S).tar.gz"
        tar -czf "${BACKUP_DIR}/${backup_name}" -C "$(dirname $INSTALL_DIR)" "$(basename $INSTALL_DIR)"
        print_success "备份完成: ${BACKUP_DIR}/${backup_name}"
        
        # 停止旧服务
        cd "$INSTALL_DIR" && docker-compose down 2>/dev/null || true
    fi
}

# 克隆代码
clone_code() {
    print_info "克隆代码..."
    
    # 如果目录存在，先删除
    if [[ -d "$INSTALL_DIR" ]]; then
        rm -rf "$INSTALL_DIR"
    fi
    
    # 创建目录
    mkdir -p "$INSTALL_DIR"
    
    # 克隆代码
    git clone "$GITHUB_REPO" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    print_success "代码克隆完成"
}

# 配置环境
setup_environment() {
    print_info "配置环境..."
    
    # 创建数据目录
    mkdir -p data nginx/ssl
    
    # 生成随机JWT密钥
    JWT_SECRET=$(openssl rand -base64 32)
    
    # 创建环境变量文件
    cat > .env << EOF
# 生产环境配置
FLASK_ENV=production
JWT_SECRET_KEY=${JWT_SECRET}
DATABASE_URL=sqlite:///data/app.db

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=5000

# 日志级别
LOG_LEVEL=INFO
EOF
    
    print_success "环境配置完成"
    print_info "JWT密钥已生成: ${JWT_SECRET:0:20}..."
}

# 构建和启动服务
build_and_start() {
    print_info "构建Docker镜像..."
    cd "$INSTALL_DIR"
    
    # 拉取最新镜像
    docker-compose pull
    
    # 构建镜像
    docker-compose build --no-cache
    
    print_success "镜像构建完成"
    
    # 启动服务
    print_info "启动服务..."
    docker-compose up -d
    
    # 等待服务启动
    print_info "等待服务启动..."
    sleep 10
    
    # 检查服务状态
    check_service_status
}

# 检查服务状态
check_service_status() {
    print_info "检查服务状态..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:5000/api/posts > /dev/null 2>&1; then
            print_success "后端服务运行正常"
            break
        fi
        
        print_info "等待服务启动... ($attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        print_error "服务启动超时"
        print_info "查看日志: docker-compose logs"
        exit 1
    fi
    
    # 检查前端
    if curl -s http://localhost > /dev/null 2>&1; then
        print_success "前端服务运行正常"
    fi
}

# 设置定时备份
setup_backup_cron() {
    print_info "设置定时备份..."
    
    # 创建备份脚本
    cat > /usr/local/bin/backup-blog.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
INSTALL_DIR="/opt/flask-blog"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"
cd "$INSTALL_DIR"

# 备份数据库
docker-compose exec -T backend tar czf - data > "${BACKUP_DIR}/blog_data_${DATE}.tar.gz"

# 保留最近7天的备份
find "$BACKUP_DIR" -name "blog_data_*.tar.gz" -mtime +7 -delete
EOF
    
    chmod +x /usr/local/bin/backup-blog.sh
    
    # 添加到crontab（每天凌晨2点备份）
    (crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-blog.sh >> /var/log/blog-backup.log 2>&1") | crontab -
    
    print_success "定时备份已设置（每天凌晨2点）"
}

# 显示访问信息
show_access_info() {
    local server_ip=$(hostname -I | awk '{print $1}')
    
    echo ""
    echo "=========================================="
    echo "  🎉 部署完成！"
    echo "=========================================="
    echo ""
    echo "📍 访问地址:"
    echo "   前台页面: http://${server_ip}"
    echo "   后台管理: http://${server_ip}/admin"
    echo "   API文档:  http://${server_ip}:5000"
    echo ""
    echo "🔑 默认管理员账号:"
    echo "   用户名: admin"
    echo "   密码: admin123"
    echo ""
    echo "📁 项目目录: ${INSTALL_DIR}"
    echo "💾 数据目录: ${INSTALL_DIR}/data"
    echo "📋 日志查看: docker-compose logs -f"
    echo ""
    echo "⚡ 常用命令:"
    echo "   停止服务: docker-compose down"
    echo "   重启服务: docker-compose restart"
    echo "   查看状态: docker-compose ps"
    echo "   更新代码: cd ${INSTALL_DIR} && git pull && docker-compose up -d --build"
    echo ""
    echo "=========================================="
}

# 主函数
main() {
    echo "=========================================="
    echo "  Flask + Vue 博客系统 - 服务器部署"
    echo "=========================================="
    echo ""
    
    check_root
    check_requirements
    backup_existing
    clone_code
    setup_environment
    build_and_start
    setup_backup_cron
    show_access_info
}

# 执行主函数
main "$@"
