# 部署指南

本文档提供博客系统的部署说明，包括开发环境和生产环境的配置。

## 目录

- [开发环境部署](#开发环境部署)
- [生产环境部署](#生产环境部署)
- [Docker 部署](#docker-部署)
- [常见问题](#常见问题)

## 开发环境部署

### 1. 系统要求

- Python 3.10+
- MySQL 5.7+ 或 MariaDB 10.3+
- Git

### 2. 安装步骤

参考 [README.md](README.md) 中的快速开始部分。

### 3. 开发环境配置

创建 `.env` 文件：

```env
# Flask 配置
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=blog_system

# 日志配置
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log
```

## 生产环境部署

### 1. 服务器要求

- Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- Python 3.10+
- MySQL 5.7+ 或 MariaDB 10.3+
- Nginx (推荐)
- Gunicorn (WSGI 服务器)

### 2. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 和相关工具
sudo apt install python3.10 python3.10-venv python3-pip -y

# 安装 MySQL
sudo apt install mysql-server -y

# 安装 Nginx
sudo apt install nginx -y
```

### 3. 部署应用

```bash
# 创建应用目录
sudo mkdir -p /var/www/blog-system
cd /var/www/blog-system

# 克隆代码
git clone <repository-url> .

# 创建虚拟环境
python3.10 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn
```

### 4. 生产环境配置

创建 `.env` 文件：

```env
# Flask 配置
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=blog_user
DB_PASSWORD=secure_password_here
DB_NAME=blog_system

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=/var/log/blog-system/app.log

# 安全配置
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

### 5. 配置数据库

```bash
# 登录 MySQL
sudo mysql

# 创建数据库和用户
CREATE DATABASE blog_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'blog_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON blog_system.* TO 'blog_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 初始化数据库
python init_db.py
```

### 6. 配置 Gunicorn

创建 `gunicorn_config.py`：

```python
# Gunicorn 配置文件
import multiprocessing

# 绑定地址
bind = "127.0.0.1:8000"

# 工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 超时时间
timeout = 120

# 日志
accesslog = "/var/log/blog-system/gunicorn-access.log"
errorlog = "/var/log/blog-system/gunicorn-error.log"
loglevel = "info"

# 进程名称
proc_name = "blog-system"

# 守护进程
daemon = False
```

### 7. 配置 Systemd 服务

创建 `/etc/systemd/system/blog-system.service`：

```ini
[Unit]
Description=Blog System Gunicorn Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/blog-system
Environment="PATH=/var/www/blog-system/venv/bin"
ExecStart=/var/www/blog-system/venv/bin/gunicorn -c gunicorn_config.py run:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
# 创建日志目录
sudo mkdir -p /var/log/blog-system
sudo chown www-data:www-data /var/log/blog-system

# 设置权限
sudo chown -R www-data:www-data /var/www/blog-system

# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start blog-system

# 设置开机自启
sudo systemctl enable blog-system

# 查看状态
sudo systemctl status blog-system
```

### 8. 配置 Nginx

创建 `/etc/nginx/sites-available/blog-system`：

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # 日志
    access_log /var/log/nginx/blog-system-access.log;
    error_log /var/log/nginx/blog-system-error.log;

    # 静态文件
    location /static {
        alias /var/www/blog-system/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 代理到 Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

启用站点：

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/blog-system /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

### 9. 配置 SSL (可选但推荐)

使用 Let's Encrypt 免费 SSL 证书：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

## Docker 部署

### 1. 创建 Dockerfile

```dockerfile
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "-c", "gunicorn_config.py", "run:app"]
```

### 2. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: blog-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: blog_system
      MYSQL_USER: blog_user
      MYSQL_PASSWORD: blog_password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
    networks:
      - blog-network

  web:
    build: .
    container_name: blog-web
    restart: always
    environment:
      FLASK_ENV: production
      DB_HOST: db
      DB_PORT: 3306
      DB_USER: blog_user
      DB_PASSWORD: blog_password
      DB_NAME: blog_system
    ports:
      - "8000:8000"
    depends_on:
      - db
    networks:
      - blog-network
    volumes:
      - ./logs:/app/logs

  nginx:
    image: nginx:alpine
    container_name: blog-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./app/static:/usr/share/nginx/html/static
    depends_on:
      - web
    networks:
      - blog-network

volumes:
  mysql_data:

networks:
  blog-network:
    driver: bridge
```

### 3. 启动 Docker 容器

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

## 数据库迁移

### 备份数据库

```bash
# 导出数据库
mysqldump -u blog_user -p blog_system > backup_$(date +%Y%m%d).sql

# 导入数据库
mysql -u blog_user -p blog_system < backup_20231218.sql
```

### 使用 Flask-Migrate (可选)

```bash
# 安装
pip install Flask-Migrate

# 初始化
flask db init

# 生成迁移
flask db migrate -m "Initial migration"

# 应用迁移
flask db upgrade
```

## 监控和维护

### 1. 日志管理

```bash
# 查看应用日志
tail -f /var/log/blog-system/app.log

# 查看 Gunicorn 日志
tail -f /var/log/blog-system/gunicorn-error.log

# 查看 Nginx 日志
tail -f /var/log/nginx/blog-system-error.log
```

### 2. 性能监控

推荐使用以下工具：
- **New Relic**: 应用性能监控
- **Prometheus + Grafana**: 系统监控
- **ELK Stack**: 日志分析

### 3. 定期维护

```bash
# 清理日志
find /var/log/blog-system -name "*.log" -mtime +30 -delete

# 数据库优化
mysql -u blog_user -p -e "OPTIMIZE TABLE blog_system.articles;"

# 更新应用
cd /var/www/blog-system
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart blog-system
```

## 常见问题

### 1. 应用无法启动

检查日志：
```bash
sudo journalctl -u blog-system -n 50
```

### 2. 数据库连接失败

检查数据库服务状态：
```bash
sudo systemctl status mysql
```

检查数据库配置：
```bash
mysql -u blog_user -p -e "SHOW DATABASES;"
```

### 3. Nginx 502 错误

检查 Gunicorn 是否运行：
```bash
sudo systemctl status blog-system
```

检查端口是否被占用：
```bash
sudo netstat -tlnp | grep 8000
```

### 4. 静态文件无法加载

检查文件权限：
```bash
ls -la /var/www/blog-system/app/static
```

清除浏览器缓存或使用硬刷新。

## 安全建议

1. **定期更新系统和依赖包**
2. **使用强密码**
3. **启用防火墙**
4. **配置 SSL/TLS**
5. **定期备份数据**
6. **限制数据库访问**
7. **使用环境变量存储敏感信息**
8. **启用日志审计**

## 性能优化

1. **使用 Redis 缓存**
2. **启用 Gzip 压缩**
3. **优化数据库查询**
4. **使用 CDN 加速静态资源**
5. **配置数据库连接池**
6. **启用浏览器缓存**

## 联系支持

如遇到部署问题，请：
1. 查看日志文件
2. 检查配置文件
3. 参考本文档的常见问题部分
4. 提交 Issue 到项目仓库
