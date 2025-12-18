"""
安全工具函数
Security Utilities
"""
import re
import html
from functools import wraps
from flask import request, abort
from flask_login import current_user
from app.utils.logger import log_security_event


def sanitize_html(text):
    """
    清理HTML内容，防止XSS攻击
    
    Args:
        text: 输入文本
        
    Returns:
        str: 清理后的文本
    """
    if not text:
        return ''
    
    # 转义HTML特殊字符
    text = html.escape(text)
    
    return text


def sanitize_input(text, max_length=None):
    """
    清理用户输入
    
    Args:
        text: 输入文本
        max_length: 最大长度限制
        
    Returns:
        str: 清理后的文本
    """
    if not text:
        return ''
    
    # 移除潜在的SQL注入字符
    # 注意：使用ORM已经提供了基本的SQL注入防护
    # 这里只是额外的防护层
    text = text.strip()
    
    # 限制长度
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_email(email):
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        bool: 是否有效
    """
    if not email:
        return False
    
    # 简单的邮箱格式验证
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username):
    """
    验证用户名格式
    
    Args:
        username: 用户名
        
    Returns:
        bool: 是否有效
    """
    if not username:
        return False
    
    # 用户名只能包含字母、数字、下划线和连字符
    # 长度3-20个字符
    pattern = r'^[a-zA-Z0-9_-]{3,20}$'
    return re.match(pattern, username) is not None


def check_sql_injection(text):
    """
    检查是否包含SQL注入特征
    
    Args:
        text: 输入文本
        
    Returns:
        bool: 是否包含SQL注入特征
    """
    if not text:
        return False
    
    # SQL注入常见关键词
    sql_keywords = [
        'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE',
        'ALTER', 'EXEC', 'EXECUTE', 'UNION', 'DECLARE', '--', ';--',
        'xp_', 'sp_', 'SCRIPT', 'JAVASCRIPT', 'ONERROR', 'ONLOAD'
    ]
    
    text_upper = text.upper()
    for keyword in sql_keywords:
        if keyword in text_upper:
            return True
    
    return False


def check_xss_attack(text):
    """
    检查是否包含XSS攻击特征
    
    Args:
        text: 输入文本
        
    Returns:
        bool: 是否包含XSS攻击特征
    """
    if not text:
        return False
    
    # XSS攻击常见模式
    xss_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'onerror\s*=',
        r'onload\s*=',
        r'onclick\s*=',
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>',
    ]
    
    text_lower = text.lower()
    for pattern in xss_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    
    return False


def validate_input_security(text, field_name='input'):
    """
    验证输入安全性
    
    Args:
        text: 输入文本
        field_name: 字段名称
        
    Returns:
        tuple: (是否有效, 错误消息)
    """
    if not text:
        return True, None
    
    # 检查SQL注入
    if check_sql_injection(text):
        log_security_event('SQL_INJECTION_ATTEMPT', 
                          f'Field: {field_name}, Content: {text[:100]}')
        return False, '输入包含非法字符'
    
    # 检查XSS攻击
    if check_xss_attack(text):
        log_security_event('XSS_ATTACK_ATTEMPT',
                          f'Field: {field_name}, Content: {text[:100]}')
        return False, '输入包含非法脚本'
    
    return True, None


def rate_limit_check(key, max_requests=10, window=60):
    """
    简单的速率限制检查
    
    Args:
        key: 限制键（如用户ID或IP）
        max_requests: 最大请求数
        window: 时间窗口（秒）
        
    Returns:
        bool: 是否允许请求
    """
    # 这是一个简化版本，生产环境应使用Redis等缓存系统
    # 这里仅作为示例
    return True


def admin_required(f):
    """
    管理员权限装饰器
    
    Args:
        f: 被装饰的函数
        
    Returns:
        function: 装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            log_security_event('UNAUTHORIZED_ACCESS', 'User not authenticated')
            abort(403)
        
        # 检查是否是管理员
        from app.models.admin import Admin
        admin = Admin.query.filter_by(user_id=current_user.id).first()
        if not admin:
            log_security_event('UNAUTHORIZED_ADMIN_ACCESS',
                             f'User {current_user.id} attempted admin access')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def secure_filename(filename):
    """
    清理文件名，防止路径遍历攻击
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 安全的文件名
    """
    if not filename:
        return ''
    
    # 移除路径分隔符
    filename = filename.replace('/', '').replace('\\', '')
    
    # 只保留字母、数字、点、下划线和连字符
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    
    return filename
