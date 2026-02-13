# Flask + Vue 前后端分离博客系统

<p align="center">
  <img src="https://img.shields.io/badge/Flask-3.0-blue?style=flat-square&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Vue-3.4-green?style=flat-square&logo=vuedotjs" alt="Vue">
  <img src="https://img.shields.io/badge/Element_Plus-2.5-blue?style=flat-square&logo=element" alt="Element Plus">
  <img src="https://img.shields.io/badge/JWT-Auth-orange?style=flat-square" alt="JWT">
  <img src="https://img.shields.io/badge/Markdown-Editor-yellow?style=flat-square" alt="Markdown">
</p>

<p align="center">
  基于 Python Flask + Vue 3 开发的前后端分离个人博客系统<br>
  包含博客核心功能 + 测试技术资源导航 + 系统管理工具
</p>

## ✨ 功能特性

### 核心博客功能
- 🔐 **用户认证** - JWT Token认证，支持登录/注册
- 📝 **文章管理** - Markdown编辑器，支持实时预览
- 🏷️ **分类标签** - 文章分类和标签管理
- 💬 **评论系统** - 文章评论功能
- 🔍 **文章搜索** - 支持关键词搜索
- 📱 **响应式设计** - 适配移动端和桌面端

### 扩展功能
- 🧪 **测试技术资源** - 汇总40+主流测试技术网站，分类导航
- 📊 **API调用日志** - 记录所有API请求，支持筛选和统计
- 📚 **接口文档** - 系统接口文档在线查看
- 👥 **用户管理** - 管理员查看用户信息、登录记录
- 🔒 **登录记录** - 记录用户登录IP和时间

## 🛠️ 技术栈

### 后端 (Backend)
| 技术 | 版本 | 说明 |
|------|------|------|
| Flask | 3.0 | Web框架 |
| Flask-SQLAlchemy | 3.1 | ORM数据库操作 |
| Flask-JWT-Extended | 4.6 | JWT认证 |
| Flask-Marshmallow | 0.15 | 数据序列化 |
| Flask-CORS | 4.0 | 跨域支持 |
| Python-Markdown | 3.5 | Markdown渲染 |
| Bleach | 6.1 | HTML安全过滤 |

### 前端 (Frontend)
| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.4 | 前端框架 |
| Vue Router | 4.2 | 路由管理 |
| Pinia | 2.1 | 状态管理 |
| Element Plus | 2.5 | UI组件库 |
| mavon-editor | 3.0 | Markdown编辑器 |
| Axios | 1.6 | HTTP客户端 |
| Vite | 5.0 | 构建工具 |

## 📁 项目结构

```
flask-blog/
├── 📂 backend/                    # 后端项目
│   ├── 📂 app/
│   │   ├── 📄 __init__.py        # Flask应用初始化
│   │   ├── 📂 config/            # 配置文件
│   │   ├── 📂 models/            # 数据库模型
│   │   │   ├── user.py          # 用户模型
│   │   │   ├── post.py          # 文章/分类/标签模型
│   │   │   ├── comment.py       # 评论模型
│   │   │   ├── log.py           # API日志模型
│   │   │   ├── login_log.py     # 登录日志模型
│   │   │   └── tech_resource.py # 测试技术资源模型
│   │   ├── 📂 schemas/           # Marshmallow序列化器
│   │   ├── 📂 routes/            # API路由
│   │   │   ├── auth.py          # 认证路由
│   │   │   ├── posts.py         # 文章路由
│   │   │   ├── comments.py      # 评论路由
│   │   │   ├── tags.py          # 分类标签路由
│   │   │   ├── admin.py         # 管理后台路由
│   │   │   └── tech.py          # 测试技术资源路由
│   │   └── 📂 utils/             # 工具函数
│   │       └── logger.py        # API日志中间件
│   ├── 📄 requirements.txt       # Python依赖
│   └── 📄 run.py                 # 启动入口
│
└── 📂 frontend/                   # 前端项目
    ├── 📂 src/
    │   ├── 📂 api/               # API接口封装
    │   ├── 📂 components/        # 公共组件
    │   ├── 📂 layouts/           # 布局组件
    │   │   ├── MainLayout.vue   # 前台布局
    │   │   └── AdminLayout.vue  # 后台布局
    │   ├── 📂 pages/             # 页面组件
    │   │   ├── 📄 Home.vue       # 首页
    │   │   ├── 📄 PostDetail.vue # 文章详情
    │   │   ├── 📄 TestTech.vue   # 测试技术资源
    │   │   ├── 📄 Login.vue      # 登录
    │   │   └── 📂 admin/         # 后台管理
    │   │       ├── Dashboard.vue    # 控制台
    │   │       ├── Posts.vue        # 文章管理
    │   │       ├── PostEdit.vue     # 文章编辑
    │   │       ├── Logs.vue         # API日志
    │   │       ├── ApiDocs.vue      # 接口文档
    │   │       └── Users.vue        # 用户管理
    │   ├── 📂 router/            # Vue Router配置
    │   ├── 📂 stores/            # Pinia状态管理
    │   └── 📂 utils/             # 工具函数
    ├── 📄 package.json           # Node.js依赖
    └── 📄 vite.config.js         # Vite配置
```

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+
- MySQL 5.7+ (可选，默认使用SQLite)

