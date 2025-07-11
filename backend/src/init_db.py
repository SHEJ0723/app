import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def init_database():
    """初始化数据库"""
    # 数据库连接参数
    db_params = {
        'host': 'localhost',
        'user': 'root',
        'password': 'hhazj0723',
        'port': 3306,
        'charset': 'utf8mb4',
        'use_unicode': True,
        'connect_timeout': 5
    }
    
    try:
        # 连接MySQL服务器
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS parking_automation_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("数据库创建成功！")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"初始化数据库时出错: {str(e)}")
        raise e

if __name__ == '__main__':
    init_database() 