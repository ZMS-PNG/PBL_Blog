"""
演示数据生成脚本
Demo Data Seeding Script

用于生成演示用的测试数据，包括：
- 测试用户账号
- 示例文章
- 示例评论
- 文章分类
"""
from app import create_app, db
from app.models.user import User
from app.models.admin import Admin
from app.models.category import Category
from app.models.article import Article
from app.models.comment import Comment
from datetime import datetime, timedelta
import random


def seed_demo_data():
    """生成演示数据"""
    app = create_app()
    
    with app.app_context():
        print("开始生成演示数据...")
        
        # 清空现有数据（可选）
        print("\n警告：此操作将清空所有现有数据！")
        confirm = input("是否继续？(yes/no): ")
        if confirm.lower() != 'yes':
            print("操作已取消")
            return
        
        print("\n清空现有数据...")
        Comment.query.delete()
        Article.query.delete()
        Category.query.delete()
        Admin.query.delete()
        User.query.delete()
        db.session.commit()
        
        # 1. 创建测试用户
        print("\n创建测试用户...")
        users = []
        
        # 管理员用户
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password='admin123',
            nickname='系统管理员',
            bio='博客系统管理员账号'
        )
        users.append(admin_user)
        
        # 普通用户
        test_users = [
            ('zhangsan', 'zhangsan@example.com', '张三', '热爱技术的程序员'),
            ('lisi', 'lisi@example.com', '李四', '全栈开发工程师'),
            ('wangwu', 'wangwu@example.com', '王五', '前端开发爱好者'),
            ('zhaoliu', 'zhaoliu@example.com', '赵六', 'Python开发者'),
        ]
        
        for username, email, nickname, bio in test_users:
            user = User(
                username=username,
                email=email,
                password='password123',
                nickname=nickname,
                bio=bio
            )
            users.append(user)
        
        db.session.add_all(users)
        db.session.commit()
        print(f"✓ 创建了 {len(users)} 个用户")
        
        # 2. 设置管理员
        print("\n设置管理员权限...")
        admin = Admin(user_id=admin_user.id, role='admin')
        db.session.add(admin)
        db.session.commit()
        print("✓ 管理员权限设置完成")
        
        # 3. 创建分类
        print("\n创建文章分类...")
        categories = [
            ('技术分享', 'technology', '分享技术文章和编程经验'),
            ('生活随笔', 'life', '记录生活点滴和感悟'),
            ('学习笔记', 'study', '学习过程中的笔记和总结'),
            ('项目实战', 'project', '实际项目开发经验分享'),
            ('工具推荐', 'tools', '好用的开发工具和资源推荐'),
        ]
        
        category_objs = []
        for name, slug, desc in categories:
            category = Category(name=name, slug=slug, description=desc)
            category_objs.append(category)
        
        db.session.add_all(category_objs)
        db.session.commit()
        print(f"✓ 创建了 {len(category_objs)} 个分类")
        
        # 4. 创建示例文章
        print("\n创建示例文章...")
        articles_data = [
            {
                'title': 'Python Flask 入门指南',
                'content': '''Flask 是一个轻量级的 Python Web 框架，非常适合初学者学习。

## 什么是 Flask？

Flask 是一个使用 Python 编写的轻量级 Web 应用框架。它被称为"微框架"，因为它使用简单的核心，用扩展增加其他功能。

## 为什么选择 Flask？

1. **简单易学**：Flask 的 API 设计简洁，容易上手
2. **灵活性高**：可以根据需要选择组件
3. **文档完善**：官方文档详细且易懂
4. **社区活跃**：有大量的扩展和教程

## 快速开始

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
```

这就是一个最简单的 Flask 应用！''',
                'category': 0,
                'author': 1
            },
            {
                'title': '如何提高编程效率',
                'content': '''作为程序员，提高编程效率是我们一直追求的目标。以下是一些实用的建议。

## 1. 使用合适的工具

选择一个好用的 IDE 或编辑器，如 VS Code、PyCharm 等。

## 2. 学习快捷键

熟练使用快捷键可以大大提高编码速度。

## 3. 编写可复用的代码

遵循 DRY（Don't Repeat Yourself）原则。

## 4. 持续学习

技术在不断更新，保持学习的习惯很重要。

## 5. 代码审查

定期审查自己的代码，发现可以改进的地方。''',
                'category': 0,
                'author': 2
            },
            {
                'title': '我的编程学习之路',
                'content': '''回顾我的编程学习历程，有很多感悟想要分享。

## 起步阶段

最开始接触编程是在大学，学的是 C 语言。那时候觉得编程很难，经常被指针搞得晕头转向。

## 转折点

后来接触到 Python，发现编程原来可以这么简单！Python 的简洁语法让我重新爱上了编程。

## 持续进步

现在我已经可以独立完成一些小项目了，这种成就感是无法用言语表达的。

## 给初学者的建议

1. 不要害怕犯错
2. 多动手实践
3. 学会查文档
4. 加入技术社区

编程是一个需要持续学习的过程，希望大家都能坚持下去！''',
                'category': 1,
                'author': 3
            },
            {
                'title': 'MySQL 数据库优化技巧',
                'content': '''数据库性能优化是后端开发中的重要课题。

## 索引优化

合理使用索引可以大大提高查询速度：

1. 为经常查询的字段添加索引
2. 避免在索引列上使用函数
3. 使用覆盖索引减少回表

## 查询优化

1. 避免 SELECT *
2. 使用 LIMIT 限制结果集
3. 合理使用 JOIN

## 表结构优化

1. 选择合适的数据类型
2. 规范化与反规范化的权衡
3. 分表分库策略

## 配置优化

调整 MySQL 配置参数，如缓冲池大小、连接数等。''',
                'category': 0,
                'author': 4
            },
            {
                'title': '推荐几个实用的开发工具',
                'content': '''工欲善其事，必先利其器。这里推荐几个我常用的开发工具。

## 1. VS Code

微软出品的免费代码编辑器，插件丰富，性能优秀。

## 2. Postman

API 测试工具，支持各种 HTTP 请求方法。

## 3. Git

版本控制工具，程序员必备。

## 4. Docker

容器化技术，简化部署流程。

## 5. Navicat

数据库管理工具，支持多种数据库。

这些工具都大大提高了我的开发效率，推荐给大家！''',
                'category': 4,
                'author': 1
            },
        ]
        
        articles = []
        base_time = datetime.now() - timedelta(days=30)
        
        for i, data in enumerate(articles_data):
            article = Article(
                title=data['title'],
                content=data['content'],
                author_id=users[data['author']].id,
                category_id=category_objs[data['category']].id,
                status='published',
                view_count=random.randint(10, 500)
            )
            article.created_at = base_time + timedelta(days=i*5)
            article.publish()
            article.published_at = article.created_at
            articles.append(article)
        
        db.session.add_all(articles)
        db.session.commit()
        print(f"✓ 创建了 {len(articles)} 篇文章")
        
        # 5. 创建示例评论
        print("\n创建示例评论...")
        comments_data = [
            (0, 2, '写得很好，对初学者很有帮助！'),
            (0, 3, '感谢分享，正好在学 Flask'),
            (1, 1, '这些建议很实用，我会试试看'),
            (1, 4, '同意，使用快捷键确实能提高效率'),
            (2, 1, '加油！编程之路虽然艰辛但很有意义'),
            (2, 4, '我也是从 Python 开始的，共勉！'),
            (3, 2, '数据库优化确实很重要'),
            (3, 3, '学到了，感谢分享'),
            (4, 3, 'VS Code 确实好用'),
            (4, 4, 'Docker 我也在用，很方便'),
        ]
        
        comments = []
        for article_idx, user_idx, content in comments_data:
            comment = Comment(
                content=content,
                author_id=users[user_idx].id,
                article_id=articles[article_idx].id,
                status='approved'
            )
            comments.append(comment)
        
        db.session.add_all(comments)
        db.session.commit()
        print(f"✓ 创建了 {len(comments)} 条评论")
        
        print("\n" + "="*50)
        print("演示数据生成完成！")
        print("="*50)
        print("\n测试账号信息：")
        print("-" * 50)
        print("管理员账号：")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n普通用户账号：")
        for username, _, nickname, _ in test_users:
            print(f"  用户名: {username} ({nickname})")
            print(f"  密码: password123")
        print("-" * 50)


if __name__ == '__main__':
    seed_demo_data()
