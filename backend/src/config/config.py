import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:hhazj0723@localhost:3306/parking_automation_system?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 跨域配置
    CORS_HEADERS = 'Content-Type'
    
    # AI模型配置
    MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 