# CI/CD 持续集成/持续部署指南

本文档介绍如何配置 CI/CD 流程，实现代码推送到 GitHub 后自动部署到服务器。

## 🔄 CI/CD 流程概览

```
代码推送 → GitHub Actions → 构建测试 → SSH部署 → 服务器更新 → 健康检查
```

## 📋 配置步骤

### 1. 配置 GitHub Secrets

在 GitHub 仓库的 Settings → Secrets and variables → Actions 中添加以下密钥：

| Secret 名称 | 说明 | 获取方式 |
|------------|------|---------|
| `SSH_PRIVATE_KEY` | 服务器SSH私钥 | `cat ~/.ssh/id_rsa` |
| `SERVER_IP` | 服务器IP地址 | 你的服务器公网IP |
| `SERVER_USER` | 服务器用户名 | 通常是 `root` 或部署用户 |

#### 生成SSH密钥对

在服务器上执行：

```bash
# 生成密钥对（如果还没有）
ssh-keygen -t rsa -b 4096 -C "github-actions"

# 查看公钥并添加到 authorized_keys
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# 查看私钥（复制到 GitHub Secrets）
cat ~/.ssh/id_rsa
```

### 2. GitHub Actions 工作流

已创建 `.github/workflows/deploy.yml`，包含以下步骤：

#### 构建和测试阶段
- ✅ 检出代码
- ✅ 设置 Python 3.11 环境
- ✅ 安装后端依赖
- ✅ 后端代码检查（flake8）
- ✅ 设置 Node.js 18 环境
- ✅ 安装前端依赖
- ✅ 前端代码检查
- ✅ 构建前端
- ✅ 上传构建产物

#### 部署阶段
- ✅ 配置 SSH 密钥
- ✅ 连接服务器
- ✅ 执行部署脚本
- ✅ 健康检查
- ✅ 发送通知

### 3. 服务器配置

确保服务器上已安装：

```bash
# Docker
docker --version

# Docker Compose
docker-compose --version

# Git
git --version
```

### 4. 部署脚本

服务器上的自动部署脚本：`/opt/flask-blog/deploy-auto.sh`

功能包括：
- 备份当前数据
- 拉取最新代码
- 重新构建镜像
- 启动服务
- 健康检查
- 失败回滚

## 🚀 使用方式

### 自动部署

1. 本地修改代码
2. 提交并推送到 GitHub
   ```bash
   git add .
   git commit -m "更新功能"
   git push origin master
   ```
3. GitHub Actions 自动触发部署
4. 查看部署状态：GitHub → Actions 标签页

### 手动部署

在服务器上执行：

```bash
cd /opt/flask-blog
sudo bash deploy-auto.sh
```

### 查看部署日志

```bash
# 查看自动部署日志
tail -f /var/log/blog-deploy.log

# 查看Docker日志
docker-compose logs -f
```

## 📊 部署状态监控

### GitHub Actions 状态

- 绿色 ✅：部署成功
- 红色 ❌：部署失败
- 黄色 🟡：正在部署

### 查看实时日志

GitHub → Actions → 选择工作流 → 查看日志

## 🔧 常见问题

### 1. SSH连接失败

检查：
- SSH密钥是否正确添加到 Secrets
- 服务器IP是否正确
- 服务器是否允许SSH连接

### 2. 部署成功但服务无法访问

检查：
- 服务器防火墙是否开放端口
- 安全组规则（云服务器）
- Docker容器是否正常运行

```bash
# 检查容器状态
docker-compose ps

# 查看容器日志
docker-compose logs backend
docker-compose logs frontend
```

### 3. 回滚操作

如果部署失败，可以手动回滚：

```bash
cd /opt/flask-blog
sudo bash deploy-auto.sh
# 选择 y 回滚到上一版本
```

## 📝 自定义配置

### 修改触发条件

编辑 `.github/workflows/deploy.yml`：

```yaml
on:
  push:
    branches: 
      - master    # 只在master分支推送时触发
      - develop   # 添加develop分支
  pull_request:
    branches: [ master ]
```

### 添加通知

在 deploy.yml 中添加：

```yaml
# 钉钉通知
- name: DingTalk Notification
  uses: zcong1993/actions-ding@master
  with:
    dingToken: ${{ secrets.DING_TOKEN }}
    body: |
      {
        "msgtype": "markdown",
        "markdown": {
          "title": "部署通知",
          "text": "### 部署${{ job.status }}\n> 项目：Flask博客系统"
        }
      }
```

### 多环境部署

创建多个工作流文件：

- `.github/workflows/deploy-dev.yml` - 开发环境
- `.github/workflows/deploy-staging.yml` - 测试环境
- `.github/workflows/deploy-prod.yml` - 生产环境

## 🔒 安全建议

1. **保护 Secrets**：不要泄露 SSH 私钥
2. **使用 Deploy Key**：为GitHub配置专门的部署密钥
3. **限制服务器权限**：使用非root用户部署
4. **启用分支保护**：禁止直接推送master分支

## 📚 相关文档

- [GitHub Actions 文档](https://docs.github.com/cn/actions)
- [Docker 部署指南](./DOCKER.md)
- [项目 README](./README.md)
