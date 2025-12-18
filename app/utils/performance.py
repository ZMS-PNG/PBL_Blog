"""
性能优化工具
Performance Optimization Utilities
"""
from flask import request, g
import time
from functools import wraps


def query_timer(f):
    """
    查询计时装饰器
    
    Args:
        f: 被装饰的函数
        
    Returns:
        function: 装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        if execution_time > 1.0:  # 超过1秒记录警告
            from flask import current_app
            current_app.logger.warning(
                f'Slow query detected: {f.__name__} took {execution_time:.2f}s'
            )
        
        return result
    return decorated_function


def optimize_query(query, eager_load=None):
    """
    优化数据库查询
    
    Args:
        query: SQLAlchemy查询对象
        eager_load: 需要预加载的关系列表
        
    Returns:
        query: 优化后的查询对象
    """
    from sqlalchemy.orm import joinedload
    
    if eager_load:
        for relation in eager_load:
            query = query.options(joinedload(relation))
    
    return query


def paginate_query(query, page, per_page):
    """
    分页查询优化
    
    Args:
        query: SQLAlchemy查询对象
        page: 页码
        per_page: 每页数量
        
    Returns:
        dict: 包含items和pagination信息的字典
    """
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': pagination.items,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next,
        'prev_num': pagination.prev_num,
        'next_num': pagination.next_num
    }


def compress_response(f):
    """
    响应压缩装饰器（简化版）
    
    Args:
        f: 被装饰的函数
        
    Returns:
        function: 装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        # 实际的压缩应该由Web服务器（如Nginx）处理
        # 这里只是一个占位符
        return response
    return decorated_function


def setup_performance_monitoring(app):
    """
    设置性能监控
    
    Args:
        app: Flask应用实例
    """
    @app.before_request
    def before_request():
        """请求开始时记录时间"""
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        """请求结束时计算执行时间"""
        if hasattr(g, 'start_time'):
            execution_time = time.time() - g.start_time
            
            # 添加响应头
            response.headers['X-Execution-Time'] = f'{execution_time:.3f}s'
            
            # 记录慢请求
            if execution_time > 2.0:  # 超过2秒
                app.logger.warning(
                    f'Slow request: {request.method} {request.path} '
                    f'took {execution_time:.2f}s'
                )
        
        return response


def batch_query(model, ids, batch_size=100):
    """
    批量查询优化
    
    Args:
        model: 模型类
        ids: ID列表
        batch_size: 批次大小
        
    Returns:
        list: 查询结果列表
    """
    results = []
    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i:i + batch_size]
        batch_results = model.query.filter(model.id.in_(batch_ids)).all()
        results.extend(batch_results)
    
    return results


def optimize_article_query(query):
    """
    优化文章查询
    
    Args:
        query: 文章查询对象
        
    Returns:
        query: 优化后的查询对象
    """
    from sqlalchemy.orm import joinedload
    from app.models.article import Article
    
    # 预加载作者和分类信息
    query = query.options(
        joinedload(Article.author),
        joinedload(Article.category)
    )
    
    return query


def optimize_comment_query(query):
    """
    优化评论查询
    
    Args:
        query: 评论查询对象
        
    Returns:
        query: 优化后的查询对象
    """
    from sqlalchemy.orm import joinedload
    from app.models.comment import Comment
    
    # 预加载作者信息
    query = query.options(joinedload(Comment.author))
    
    return query
