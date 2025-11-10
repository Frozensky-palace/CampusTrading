import os
from app import create_app, db
from flask_migrate import Migrate
from app.modules.user.models import User
from app.modules.admin.models import AdminUser, SystemConfig

# 获取配置环境
config_name = os.environ.get('FLASK_CONFIG', 'development')

# 创建Flask应用
app = create_app(config_name)

# 初始化数据库迁移工具
migrate = Migrate(app, db)


@app.cli.command()
def init_db():
    """初始化数据库"""
    # 创建所有表
    db.create_all()
    
    # 创建默认管理员
    admin_user = AdminUser.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = AdminUser(username='admin')
        admin_user.set_password('admin123')  # 注意：生产环境中应该使用更安全的密码
        admin_user.role = 'super_admin'
        db.session.add(admin_user)
    
    # 创建基础系统配置
    if not SystemConfig.query.filter_by(key='site_name').first():
        site_config = SystemConfig(
            key='site_name',
            value='CampusTrading',
            description='网站名称',
            config_type='string'
        )
        db.session.add(site_config)
    
    if not SystemConfig.query.filter_by(key='site_description').first():
        desc_config = SystemConfig(
            key='site_description',
            value='校园交易平台',
            description='网站描述',
            config_type='string'
        )
        db.session.add(desc_config)
    
    db.session.commit()
    print('数据库初始化成功！')
    print('默认管理员账号：admin 密码：admin123')
    print('请在生产环境中立即修改密码！')


@app.cli.command()
def reset_db():
    """重置数据库（警告：这将删除所有数据）"""
    if input('确定要重置数据库吗？这将删除所有数据！(y/N): ').lower() == 'y':
        db.drop_all()
        db.create_all()
        print('数据库已重置！')
    else:
        print('操作已取消！')


@app.cli.command()
def create_migration():
    """创建数据库迁移脚本"""
    from flask_migrate import upgrade, migrate
    migrate()
    print('迁移脚本已创建！')


@app.cli.command()
def apply_migration():
    """应用数据库迁移"""
    from flask_migrate import upgrade
    upgrade()
    print('数据库迁移已应用！')


if __name__ == '__main__':
    # 启动Flask应用
    app.run(host='0.0.0.0', port=5000)


# 为了便于使用Python shell进行调试和开发
# 可以使用以下命令进入shell
# flask shell

# 使用示例:
# >>> from app import db
# >>> from app.modules.user.models import User
# >>> users = User.query.all()