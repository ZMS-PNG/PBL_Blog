"""
日志记录工具
Logging Utilities
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(app):
    """
    配置应用日志系统
    
    Args:
        app: Flask应用实例
    """
    # 创建日志目录
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志级别
    if app.config.get('DEBUG'):
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    # 配置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # 配置文件处理器 - 应用日志
    app_log_file = os.path.join(log_dir, 'app.log')
    app_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    app_handler.setFormatter(formatter)
    app_handler.setLevel(log_level)
    
    # 配置文件处理器 - 错误日志
    error_log_file = os.path.join(log_dir, 'error.log')
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    
    # 配置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # 添加处理器到应用日志
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # 记录启动信息
    app.logger.info('=' * 50)
    app.logger.info(f'Blog System started at {datetime.now()}')
    app.logger.info(f'Environment: {app.config.get("ENV", "production")}')
    app.logger.info('=' * 50)


def log_error(error, context=None):
    """
    记录错误信息
    
    Args:
        error: 错误对象
        context: 额外的上下文信息
    """
    from flask import current_app, request
    
    error_msg = f'Error: {str(error)}'
    if context:
        error_msg += f' | Context: {context}'
    
    # 记录请求信息
    if request:
        error_msg += f' | URL: {request.url} | Method: {request.method}'
        if request.form:
            # 不记录敏感信息
            safe_form = {k: v for k, v in request.form.items() 
                        if k not in ['password', 'password_hash']}
            error_msg += f' | Form: {safe_form}'
    
    current_app.logger.error(error_msg, exc_info=True)


def log_security_event(event_type, details):
    """
    记录安全事件
    
    Args:
        event_type: 事件类型
        details: 事件详情
    """
    from flask import current_app, request
    
    security_msg = f'SECURITY EVENT: {event_type}'
    if details:
        security_msg += f' | Details: {details}'
    
    if request:
        security_msg += f' | IP: {request.remote_addr} | URL: {request.url}'
    
    current_app.logger.warning(security_msg)
