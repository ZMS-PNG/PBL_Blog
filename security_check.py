#!/usr/bin/env python3
"""
安全配置检查脚本
Security Configuration Check Script

运行此脚本检查生产环境配置是否安全
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_secret_key():
    """检查 SECRET_KEY 配置"""
    secret_key = os.environ.get('SECRET_KEY', '')
    
    issues = []
    
    if not secret_key:
        issues.append("❌ SECRET_KEY 未设置")
    elif secret_key == 'dev-secret-key-change-in-production' or 'dev' in secret_key.lower():
        issues.append("❌ SECRET_KEY 仍在使用开发环境默认值，必须更换！")
    elif len(secret_key) < 32:
        issues.append("⚠️  SECRET_KEY 长度过短，建议至少32个字符")
    else:
        print("✅ SECRET_KEY 配置正确")
        return True
    
    for issue in issues:
        print(issue)
    return False

def check_flask_env():
    """检查 FLASK_ENV 配置"""
    flask_env = os.environ.get('FLASK_ENV', 'production')
    
    if flask_env == 'production':
        print("✅ FLASK_ENV 设置为 production")
        return True
    else:
        print(f"⚠️  FLASK_ENV 设置为 {flask_env}，生产环境应设置为 production")
        return False

def check_database_config():
    """检查数据库配置"""
    db_password = os.environ.get('MYSQL_PASSWORD', '')
    db_user = os.environ.get('MYSQL_USER', 'root')
    db_name = os.environ.get('MYSQL_DATABASE', '')
    
    issues = []
    
    if not db_password:
        issues.append("❌ 数据库密码未设置")
    elif len(db_password) < 8:
        issues.append("⚠️  数据库密码过短，建议至少8个字符")
    elif db_password in ['password', '123456', 'admin', 'root']:
        issues.append("❌ 数据库密码过于简单，必须更换！")
    
    if db_user == 'root':
        issues.append("⚠️  建议创建专用数据库用户，不要使用 root")
    
    if 'dev' in db_name.lower():
        issues.append("⚠️  数据库名称包含 'dev'，确认是否为生产环境数据库")
    
    if not issues:
        print("✅ 数据库配置检查通过")
        return True
    
    for issue in issues:
        print(issue)
    return False

def check_debug_mode():
    """检查调试模式"""
    # 尝试导入配置
    try:
        from config.config import config
        flask_env = os.environ.get('FLASK_ENV', 'development')
        app_config = config.get(flask_env)
        
        if hasattr(app_config, 'DEBUG') and app_config.DEBUG:
            print("❌ DEBUG 模式已启用，生产环境必须关闭！")
            return False
        else:
            print("✅ DEBUG 模式已关闭")
            return True
    except Exception as e:
        print(f"⚠️  无法检查 DEBUG 模式: {e}")
        return False

def check_session_config():
    """检查 Session 配置"""
    try:
        from config.config import config
        flask_env = os.environ.get('FLASK_ENV', 'development')
        app_config = config.get(flask_env)
        
        issues = []
        
        if not app_config.SESSION_COOKIE_SECURE and flask_env == 'production':
            issues.append("⚠️  SESSION_COOKIE_SECURE 未启用，HTTPS 环境下应启用")
        
        if not app_config.SESSION_COOKIE_HTTPONLY:
            issues.append("❌ SESSION_COOKIE_HTTPONLY 未启用，存在 XSS 风险")
        
        if not issues:
            print("✅ Session 配置安全")
            return True
        
        for issue in issues:
            print(issue)
        return False
    except Exception as e:
        print(f"⚠️  无法检查 Session 配置: {e}")
        return False

def check_file_permissions():
    """检查文件权限"""
    sensitive_files = ['.env', 'config/config.py']
    
    issues = []
    
    for file_path in sensitive_files:
        if os.path.exists(file_path):
            # 在 Windows 上跳过权限检查
            if sys.platform == 'win32':
                continue
            
            stat_info = os.stat(file_path)
            mode = stat_info.st_mode & 0o777
            
            if mode & 0o004:  # 其他用户可读
                issues.append(f"⚠️  {file_path} 其他用户可读，建议设置为 600")
    
    if not issues:
        print("✅ 敏感文件权限检查通过")
        return True
    
    for issue in issues:
        print(issue)
    return False

def check_dependencies():
    """检查依赖包版本"""
    try:
        import flask
        import sqlalchemy
        
        print(f"✅ Flask 版本: {flask.__version__}")
        print(f"✅ SQLAlchemy 版本: {sqlalchemy.__version__}")
        
        # 检查是否有已知漏洞的版本
        flask_version = tuple(map(int, flask.__version__.split('.')))
        if flask_version < (2, 3, 0):
            print("⚠️  Flask 版本较旧，建议升级到最新版本")
            return False
        
        return True
    except Exception as e:
        print(f"⚠️  无法检查依赖版本: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("博客系统安全配置检查")
    print("=" * 60)
    print()
    
    checks = [
        ("SECRET_KEY 配置", check_secret_key),
        ("Flask 环境配置", check_flask_env),
        ("数据库配置", check_database_config),
        ("调试模式", check_debug_mode),
        ("Session 配置", check_session_config),
        ("文件权限", check_file_permissions),
        ("依赖包版本", check_dependencies),
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n检查 {name}:")
        print("-" * 60)
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("检查结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print(f"\n通过: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有检查通过！系统配置安全。")
        return 0
    else:
        print("\n⚠️  存在安全问题，请根据上述提示进行修复。")
        print("\n建议:")
        print("1. 生成新的 SECRET_KEY: python -c \"import secrets; print(secrets.token_hex(32))\"")
        print("2. 更换数据库密码为强密码")
        print("3. 设置 FLASK_ENV=production")
        print("4. 查看 PRODUCTION_SETUP.md 了解详细配置")
        return 1

if __name__ == '__main__':
    sys.exit(main())
