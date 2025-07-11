import os
import sys
from src.migrations.create_tables import init_db

if __name__ == '__main__':
    # 添加项目根目录到系统路径
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # 初始化数据库
    init_db() 