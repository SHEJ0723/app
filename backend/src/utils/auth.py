from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
from models.user import User

def generate_token(user_id):
    """生成JWT令牌"""
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return None

def token_required(f):
    """验证JWT令牌的装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': '无效的认证头部'}), 401

        if not token:
            return jsonify({'message': '缺少令牌'}), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
            current_user = User.query.get(payload['sub'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '令牌已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '无效的令牌'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    """验证管理员权限的装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': '无效的认证头部'}), 401

        if not token:
            return jsonify({'message': '缺少令牌'}), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
            current_user = User.query.get(payload['sub'])
            if not current_user.role == 'admin':
                return jsonify({'message': '需要管理员权限'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '令牌已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '无效的令牌'}), 401

        return f(current_user, *args, **kwargs)
    return decorated 