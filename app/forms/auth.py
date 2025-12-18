"""
用户认证表单
Authentication Forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User


class RegistrationForm(FlaskForm):
    """
    用户注册表单
    
    实现需求:
    - 1.1: 验证用户输入信息的完整性和格式正确性
    - 1.2: 用户名或邮箱已存在时显示错误信息并阻止注册
    - 1.5: 用户输入无效邮箱格式时显示邮箱格式错误提示
    """
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=50, message='用户名长度必须在3-50个字符之间')
    ])
    
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='邮箱格式不正确'),
        Length(max=100, message='邮箱长度不能超过100个字符')
    ])
    
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, max=128, message='密码长度必须在6-128个字符之间')
    ])
    
    password2 = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    
    nickname = StringField('昵称', validators=[
        Length(max=50, message='昵称长度不能超过50个字符')
    ])
    
    submit = SubmitField('注册')
    
    def validate_username(self, username):
        """
        验证用户名唯一性
        
        Args:
            username: 用户名字段
            
        Raises:
            ValidationError: 用户名已存在时抛出异常
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已存在，请选择其他用户名')
    
    def validate_email(self, email):
        """
        验证邮箱唯一性
        
        Args:
            email: 邮箱字段
            
        Raises:
            ValidationError: 邮箱已存在时抛出异常
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱已存在，请使用其他邮箱')


class LoginForm(FlaskForm):
    """
    用户登录表单
    
    实现需求:
    - 2.1: 用户输入正确的用户名和密码时验证凭据并创建用户会话
    - 2.2: 用户输入错误的登录信息时显示登录失败提示
    """
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空')
    ])
    
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空')
    ])
    
    remember_me = BooleanField('记住我')
    
    submit = SubmitField('登录')


class EditProfileForm(FlaskForm):
    """
    编辑个人资料表单
    
    实现需求:
    - 7.2: 用户修改个人信息时验证并更新用户资料
    """
    nickname = StringField('昵称', validators=[
        Length(max=50, message='昵称长度不能超过50个字符')
    ])
    
    bio = StringField('个人简介', validators=[
        Length(max=500, message='个人简介长度不能超过500个字符')
    ])
    
    submit = SubmitField('保存修改')


class ChangePasswordForm(FlaskForm):
    """
    修改密码表单
    
    实现需求:
    - 7.3: 用户修改密码时验证原密码并加密存储新密码
    """
    old_password = PasswordField('原密码', validators=[
        DataRequired(message='请输入原密码')
    ])
    
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='请输入新密码'),
        Length(min=6, max=128, message='密码长度必须在6-128个字符之间')
    ])
    
    confirm_password = PasswordField('确认新密码', validators=[
        DataRequired(message='请确认新密码'),
        EqualTo('new_password', message='两次输入的密码不一致')
    ])
    
    submit = SubmitField('修改密码')