### 1️⃣ 后端部署

#### 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 启动服务
```bash
# 开发模式
python run.py

# 生产模式
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

服务启动后访问：http://localhost:5000

### 2️⃣ 前端部署

#### 安装依赖
```bash
cd frontend
npm install
```

#### 开发模式
```bash
npm run dev
```

访问：http://localhost:5173

#### 生产构建
```bash
npm run build
```

### 3️⃣ 初始化数据

```bash
# 创建管理员账号和测试数据
python create_test_post.py
```

默认管理员账号：`admin` / `admin123`

## 📸 功能预览

### 前台页面
- **首页** - 文章列表、搜索功能
- **文章详情** - Markdown渲染、评论展示
- **🧪 测试技术** - 40+测试技术网站导航
- **分类/标签** - 按分类或标签筛选文章
- **归档** - 按时间归档展示

### 后台管理
- **控制台** - 数据统计概览
- **文章管理** - 创建/编辑/删除文章
- **📊 日志模块** - API调用日志查看、筛选、统计
- **📚 接口文档** - 系统接口文档在线查看
- **👥 用户管理** - 用户信息、登录记录管理

## 📡 API文档

### 认证接口
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/auth/register` | 用户注册 | 公开 |
| POST | `/api/auth/login` | 用户登录 | 公开 |
| GET | `/api/auth/me` | 获取当前用户 | 登录用户 |

### 文章接口
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/posts` | 文章列表 | 公开 |
| GET | `/api/posts/{slug}` | 文章详情 | 公开 |
| POST | `/api/posts` | 创建文章 | 管理员 |
| PUT | `/api/posts/{id}` | 更新文章 | 管理员 |
| DELETE | `/api/posts/{id}` | 删除文章 | 管理员 |

### 测试技术资源接口
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/test-tech-resources` | 获取测试技术资源列表 | 公开 |
| GET | `/api/test-tech-resources/categories` | 获取分类列表 | 公开 |

### 管理后台接口
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/admin/logs` | API调用日志 | 管理员 |
| GET | `/api/admin/logs/stats` | 日志统计 | 管理员 |
| GET | `/api/admin/api-docs` | 接口文档 | 管理员 |
| GET | `/api/admin/users` | 用户列表 | 管理员 |
| GET | `/api/admin/users/stats` | 用户统计 | 管理员 |

## 🧪 测试技术资源分类

| 分类 | 数量 | 代表工具 |
|------|------|----------|
| 自动化测试框架 | 7 | Selenium, Cypress, Playwright, Pytest |
| API测试工具 | 5 | Postman, Swagger, REST Assured |
| 性能测试工具 | 4 | JMeter, Gatling, k6, Locust |
| 测试管理工具 | 3 | TestRail, Zephyr, TestLink |
| 持续集成 | 4 | Jenkins, GitHub Actions, GitLab CI |
| 代码质量 | 3 | SonarQube, Codecov |
| 安全测试 | 3 | OWASP ZAP, Burp Suite, Snyk |
| 移动测试 | 3 | Espresso, XCUITest, Detox |
| 测试社区 | 4 | Ministry of Testing, TesterHome |

## 🔧 核心实现

### JWT认证流程
```
1. 用户登录 → 后端验证 → 返回JWT Token
2. 前端存储Token到localStorage
3. 请求时Header携带: Authorization: Bearer <token>
4. 后端验证Token有效性
5. Token过期后需重新登录
```

### API日志记录
```
请求进入 → 日志中间件记录请求信息
                ↓
请求处理 → 后端执行业务逻辑
                ↓
响应返回 → 日志中间件记录响应信息
                ↓
          保存到数据库(APILog表)
```

### 登录记录
```
用户登录成功 → 创建LoginLog记录
                ↓
          记录用户ID、IP、时间
                ↓
          用户管理页面展示最近登录
```

## ⚙️ 配置说明

### 后端配置
```python
# JWT密钥（生产环境务必修改）
JWT_SECRET_KEY = 'your-secret-key'

# Token过期时间
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

# CORS配置
CORS_ORIGINS = ['http://localhost:5173']

# 数据库
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
```

### 前端配置
```javascript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true
    }
  }
}
```

## 🐛 常见问题

### 跨域问题
- 检查后端CORS配置中的`CORS_ORIGINS`
- 检查前端`vite.config.js`中的proxy配置

### Token验证失败
- 确保`Authorization` Header格式：`Bearer <token>`
- 检查Token是否过期
- 确认JWT密钥一致

## 📝 更新日志

### v1.1.0 (2026-02-13)
- ✅ 新增测试技术资源模块
- ✅ 新增API调用日志模块
- ✅ 新增接口文档模块
- ✅ 新增用户管理模块
- ✅ 新增登录记录功能

### v1.0.0 (2026-02-13)
- ✅ 基础博客功能
- ✅ 用户认证（JWT）
- ✅ 文章CRUD
- ✅ Markdown编辑器
- ✅ 评论系统

## 📄 许可证

MIT License

---

<p align="center">
  如果这个项目对你有帮助，欢迎 ⭐ Star！
</p>
