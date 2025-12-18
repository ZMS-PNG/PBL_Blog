# 生产环境配置指南

本文档提供了将博客系统部署到生产环境的详细配置说明。

## ⚠️ 安全检查清单

在部署到生产环境之前，**必须**完成以下安全配置：

### 1. 更换 SECRET_KEY

SECRET_KEY 用于加密 session 和 CSRF token，必须使用强随机密钥。

**生成强随机密钥：**

```python
# 方法1：使用 Python
python -c "import secrets; print(secrets.token_hex(32))"

# 方法2：使用 OpenSSL
openssl rand -hex 32
```

**更新 .env 文件：**

```env
SECRET_KEY=your-generated-strong-random-key-here
```

### 2. 数据库安全

**更换数据库密码：**

```env
MYSQL_PASSWORD=your-strong-database-password
MYSQL_DATABASE=blog_system_prod
```

**数据库用户权限：**

```sql
-- 创建专用数据库用户（不要使用 root）
CREATE USER 'blog_user'@'localhost' IDENTIFIED BY 'strong-password';
GRANT ALL PRIVILEGES ON blog_system_prod.* TO 'blog_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 环境变量配置

**生产环境 .env 文件示例：**

```env
# Flask配置
SECRET_KEY=your-generated-strong-random-key-here
FLASK_ENV=production

# 数据库配置
USE_SQLITE=false
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=blog_user
MYSQL_PASSWORD=your-strong-database-password
MYSQL_DATABASE=blog_system_prod
```

### 4. HTTPS 配置

生产环境**必须**使用 HTTPS。配置 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;
    
    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/PBL_Blog/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 5. 防火墙配置

```bash
# 只开放必要端口
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## 📋 部署步骤

### 1. 准备服务器

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装依赖
sudo apt install python3-pip python3-venv nginx mysql-server -y
```

### 2. 配置数据库

```bash
# 安全配置 MySQL
sudo mysql_secure_installation

# 创建数据库
sudo mysql -u root -p
```

```sql
CREATE DATABASE blog_system_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'blog_user'@'localhost' IDENTIFIED BY 'strong-password';
GRANT ALL PRIVILEGES ON blog_system_prod.* TO 'blog_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. 部署应用

```bash
# 克隆代码
cd /var/www
sudo git clone <repository-url> blog_system
cd blog_system

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 配置环境变量
cp .env.example .env
nano .env  # 编辑配置

# 初始化数据库
python init_db.py

# 创建管理员账号（可选）
python seed_demo_data.py
```

### 4. 配置 Gunicorn

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/blog_system.service
```

```ini
[Unit]
Description=Blog System Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/blog_system
Environment="PATH=/var/www/blog_system/venv/bin"
ExecStart=/var/www/blog_system/venv/bin/gunicorn -c gunicorn_config.py run:app

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start blog_system
sudo systemctl enable blog_system
sudo systemctl status blog_system
```

### 5. 配置 Nginx

```bash
sudo nano /etc/nginx/sites-available/blog_system
```

使用上面的 Nginx 配置，然后：

```bash
sudo ln -s /etc/nginx/sites-available/blog_system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. 配置 SSL 证书（Let's Encrypt）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

## 🔒 安全加固

### 1. 限制文件权限

```bash
sudo chown -R www-data:www-data /var/www/blog_system
sudo chmod -R 755 /var/www/blog_system
sudo chmod 600 /var/www/blog_system/.env
```

### 2. 配置日志轮转

```bash
sudo nano /etc/logrotate.d/blog_system
```

```
/var/www/blog_system/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

### 3. 设置定期备份

```bash
# 创建备份脚本
sudo nano /usr/local/bin/backup_blog_system.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/blog_system"
DATE=$(date +%Y%m%d_%H%M%S)

# 备份数据库
mysqldump -u blog_user -p'password' blog_system_prod > "$BACKUP_DIR/db_$DATE.sql"

# 备份上传文件
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" /var/www/blog_system/app/static/uploads

# 删除30天前的备份
find $BACKUP_DIR -type f -mtime +30 -delete
```

```bash
sudo chmod +x /usr/local/bin/backup_blog_system.sh

# 添加到 crontab（每天凌晨2点备份）
sudo crontab -e
0 2 * * * /usr/local/bin/backup_blog_system.sh
```

## 📊 监控和维护

### 1. 查看应用日志

```bash
# 应用日志
tail -f /var/www/blog_system/logs/app.log

# Gunicorn 日志
sudo journalctl -u blog_system -f

# Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. 性能监控

建议安装监控工具：
- **Prometheus + Grafana**: 系统和应用监控
- **New Relic / DataDog**: APM 监控
- **Sentry**: 错误追踪

### 3. 定期维护

```bash
# 更新依赖
cd /var/www/blog_system
source venv/bin/activate
pip install --upgrade -r requirements.txt

# 重启服务
sudo systemctl restart blog_system

# 清理日志
sudo journalctl --vacuum-time=30d
```

## 🚨 故障排查

### 应用无法启动

```bash
# 检查服务状态
sudo systemctl status blog_system

# 查看详细日志
sudo journalctl -u blog_system -n 50

# 检查配置文件
python -c "from app import create_app; app = create_app('production')"
```

### 数据库连接失败

```bash
# 测试数据库连接
mysql -u blog_user -p blog_system_prod

# 检查 MySQL 状态
sudo systemctl status mysql
```

### Nginx 502 错误

```bash
# 检查 Gunicorn 是否运行
sudo systemctl status blog_system

# 检查端口占用
sudo netstat -tlnp | grep 8000

# 检查 Nginx 配置
sudo nginx -t
```

## 📝 更新部署

```bash
cd /var/www/blog_system

# 拉取最新代码
git pull origin main

# 激活虚拟环境
source venv/bin/activate

# 更新依赖
pip install -r requirements.txt

# 运行数据库迁移（如果有）
# python migrate.py

# 重启服务
sudo systemctl restart blog_system
```

## ✅ 部署检查清单

部署完成后，请检查：

- [ ] SECRET_KEY 已更换为强随机密钥
- [ ] 数据库密码已更换
- [ ] HTTPS 已配置并正常工作
- [ ] 防火墙已配置
- [ ] 文件权限已正确设置
- [ ] 日志轮转已配置
- [ ] 备份脚本已设置
- [ ] 监控系统已部署
- [ ] 所有测试通过
- [ ] 性能测试完成

## 📞 支持

如遇问题，请查看：
- 应用日志：`/var/www/blog_system/logs/`
- 系统日志：`sudo journalctl -u blog_system`
- 文档：`README.md` 和 `DEPLOYMENT.md`
