"""
应用配置文件
Application Configuration
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'blog_system'
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 生产环境不输出SQL语句
    SQLALCHEMY_POOL_SIZE = 10  # 连接池大小
    SQLALCHEMY_POOL_TIMEOUT = 30  # 连接池超时时间
    SQLALCHEMY_POOL_RECYCLE = 3600  # 连接回收时间
    SQLALCHEMY_MAX_OVERFLOW = 20  # 连接池最大溢出
    
    # 分页配置
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 20
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'app/static/uploads'
    
    # 安全配置
    # CSRF保护
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # CSRF令牌不过期
    
    # Session配置
    SESSION_COOKIE_SECURE = False  # 生产环境应设为True（需要HTTPS）
    SESSION_COOKIE_HTTPONLY = True  # 防止JavaScript访问cookie
    SESSION_COOKIE_SAMESITE = 'Lax'  # 防止CSRF攻击
    PERMANENT_SESSION_LIFETIME = 3600  # Session过期时间（秒）

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    # 使用 SQLite 进行快速开发（如果 MySQL 不可用）
    USE_SQLITE = os.environ.get('USE_SQLITE', 'false').lower() == 'true'
    
    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///blog_system.db'
    else:
        # 使用环境变量中的数据库名称
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@"
            f"{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}"
        )

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # 生产环境启用HTTPS cookie

# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}