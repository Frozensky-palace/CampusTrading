from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

# 初始化数据库
db = SQLAlchemy()
# 初始化数据库迁移
migrate = Migrate()
# 初始化JWT
jwt = JWTManager()


def create_app(config_name=None):
    """创建Flask应用实例"""
    app = Flask(__name__)
    
    # 配置应用
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    # 根据配置名称加载不同的配置
    if config_name == 'development':
        from config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        from config.testing import TestingConfig
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        from config.production import ProductionConfig
        app.config.from_object(ProductionConfig)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # 配置CORS，允许跨域请求
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 注册蓝图
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # 用户模块
    from app.modules.user.routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    # 商品模块
    from app.modules.item.routes import item_bp
    app.register_blueprint(item_bp, url_prefix='/api/items')
    
    # 交易模块
    from app.modules.transaction.routes import transaction_bp
    app.register_blueprint(transaction_bp, url_prefix='/api/transaction')
    
    # 求购模块
    from app.modules.request.routes import request_bp
    app.register_blueprint(request_bp, url_prefix='/api/requests')
    
    # 比价模块
    from app.modules.compare.routes import compare_bp
    app.register_blueprint(compare_bp, url_prefix='/api/compare')
    
    # 管理员模块
    from app.modules.admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    return app