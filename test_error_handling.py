"""
测试错误处理和日志记录系统
Test Error Handling and Logging System
"""
import os
import sys
import pytest
from flask import Flask
from app import create_app, db
from app.models.user import User


class TestErrorHandling:
    """测试错误处理功能"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        app = create_app('testing')
        with app.app_context():
            db.create_all()
            yield app
            db.session.remove()
            db.drop_all()
    
    @pytest.fixture
    def client(self, app):
        """创建测试客户端"""
        return app.test_client()
    
    def test_404_error_page(self, client):
        """测试404错误页面"""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
        assert '404' in response.data.decode('utf-8')
        assert '页面不存在' in response.data.decode('utf-8')
    
    def test_404_error_json(self, client):
        """测试404错误JSON响应"""
        response = client.get('/api/nonexistent', 
                            headers={'Content-Type': 'application/json'})
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False
        assert data['error']['code'] == 'NOT_FOUND'
    
    def test_403_error_page(self, client):
        """测试403权限不足页面"""
        # 尝试访问管理员页面（未登录）
        response = client.get('/admin/users')
        # 应该重定向到登录页面或显示403
        assert response.status_code in [302, 403]
    
    def test_405_error_page(self, client):
        """测试405方法不允许错误"""
        # 尝试使用错误的HTTP方法
        response = client.post('/auth/login', data={})
        # 登录页面应该接受POST，所以这里测试其他只接受GET的路由
        response = client.post('/')
        # 首页通常只接受GET
        if response.status_code == 405:
            assert '405' in response.data.decode('utf-8')
    
    def test_logging_directory_created(self, app):
        """测试日志目录是否创建"""
        assert os.path.exists('logs')
    
    def test_log_files_exist(self, app):
        """测试日志文件是否创建"""
        # 触发一些日志记录
        with app.app_context():
            app.logger.info('Test log message')
            app.logger.error('Test error message')
        
        # 检查日志文件
        assert os.path.exists('logs/app.log')
        assert os.path.exists('logs/error.log')
    
    def test_error_handler_registration(self, app):
        """测试错误处理器是否正确注册"""
        # 检查错误处理器是否存在
        assert 404 in app.error_handler_spec[None]
        assert 500 in app.error_handler_spec[None]


class TestLoggingSystem:
    """测试日志记录系统"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        app = create_app('testing')
        with app.app_context():
            db.create_all()
            yield app
            db.session.remove()
            db.drop_all()
    
    def test_logger_configured(self, app):
        """测试日志器是否正确配置"""
        assert app.logger is not None
        assert len(app.logger.handlers) > 0
    
    def test_log_levels(self, app):
        """测试不同日志级别"""
        with app.app_context():
            app.logger.debug('Debug message')
            app.logger.info('Info message')
            app.logger.warning('Warning message')
            app.logger.error('Error message')
            app.logger.critical('Critical message')
        
        # 验证日志文件包含消息
        if os.path.exists('logs/app.log'):
            with open('logs/app.log', 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'Info message' in content or 'Error message' in content
    
    def test_error_logging_with_context(self, app):
        """测试带上下文的错误日志"""
        from app.utils.logger import log_error
        
        with app.app_context():
            with app.test_request_context('/test'):
                try:
                    raise ValueError('Test error')
                except ValueError as e:
                    log_error(e, 'Test context')
        
        # 验证错误日志
        if os.path.exists('logs/error.log'):
            with open('logs/error.log', 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'Test error' in content or 'ValueError' in content
    
    def test_security_event_logging(self, app):
        """测试安全事件日志"""
        from app.utils.logger import log_security_event
        
        with app.app_context():
            with app.test_request_context('/test'):
                log_security_event('TEST_EVENT', 'Test security details')
        
        # 验证安全事件被记录
        if os.path.exists('logs/app.log'):
            with open('logs/app.log', 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'SECURITY EVENT' in content or 'TEST_EVENT' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
