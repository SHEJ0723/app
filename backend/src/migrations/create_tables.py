from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from models.user import db, User, Admin
from app import create_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化迁移
    migrate = Migrate(app, db)
    
    return app

def init_database():
    """初始化数据库表和默认数据"""
    app = create_app()
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 检查是否已存在默认管理员
        admin = Admin.query.filter_by(employee_id='admin').first()
        if not admin:
            # 创建默认管理员账号
            default_admin = Admin(
                employee_id='admin',
                name='系统管理员',
                email='admin@example.com',
                role='super_admin',
                department='IT部门',
                status='active'
            )
            default_admin.set_password('Admin@123456')
            
            # 添加到数据库
            db.session.add(default_admin)
            db.session.commit()
            print("默认管理员账号创建成功！")
        else:
            print("默认管理员账号已存在")

if __name__ == '__main__':
    init_database() 