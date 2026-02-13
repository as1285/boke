# 前端Dockerfile
# 使用Node.js 18官方镜像构建，Nginx运行

# 构建阶段
FROM node:18-alpine AS builder

# 设置工作目录
WORKDIR /app

# 复制package.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目代码
COPY . .

# 构建生产环境
RUN npm run build

# 运行阶段
FROM nginx:alpine

# 复制Nginx配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制构建好的文件
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
