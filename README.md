# 博客系统 (Blog System)

基于Flask的全功能博客管理系统，支持用户注册、文章发布、评论互动、管理员管理等完整功能。

## 功能特性

### 用户功能
- ✅ 用户注册和登录（支持邮箱验证）
- ✅ 个人资料管理（昵称、简介、密码修改）
- ✅ 文章发布、编辑、删除
- ✅ 文章草稿和发布状态管理
- ✅ 评论发表和管理
- ✅ 个人文章和评论列表查看

### 文章功能
- ✅ 文章分类管理
- ✅ 文章搜索（标题、内容）
- ✅ 分类筛选
- ✅ 分页浏览
- ✅ 浏览计数
- ✅ 文章状态管理（草稿、已发布、已归档）

### 评论功能
- ✅ 评论发表
- ✅ 评论回复（支持层级结构）
- ✅ 评论删除
- ✅ 评论审核状态管理

### 管理员功能
- ✅ 用户管理（查看、编辑、删除）
- ✅ 文章管理（查看、编辑、删除所有文章）
- ✅ 评论管理（审核、删除所有评论）
- ✅ 管理员仪表板

### 系统功能
- ✅ 响应式界面设计
- ✅ CSRF 保护
- ✅ XSS 防护
- ✅ SQL 注入防护
- ✅ 错误处理和日志记录
- ✅ 性能优化（缓存、查询优化）
- ✅ 静态资源压缩

## 技术栈

- **后端框架**: Python Flask 2.3.3
- **数据库**: MySQL 5.7+
- **ORM**: SQLAlchemy 3.0.5
- **认证**: Flask-Login 0.6.3
- **表单**: Flask-WTF 1.1.1 + WTForms 3.0.1
- **密码加密**: bcrypt 4.0.1
- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap 5
- **测试框架**: pytest 7.4.2 + pytest-flask 1.2.0
- **属性测试**: Hypothesis 6.88.1

## 快速开始

### 1. 环境准备

确保已安装以下软件：
- Python 3.10+ （推荐 3.10.10）
- MySQL 5.7+ 或 MariaDB 10.3+
- Git

### 2. 克隆项目

```bash
git clone <repository-url>
cd PBL_Blog
```

### 3. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置数据库

创建 `.env` 文件（参考 `.env.example`）：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=blog_system

