"""
Flask应用工厂函数
Flask Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config.config import config

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_name='default'):
    """
    应用工厂函数
    
    Args:
        config_name (str): 配置名称
        
    Returns:
        Flask: Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # 配置日志系统
    from app.utils.logger import setup_logging
    setup_logging(app)
    
    # 配置性能监控
    from app.utils.performance import setup_performance_monitoring
    setup_performance_monitoring(app)
    
    # 配置静态资源优化
    from app.utils.assets import setup_asset_optimization
    setup_asset_optimization(app)
    
    # 配置登录管理器
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录以访问此页面。'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """加载用户回调函数"""
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    from app.routes.article import article_bp
    from app.routes.comment import comment_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(article_bp)
    app.register_blueprint(comment_bp)
    
    # 注册全局错误处理器
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # 添加安全响应头
    @app.after_request
    def add_security_headers(response):
        """添加安全响应头"""
        # 防止XSS攻击
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # 内容安全策略
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net;"
        )
        
        return response
    
    # 注册模板过滤器
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """将换行符转换为HTML换行标签"""
        if text is None:
            return ''
        return text.replace('\n', '<br>\n')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app