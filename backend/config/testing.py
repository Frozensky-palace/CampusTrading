import os

class TestingConfig:
    """测试环境配置"""
    TESTING = True
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql+pymysql://root:password@localhost:3306/campus_trading_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'test-jwt-secret-key'
    
    # 上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 虚拟币配置
    INITIAL_COINS = 100  # 新用户初始校园币
    REVIEW_REWARD_COINS = 5  # 评价奖励校园币