"""
主要页面路由
Main Page Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.utils.decorators import active_user_required

# 创建主页面蓝图
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首页
    
    实现需求:
    - 6.1: 用户访问首页时显示最新发布的文章列表
    """
    from app.models.article import Article
    # 获取最新的5篇文章
    recent_articles = Article.get_recent_articles(limit=5)
    return render_template('main/index.html', recent_articles=recent_articles)

@main_bp.route('/profile')
@active_user_required
def profile():
    """
    用户个人中心
    
    实现需求:
    - 2.5: 未登录用户访问受保护页面时重定向到登录页面
    - 7.1: 用户访问个人中心时显示用户的基本信息和统计数据
    """
    # 获取用户统计信息
    article_count = current_user.articles.count()
    published_article_count = current_user.articles.filter_by(status='published').count()
    draft_article_count = current_user.articles.filter_by(status='draft').count()
    comment_count = current_user.comments.count()
    
    return render_template('main/profile.html',
                         article_count=article_count,
                         published_article_count=published_article_count,
                         draft_article_count=draft_article_count,
                         comment_count=comment_count)

@main_bp.route('/profile/edit', methods=['GET', 'POST'])
@active_user_required
def edit_profile():
    """
    编辑个人资料
    
    实现需求:
    - 7.2: 用户修改个人信息时验证并更新用户资料
    """
    from app.forms.auth import EditProfileForm
    
    form = EditProfileForm()
    
    if form.validate_on_submit():
        try:
            # 更新用户信息
            current_user.nickname = form.nickname.data.strip() if form.nickname.data else None
            current_user.bio = form.bio.data.strip() if form.bio.data else None
            
            db.session.commit()
            flash('个人资料更新成功。', 'success')
            return redirect(url_for('main.profile'))
            
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'更新个人资料失败: {str(e)}', 'error')
    
    # 预填充表单
    if request.method == 'GET':
        form.nickname.data = current_user.nickname
        form.bio.data = current_user.bio
    
    return render_template('main/edit_profile.html', form=form)

@main_bp.route('/profile/change-password', methods=['GET', 'POST'])
@active_user_required
def change_password():
    """
    修改密码
    
    实现需求:
    - 7.3: 用户修改密码时验证原密码并加密存储新密码
    """
    from app.forms.auth import ChangePasswordForm
    
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # 验证原密码
        if not current_user.check_password(form.old_password.data):
            flash('原密码不正确。', 'error')
            return render_template('main/change_password.html', form=form)
        
        try:
            # 更新密码
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('密码修改成功，请使用新密码登录。', 'success')
            return redirect(url_for('main.profile'))
            
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'修改密码失败: {str(e)}', 'error')
    
    return render_template('main/change_password.html', form=form)


@main_bp.route('/robots.txt')
def robots():
    """
    提供 robots.txt 文件
    """
    from flask import send_from_directory
    import os
    return send_from_directory(os.path.join(main_bp.root_path, '..', 'static'), 'robots.txt')

@main_bp.route('/favicon.ico')
def favicon():
    """
    提供 favicon.ico 文件
    """
    from flask import send_from_directory
    import os
    return send_from_directory(os.path.join(main_bp.root_path, '..', 'static'), 'favicon.ico')
