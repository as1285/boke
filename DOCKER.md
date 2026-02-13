# Docker 部署指南

本文档介绍如何使用 Docker 部署 Flask 博客系统。

## 📋 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- 服务器内存：建议 1GB+
- 服务器磁盘：建议 10GB+

## 🚀 快速部署

### 1. 克隆项目到服务器

```bash
git clone https://github.com/your-repo/flask-blog.git
cd flask-blog
```

### 2. 运行部署脚本

```bash
chmod +x deploy.sh
./deploy.sh
```

部署脚本会自动完成以下操作：
1. 检查 Docker 环境
2. 创建数据目录
3. 构建 Docker 镜像
4. 启动服务
5. 检查服务状态

### 3. 访问应用

部署完成后，访问以下地址：

- **前台页面**: http://localhost
- **后台管理**: http://localhost/admin
- **后端API**: http://localhost:5000

## 🔧 手动部署

如果不想使用部署脚本，可以手动执行：

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## ⚙️ 配置说明

### 环境变量

在 `docker-compose.yml` 中可以配置以下环境变量：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `JWT_SECRET_KEY` | your-secret-key | JWT密钥，生产环境务必修改 |
| `DATABASE_URL` | sqlite:///data/app.db | 数据库地址 |
| `FLASK_ENV` | production | Flask环境 |

### 数据持久化

- **数据库**: 挂载到 `./data` 目录
- **Nginx配置**: 挂载到 `./nginx` 目录

## 🌐 生产环境部署

### 使用Nginx反向代理

```bash
# 启动生产环境配置
docker-compose --profile production up -d
```

### 配置HTTPS

1. 将SSL证书放入 `nginx/ssl` 目录：
   - `cert.pem` - 证书文件
   - `key.pem` - 私钥文件

2. 修改 `nginx/nginx.conf`，取消HTTPS配置的注释

3. 重启服务：
   ```bash
   docker-compose restart nginx
   ```

## 📊 常用命令

```bash
# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 重启服务
docker-compose restart

# 进入容器
docker-compose exec backend bash
docker-compose exec frontend sh

# 更新代码后重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🐛 故障排查

### 服务无法启动

```bash
# 查看详细日志
docker-compose logs

# 检查端口占用
netstat -tlnp | grep -E '80|5000'
```

### 数据库问题

```bash
# 进入后端容器
docker-compose exec backend bash

# 查看数据库
ls -la data/
```

### 前端无法访问API

检查Nginx配置：
```bash
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
```

## 🔒 安全建议

1. **修改JWT密钥**: 在 `docker-compose.yml` 中设置强密码
2. **启用HTTPS**: 生产环境务必使用HTTPS
3. **限制端口暴露**: 只暴露必要的端口
4. **定期备份数据**: 备份 `./data` 目录

## 📦 镜像说明

| 服务 | 镜像 | 说明 |
|------|------|------|
| backend | python:3.11-slim | Flask后端服务 |
| frontend | nginx:alpine | Vue前端静态文件 |
| nginx | nginx:alpine | 反向代理（可选） |

## 📝 更新日志

### v1.0.0 (2026-02-13)
- ✅ 支持Docker容器化部署
- ✅ 支持Docker Compose编排
- ✅ 支持Nginx反向代理
- ✅ 支持HTTPS配置
