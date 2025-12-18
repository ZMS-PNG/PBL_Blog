"""
全局错误处理器
Global Error Handlers
"""
from flask import render_template, jsonify, request
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.utils.logger import log_error, log_security_event


def register_error_handlers(app):
    """
    注册全局错误处理器
    
    Args:
        app: Flask应用实例
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """400 错误请求"""
        log_error(error, 'Bad Request')
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': '请求格式错误'
                }
            }), 400
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(403)
    def forbidden(error):
        """403 权限不足"""
        log_security_event('FORBIDDEN_ACCESS', str(error))
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'FORBIDDEN',
                    'message': '您没有权限访问此资源'
                }
            }), 403
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """404 页面不存在"""
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'NOT_FOUND',
                    'message': '请求的资源不存在'
                }
            }), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """405 方法不允许"""
        log_error(error, 'Method Not Allowed')
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'METHOD_NOT_ALLOWED',
                    'message': '不支持的请求方法'
                }
            }), 405
        return render_template('errors/405.html'), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 服务器内部错误"""
        log_error(error, 'Internal Server Error')
        # 回滚数据库会话
        from app import db
        db.session.rollback()
        
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': '服务器内部错误，请稍后重试'
                }
            }), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        """数据库错误"""
        log_error(error, 'Database Error')
        from app import db
        db.session.rollback()
        
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'DATABASE_ERROR',
                    'message': '数据库操作失败'
                }
            }), 500
        return render_template('errors/500.html', 
                             message='数据库操作失败，请稍后重试'), 500
    
    @app.errorhandler(Exception)
    def unhandled_exception(error):
        """未处理的异常"""
        log_error(error, 'Unhandled Exception')
        from app import db
        db.session.rollback()
        
        # 在生产环境中不暴露详细错误信息
        if app.config.get('DEBUG'):
            raise error
        
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'UNKNOWN_ERROR',
                    'message': '发生未知错误'
                }
            }), 500
        return render_template('errors/500.html'), 500
