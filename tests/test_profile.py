"""
测试用户个人中心功能
Test User Profile Features
"""
import pytest
from app.models.user import User
from app.models.article import Article
from app.models.comment import Comment
from app import db


def test_profile_page_requires_login(client):
    """测试个人中心页面需要登录"""
    response = client.get('/profile')
    assert response.status_code == 302  # 重定向到登录页面


def test_profile_page_displays_user_info(client, auth):
    """测试个人中心页面显示用户信息"""
    # 登录
    auth.login()
    
    # 访问个人中心
    response = client.get('/profile')
    assert response.status_code == 200
    assert 'testuser'.encode('utf-8') in response.data


def test_edit_profile_page(client, auth):
    """测试编辑个人资料页面"""
    # 登录
    auth.login()
    
    # 访问编辑页面
    response = client.get('/profile/edit')
    assert response.status_code == 200
    assert '编辑个人资料'.encode('utf-8') in response.data


def test_edit_profile_updates_user_info(client, auth, app):
    """测试编辑个人资料更新用户信息"""
    # 登录
    auth.login()
    
    # 提交编辑表单
    response = client.post('/profile/edit', data={
        'nickname': '测试昵称',
        'bio': '这是我的个人简介'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert '个人资料更新成功'.encode('utf-8') in response.data
    
    # 验证数据库中的更新
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user.nickname == '测试昵称'
        assert user.bio == '这是我的个人简介'


def test_change_password_page(client, auth):
    """测试修改密码页面"""
    # 登录
    auth.login()
    
    # 访问修改密码页面
    response = client.get('/profile/change-password')
    assert response.status_code == 200
    assert '修改密码'.encode('utf-8') in response.data


def test_change_password_with_correct_old_password(client, auth, app):
    """测试使用正确的原密码修改密码"""
    # 登录
    auth.login()
    
    # 提交修改密码表单
    response = client.post('/profile/change-password', data={
        'old_password': 'testpass',
        'new_password': 'newpass123',
        'confirm_password': 'newpass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert '密码修改成功'.encode('utf-8') in response.data
    
    # 验证新密码可以登录
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user.check_password('newpass123')


def test_change_password_with_wrong_old_password(client, auth):
    """测试使用错误的原密码修改密码"""
    # 登录
    auth.login()
    
    # 提交修改密码表单（原密码错误）
    response = client.post('/profile/change-password', data={
        'old_password': 'wrongpass',
        'new_password': 'newpass123',
        'confirm_password': 'newpass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert '原密码不正确'.encode('utf-8') in response.data


def test_my_articles_page(client, auth):
    """测试我的文章页面"""
    # 登录
    auth.login()
    
    # 访问我的文章页面
    response = client.get('/my-articles')
    assert response.status_code == 200
    assert '我的文章'.encode('utf-8') in response.data


def test_my_comments_page(client, auth):
    """测试我的评论页面"""
    # 登录
    auth.login()
    
    # 访问我的评论页面
    response = client.get('/my-comments')
    assert response.status_code == 200
    assert '我的评论'.encode('utf-8') in response.data


def test_profile_shows_statistics(client, auth, app):
    """测试个人中心显示统计信息"""
    # 登录
    auth.login()
    
    # 创建一些测试数据
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        
        # 创建文章
        article = Article(
            title='测试文章',
            content='测试内容',
            author_id=user.id,
            status='published'
        )
        article.publish()
        db.session.add(article)
        db.session.commit()
        
        # 创建评论
        comment = Comment(
            content='测试评论',
            author_id=user.id,
            article_id=article.id
        )
        db.session.add(comment)
        db.session.commit()
    
    # 访问个人中心
    response = client.get('/profile')
    assert response.status_code == 200
    # 验证统计信息显示
    assert response.data.count('1'.encode('utf-8')) >= 2  # 应该显示1篇文章和1条评论