# Flask配置
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# 其他配置
DEBUG=True
```

### 6. 创建数据库

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE blog_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 7. 初始化数据库

```bash
python init_db.py
```

### 8. 启动应用

```bash
python run.py
```

应用将在 http://127.0.0.1:5000 启动。

### 9. 生成演示数据（可选）

```bash
python seed_demo_data.py
```

这将创建：
- 1个管理员账号（admin/admin123）
- 4个普通用户
- 5个文章分类
- 5篇示例文章
- 10条示例评论

### 10. 安全检查

在部署到生产环境前，运行安全检查脚本：

```bash
python security_check.py
```

该脚本会检查：
- SECRET_KEY 配置
- 数据库密码强度
- DEBUG 模式状态
- Session 安全配置
- 文件权限

⚠️ **生产环境部署前必读**: 请查看 `PRODUCTION_SETUP.md` 了解详细的安全配置指南。

## 项目结构

```
PBL_Blog/
├── .kiro/                      # Kiro 配置和规范
│   └── specs/                  # 功能规范文档
│       └── blog-system/
│           ├── requirements.md # 需求文档
│           ├── design.md       # 设计文档
│           └── tasks.md        # 任务列表
├── app/                        # 应用主目录
│   ├── forms/                  # 表单定义
│   │   ├── article.py         # 文章表单
│   │   ├── auth.py            # 认证表单
│   │   └── comment.py         # 评论表单
│   ├── models/                 # 数据模型
│   │   ├── admin.py           # 管理员模型
│   │   ├── article.py         # 文章模型
│   │   ├── category.py        # 分类模型
│   │   ├── comment.py         # 评论模型
│   │   └── user.py            # 用户模型
│   ├── routes/                 # 路由处理
│   │   ├── admin.py           # 管理员路由
│   │   ├── article.py         # 文章路由
│   │   ├── auth.py            # 认证路由
│   │   ├── comment.py         # 评论路由
│   │   └── main.py            # 主路由
│   ├── services/               # 业务逻辑（预留）
│   ├── static/                 # 静态文件
│   │   ├── css/               # 样式文件
│   │   └── js/                # JavaScript文件
│   ├── templates/              # HTML模板
│   │   ├── admin/             # 管理员模板
│   │   ├── article/           # 文章模板
│   │   ├── auth/              # 认证模板
│   │   ├── comment/           # 评论模板
│   │   ├── errors/            # 错误页面
│   │   ├── main/              # 主页面模板
│   │   └── base.html          # 基础模板
│   ├── utils/                  # 工具函数
│   │   ├── assets.py          # 静态资源优化
│   │   ├── cache.py           # 缓存管理
│   │   ├── database.py        # 数据库工具
│   │   ├── decorators.py      # 装饰器
│   │   ├── error_handlers.py  # 错误处理
│   │   ├── logger.py          # 日志记录
│   │   ├── performance.py     # 性能监控
│   │   └── security.py        # 安全工具
│   └── __init__.py            # 应用工厂
├── config/                     # 配置文件
│   └── config.py              # 配置类
├── tests/                      # 测试文件
│   ├── conftest.py            # 测试配置
│   ├── test_basic.py          # 基础测试
│   └── test_profile.py        # 个人中心测试
├── .env.example                # 环境变量示例
├── .gitignore                  # Git忽略文件
├── init_db.py                  # 数据库初始化脚本
├── pytest.ini                  # pytest配置
├── README.md                   # 项目说明
├── requirements.txt            # 依赖列表
├── run.py                      # 启动文件
└── setup.py                    # 安装脚本
```

## 开发指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_profile.py

# 运行特定测试函数
pytest tests/test_profile.py::test_profile_page_displays_user_info

# 显示详细输出
pytest -v

# 显示测试覆盖率
pytest --cov=app
```

### 数据库操作

```bash
# 初始化数据库（创建所有表）
python init_db.py

# 手动创建表
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# 删除所有表
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.drop_all()"
```

### 代码风格

项目遵循 PEP 8 代码风格指南。建议使用以下工具：

```bash
# 安装代码检查工具
pip install flake8 black

# 检查代码风格
flake8 app/

# 自动格式化代码
black app/
```

### 调试

```bash
# 开启调试模式
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows

# 运行应用
python run.py
```

## API 文档

### 用户认证 API

- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `GET /auth/logout` - 用户登出

### 文章 API

- `GET /articles` - 获取文章列表
- `GET /articles/<id>` - 获取文章详情
- `POST /articles/create` - 创建文章
- `POST /articles/<id>/edit` - 编辑文章
- `POST /articles/<id>/delete` - 删除文章

### 评论 API

- `POST /articles/<id>/comments` - 发表评论
- `POST /comments/<id>/delete` - 删除评论
- `GET /my-comments` - 获取我的评论

### 管理员 API

- `GET /admin/dashboard` - 管理员仪表板
- `GET /admin/users` - 用户管理
- `GET /admin/articles` - 文章管理
- `GET /admin/comments` - 评论管理

## 常见问题

### 1. 数据库连接失败

确保 MySQL 服务正在运行，并检查 `.env` 文件中的数据库配置是否正确。

### 2. 导入错误

确保已激活虚拟环境并安装了所有依赖：
```bash
pip install -r requirements.txt
```

### 3. 端口被占用

如果 5000 端口被占用，可以在 `run.py` 中修改端口号。

### 4. 静态文件不加载

清除浏览器缓存或使用硬刷新（Ctrl+F5）。

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 贡献规范

- 遵循 PEP 8 代码风格
- 为新功能编写测试
- 更新相关文档
- 确保所有测试通过

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送 Pull Request
- 邮箱：[your-email@example.com]

## 致谢

感谢所有为本项目做出贡献的开发者！