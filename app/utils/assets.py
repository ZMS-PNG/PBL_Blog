"""
静态资源优化工具
Static Assets Optimization Utilities
"""
import os
import hashlib
from flask import url_for


def get_file_hash(filepath):
    """
    获取文件哈希值用于缓存破坏
    
    Args:
        filepath: 文件路径
        
    Returns:
        str: 文件哈希值
    """
    try:
        with open(filepath, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:8]
        return file_hash
    except:
        return ''


def versioned_url_for(endpoint, **values):
    """
    生成带版本号的静态资源URL
    
    Args:
        endpoint: 端点名称
        **values: URL参数
        
    Returns:
        str: 带版本号的URL
    """
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            # 获取文件路径
            from flask import current_app
            filepath = os.path.join(current_app.static_folder, filename)
            
            # 添加版本号
            if os.path.exists(filepath):
                file_hash = get_file_hash(filepath)
                values['v'] = file_hash
    
    return url_for(endpoint, **values)


def minify_css(css_content):
    """
    简单的CSS压缩
    
    Args:
        css_content: CSS内容
        
    Returns:
        str: 压缩后的CSS
    """
    # 移除注释
    import re
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # 移除多余空白
    css_content = re.sub(r'\s+', ' ', css_content)
    css_content = re.sub(r'\s*([{}:;,])\s*', r'\1', css_content)
    
    return css_content.strip()


def minify_js(js_content):
    """
    简单的JavaScript压缩
    注意：这是一个非常简化的版本，生产环境应使用专业工具
    
    Args:
        js_content: JavaScript内容
        
    Returns:
        str: 压缩后的JavaScript
    """
    # 移除单行注释
    import re
    js_content = re.sub(r'//.*?$', '', js_content, flags=re.MULTILINE)
    
    # 移除多行注释
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    
    # 移除多余空白（保留字符串内的空白）
    # 注意：这是一个简化版本，可能不完美
    js_content = re.sub(r'\s+', ' ', js_content)
    
    return js_content.strip()


def setup_asset_optimization(app):
    """
    设置静态资源优化
    
    Args:
        app: Flask应用实例
    """
    # 注册模板函数
    app.jinja_env.globals['versioned_url_for'] = versioned_url_for
    
    # 在生产环境启用静态文件缓存
    if not app.config.get('DEBUG'):
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1年
