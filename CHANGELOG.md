# 更新日志

本文档记录项目的所有重要更改。

## [1.1.0] - 2024-12-18

### 🔧 修复

- **数据库配置不一致**: 修复了 `.env` 和 `config.py` 中数据库名称不一致的问题
  - 统一使用环境变量 `MYSQL_DATABASE`
  - 更新配置文件使用 `blog_system_dev` 作为开发数据库名

### ✨ 新增

- **安全检查脚本** (`security_check.py`)
  - 自动检查 SECRET_KEY 配置
  - 验证数据库密码强度
  - 检查 DEBUG 模式状态
  - 验证 Session 安全配置
  - 检查文件权限
  - 验证依赖包版本

- **生产环境配置指南** (`PRODUCTION_SETUP.md`)
  - 详细的安全检查清单
  - SECRET_KEY 生成方法
  - 数据库安全配置
  - HTTPS 和 SSL 配置
  - Nginx 反向代理配置
  - Gunicorn 服务配置
  - 日志轮转和备份脚本
  - 监控和故障排查指南

- **SEO 优化**
  - 添加 `robots.txt` 文件
  - 添加 `favicon.ico` 支持
  - 在 `base.html` 中添加 meta description
  - 添加 `/robots.txt` 和 `/favicon.ico` 路由处理

- **项目文档**
  - `IMPROVEMENTS.md` - 改进记录和待办事项
  - `CHANGELOG.md` - 本文档

### 📝 改进

- **环境变量配置**
  - 更新 `.env.example`，添加详细注释
  - 添加 `USE_SQLITE` 选项说明
  - 添加生产环境配置示例

- **README 文档**
  - 添加安全检查说明
  - 添加演示数据生成步骤
  - 添加生产环境部署警告

- **项目检查清单**
  - 更新 `PROJECT_CHECKLIST.md`
  - 添加新增的配置文件和工具

### 🔒 安全

- 在 `.env` 中添加安全提示
- 创建安全配置检查工具
- 提供详细的生产环境安全指南

---

## [1.0.0] - 2024-12-17

### ✨ 初始版本

#### 核心功能

- **用户系统**
  - 用户注册和登录
  - 密码加密存储（bcrypt）
  - 个人资料管理
  - 密码修改功能

- **文章管理**
  - 文章发布、编辑、删除（CRUD）
  - 文章状态管理（草稿、已发布、已归档）
  - 文章分类
  - 文章搜索和筛选
  - 分页浏览
  - 浏览计数

- **评论系统**
  - 评论发表和删除
  - 评论回复（层级结构）
  - 评论审核状态管理

- **管理员功能**
  - 用户管理（查看、编辑、删除）
  - 文章管理（查看、编辑、删除所有文章）
  - 评论管理（审核、删除所有评论）
  - 管理员仪表板

#### 技术实现

- **后端**
  - Flask 2.3.3 应用框架
  - SQLAlchemy 3.0.5 ORM
  - Flask-Login 用户认证
  - Flask-WTF 表单处理
  - MySQL 数据库支持

- **前端**
  - 响应式布局（Bootstrap 5）
  - JavaScript 交互
  - 自定义 CSS 样式

- **安全**
  - CSRF 保护
  - XSS 防护
  - SQL 注入防护（ORM）
  - 密码加密存储
  - 会话管理
  - 安全响应头

- **性能**
  - 数据库查询优化
  - 缓存机制
  - 静态资源优化
  - 数据库连接池

- **错误处理**
  - 全局错误处理器
  - 日志记录系统
  - 友好的错误页面

#### 测试

- pytest 测试框架
- 基础功能测试
- 个人中心功能测试
- Hypothesis 属性测试库（已安装）

#### 文档

- README.md（项目说明）
- DEPLOYMENT.md（部署指南）
- LICENSE（MIT 许可证）
- 需求文档（requirements.md）
- 设计文档（design.md）
- 任务列表（tasks.md）

#### 配置和工具

- requirements.txt（依赖列表）
- pytest.ini（测试配置）
- .gitignore（Git 忽略文件）
- .env.example（环境变量示例）
- gunicorn_config.py（生产服务器配置）
- init_db.py（数据库初始化）
- seed_demo_data.py（演示数据生成）

---

## 版本说明

版本号格式：`主版本号.次版本号.修订号`

- **主版本号**: 重大功能变更或不兼容的 API 修改
- **次版本号**: 新增功能，向下兼容
- **修订号**: 问题修复，向下兼容

---

## 链接

- [项目主页](README.md)
- [部署指南](DEPLOYMENT.md)
- [生产环境配置](PRODUCTION_SETUP.md)
- [改进记录](IMPROVEMENTS.md)
