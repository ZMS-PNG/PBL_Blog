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
    
    # 注册错误处理器
    @app.errorhandler(403)
    def forbidden(error):
        """403 权限不足错误处理"""
        from flask import render_template
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """404 页面不存在错误处理"""
        from flask import render_template
        return render_template('errors/404.html'), 404
    
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