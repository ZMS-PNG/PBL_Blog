"""
测试配置文件
Test Configuration
"""
import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    """创建测试应用实例"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        
        # 创建测试用户
        user = User(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        db.session.add(user)
        db.session.commit()
        
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """创建CLI测试运行器"""
    return app.test_cli_runner()

class AuthActions:
    """认证操作辅助类"""
    def __init__(self, client):
        self._client = client
    
    def login(self, username='testuser', password='testpass'):
        """登录"""
        return self._client.post('/auth/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)
    
    def logout(self):
        """登出"""
        return self._client.get('/auth/logout', follow_redirects=True)

@pytest.fixture
def auth(client):
    """认证操作fixture"""
    return AuthActions(client)