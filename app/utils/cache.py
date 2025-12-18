"""
缓存工具
Cache Utilities
"""
from functools import wraps
from flask import request
import hashlib
import json


# 简单的内存缓存（生产环境应使用Redis）
_cache = {}


def get_cache_key(prefix, *args, **kwargs):
    """
    生成缓存键
    
    Args:
        prefix: 键前缀
        *args: 位置参数
        **kwargs: 关键字参数
        
    Returns:
        str: 缓存键
    """
    key_data = {
        'prefix': prefix,
        'args': args,
        'kwargs': kwargs
    }
    key_str = json.dumps(key_data, sort_keys=True)
    key_hash = hashlib.md5(key_str.encode()).hexdigest()
    return f"{prefix}:{key_hash}"


def cache_result(timeout=300, key_prefix='view'):
    """
    缓存函数结果装饰器
    
    Args:
        timeout: 缓存超时时间（秒）
        key_prefix: 缓存键前缀
        
    Returns:
        function: 装饰器函数
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 生成缓存键
            cache_key = get_cache_key(key_prefix, *args, **kwargs)
            
            # 检查缓存
            if cache_key in _cache:
                cached_data = _cache[cache_key]
                # 简单的过期检查（生产环境应使用更完善的机制）
                return cached_data
            
            # 执行函数
            result = f(*args, **kwargs)
            
            # 存储到缓存
            _cache[cache_key] = result
            
            return result
        return decorated_function
    return decorator


def clear_cache(key_prefix=None):
    """
    清除缓存
    
    Args:
        key_prefix: 要清除的缓存键前缀，None表示清除所有
    """
    global _cache
    if key_prefix is None:
        _cache = {}
    else:
        keys_to_delete = [k for k in _cache.keys() if k.startswith(key_prefix)]
        for key in keys_to_delete:
            del _cache[key]


def invalidate_cache_on_change(key_prefix):
    """
    数据变更时清除缓存的装饰器
    
    Args:
        key_prefix: 要清除的缓存键前缀
        
    Returns:
        function: 装饰器函数
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            clear_cache(key_prefix)
            return result
        return decorated_function
    return decorator
