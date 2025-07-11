from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
import re
import uuid

from models.user import User, Admin, db
from utils.captcha import CaptchaGenerator
from utils.redis_client import redis_client

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/captcha', methods=['GET'])
def generate_captcha():
    """生成验证码"""
    try:
        # 生成验证码
        captcha_data = CaptchaGenerator.generate_captcha()
        
        # 获取或生成会话ID
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # 将验证码存入Redis，有效期10分钟
        redis_key = f'captcha:{session_id}'
        redis_client.setex(redis_key, 600, captcha_data['text'])
        
        # 准备响应
        response = jsonify({
            'success': True,
            'data': {
                'image': captcha_data['image'],
                'expires_in': 600  # 返回过期时间给前端
            }
        })
        
        # 如果没有session_id，设置cookie
        if not request.cookies.get('session_id'):
            # 设置cookie的过期时间为10分钟
            response.set_cookie(
                'session_id',
                session_id,
                httponly=True,
                secure=True,
                max_age=600,
                samesite='Strict'
            )
        
        return response
    except Exception as e:
        current_app.logger.error(f"Generate captcha error: {str(e)}")
        return jsonify(success=False, message="生成验证码失败，请刷新重试"), 500

@auth_bp.route('/api/user-login', methods=['POST'])
def user_login():
    """用户登录"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        password = data.get('password')
        remember = data.get('remember', False)
        
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return jsonify(success=False, message="手机号格式错误"), 400
        
        # 查询用户
        user = User.query.filter_by(phone=phone).first()
        if not user or not user.check_password(password):
            return jsonify(success=False, message="手机号或密码错误"), 401
        
        # 设置token过期时间
        expires_delta = timedelta(days=7 if remember else 1)
        
        # 创建访问令牌
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'role': 'user'},
            expires_delta=expires_delta
        )
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify(
            success=True,
            message="登录成功",
            data={
                'token': access_token,
                'user': user.to_dict()
            }
        )
        
    except Exception as e:
        current_app.logger.error(f"User login error: {str(e)}")
        return jsonify(success=False, message="登录失败，请稍后重试"), 500

@auth_bp.route('/api/admin-login', methods=['POST'])
def admin_login():
    """管理员登录"""
    try:
        data = request.get_json()
        employee_id = data.get('workId')  # 前端传workId
        password = data.get('adminPassword')  # 前端传adminPassword
        captcha = data.get('captcha', '').upper()
        
        # 获取session_id
        session_id = request.cookies.get('session_id')
        if not session_id:
            return jsonify(success=False, message="请重新获取验证码"), 400  # 改为400而不是401
        
        # 验证验证码
        redis_key = f'captcha:{session_id}'
        stored_captcha = redis_client.get(redis_key)
        if not stored_captcha:
            return jsonify(success=False, message="验证码已过期，请重新获取"), 400  # 改为400而不是401
        
        if stored_captcha.decode('utf-8').upper() != captcha:
            return jsonify(success=False, message="验证码错误，请重新输入"), 400  # 改为400而不是401
        
        # 验证工号格式
        if not employee_id or not re.match(r'^[a-zA-Z0-9]+$', employee_id):
            return jsonify(success=False, message="工号格式错误"), 400
        
        # 查询管理员
        admin = Admin.query.filter_by(employee_id=employee_id).first()
        if not admin or not admin.check_password(password):
            return jsonify(success=False, message="工号或密码错误"), 401
        
        # 创建访问令牌（管理员token有效期较短）
        access_token = create_access_token(
            identity=admin.id,
            additional_claims={'role': 'admin', 'admin_role': admin.role},
            expires_delta=timedelta(hours=4)
        )
        
        # 更新最后登录时间
        admin.last_login = datetime.utcnow()
        db.session.commit()
        
        # 删除验证码
        redis_client.delete(redis_key)
        
        return jsonify(
            success=True,
            message="登录成功",
            data={
                'token': access_token,
                'admin': admin.to_dict()
            }
        )
        
    except Exception as e:
        current_app.logger.error(f"Admin login error: {str(e)}")
        return jsonify(success=False, message="登录失败，请稍后重试"), 500

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')
        # 参数校验
        if not name or not phone or not password:
            return jsonify(success=False, message="缺少必要参数"), 400
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return jsonify(success=False, message="手机号格式错误"), 400
        if User.query.filter_by(name=name).first():
            return jsonify(success=False, message="用户名已存在"), 400
        if User.query.filter_by(phone=phone).first():
            return jsonify(success=False, message="手机号已被使用"), 400
        if email and User.query.filter_by(email=email).first():
            return jsonify(success=False, message="邮箱已被使用"), 400
        # 创建用户
        user = User(name=name, phone=phone, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify(success=True, message="注册成功", data=user.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f"User register error: {str(e)}")
        return jsonify(success=False, message="注册失败，请稍后重试"), 500 