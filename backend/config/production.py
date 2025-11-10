import os

class ProductionConfig:
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    # 上传配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or '/var/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 虚拟币配置
    INITIAL_COINS = 100  # 新用户初始校园币
    REVIEW_REWARD_COINS = 5  # 评价奖励校园币