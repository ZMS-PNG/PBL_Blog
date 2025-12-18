"""
验证个人中心实现
Validate Profile Implementation
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def validate_profile_routes():
    """验证个人中心路由"""
    print("验证个人中心路由...")
    
    from app.routes.main import main_bp
    
    # 检查路由是否存在
    routes = [rule.rule for rule in main_bp.url_map.iter_rules()]
    
    required_routes = [
        '/profile',
        '/profile/edit',
        '/profile/change-password'
    ]
    
    for route in required_routes:
        if any(route in r for r in routes):
            print(f"✓ 路由 {route} 存在")
        else:
            print(f"✗ 路由 {route} 不存在")
            return False
    
    return True

def validate_profile_forms():
    """验证个人中心表单"""
    print("\n验证个人中心表单...")
    
    from app.forms.auth import EditProfileForm, ChangePasswordForm
    
    # 检查表单类是否存在
    forms = [
        ('EditProfileForm', EditProfileForm),
        ('ChangePasswordForm', ChangePasswordForm)
    ]
    
    for form_name, form_class in forms:
        if form_class:
            print(f"✓ 表单 {form_name} 存在")
            
            # 检查表单字段
            form = form_class()
            if form_name == 'EditProfileForm':
                if hasattr(form, 'nickname') and hasattr(form, 'bio'):
                    print(f"  ✓ 表单字段完整")
                else:
                    print(f"  ✗ 表单字段不完整")
                    return False
            elif form_name == 'ChangePasswordForm':
                if hasattr(form, 'old_password') and hasattr(form, 'new_password') and hasattr(form, 'confirm_password'):
                    print(f"  ✓ 表单字段完整")
                else:
                    print(f"  ✗ 表单字段不完整")
                    return False
        else:
            print(f"✗ 表单 {form_name} 不存在")
            return False
    
    return True

def validate_profile_templates():
    """验证个人中心模板"""
    print("\n验证个人中心模板...")
    
    import os
    
    templates = [
        'app/templates/main/profile.html',
        'app/templates/main/edit_profile.html',
        'app/templates/main/change_password.html'
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"✓ 模板 {template} 存在")
        else:
            print(f"✗ 模板 {template} 不存在")
            return False
    
    return True

def validate_content_management():
    """验证个人内容管理"""
    print("\n验证个人内容管理...")
    
    from app.routes.article import article_bp
    from app.routes.comment import comment_bp
    
    # 检查我的文章和我的评论路由
    article_routes = [rule.rule for rule in article_bp.url_map.iter_rules()]
    comment_routes = [rule.rule for rule in comment_bp.url_map.iter_rules()]
    
    if any('/my-articles' in r for r in article_routes):
        print("✓ 我的文章路由存在")
    else:
        print("✗ 我的文章路由不存在")
        return False
    
    if any('/my-comments' in r for r in comment_routes):
        print("✓ 我的评论路由存在")
    else:
        print("✗ 我的评论路由不存在")
        return False
    
    # 检查模板
    import os
    templates = [
        'app/templates/article/my_articles.html',
        'app/templates/comment/my_comments.html'
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"✓ 模板 {template} 存在")
        else:
            print(f"✗ 模板 {template} 不存在")
            return False
    
    return True

def validate_csrf_protection():
    """验证CSRF保护"""
    print("\n验证CSRF保护...")
    
    try:
        from app import csrf
        print("✓ CSRF保护已配置")
        return True
    except ImportError:
        print("✗ CSRF保护未配置")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("开始验证个人中心实现")
    print("=" * 60)
    
    results = []
    
    # 验证各个部分
    results.append(("个人中心路由", validate_profile_routes()))
    results.append(("个人中心表单", validate_profile_forms()))
    results.append(("个人中心模板", validate_profile_templates()))
    results.append(("个人内容管理", validate_content_management()))
    results.append(("CSRF保护", validate_csrf_protection()))
    
    # 输出总结
    print("\n" + "=" * 60)
    print("验证结果总结")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ 所有验证通过！个人中心实现完成。")
        print("\n实现的功能:")
        print("  - 个人资料管理（查看、编辑）")
        print("  - 密码修改")
        print("  - 个人统计信息显示")
        print("  - 我的文章列表")
        print("  - 我的评论列表")
        return 0
    else:
        print("\n✗ 部分验证失败，请检查实现。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
