from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        from models.user import Admin
        current_admin = Admin.query.get(user_id)
        if not current_admin:
            return jsonify({'success': False, 'message': '权限不足'}), 403
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    keyword = request.args.get('keyword', '')
    query = User.query
    if keyword:
        query = query.filter(User.name.like(f'%{keyword}%'))
    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'success': True,
        'data': {
            'list': [user.to_dict() for user in users],
            'total': total
        }
    })

@users_bp.route('/api/users', methods=['POST'])
@jwt_required()
def add_user():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        from models.user import Admin
        current_admin = Admin.query.get(user_id)
        if not current_admin:
            return jsonify({'success': False, 'message': '权限不足'}), 403
    data = request.get_json()
    if not data or 'name' not in data or 'password' not in data or 'phone' not in data:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    if User.query.filter_by(name=data['name']).first():
        return jsonify({'success': False, 'message': '用户名已存在'}), 400
    if User.query.filter_by(phone=data['phone']).first():
        return jsonify({'success': False, 'message': '手机号已被使用'}), 400
    if data.get('email'):
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': '邮箱已被使用'}), 400
    user = User(
        name=data['name'],
        phone=data['phone'],
        email=data.get('email', None)
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'message': '用户创建成功', 'data': user.to_dict()}), 201

@users_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    operator_id = get_jwt_identity()
    current_user = User.query.get(operator_id)
    if not current_user:
        from models.user import Admin
        current_admin = Admin.query.get(operator_id)
        if not current_admin:
            return jsonify({'success': False, 'message': '权限不足'}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    data = request.get_json()
    if 'name' in data:
        if User.query.filter(User.name == data['name'], User.id != user_id).first():
            return jsonify({'success': False, 'message': '用户名已存在'}), 400
        user.name = data['name']
    if 'phone' in data:
        if User.query.filter(User.phone == data['phone'], User.id != user_id).first():
            return jsonify({'success': False, 'message': '手机号已被使用'}), 400
        user.phone = data['phone']
    if 'email' in data:
        if data['email'] and User.query.filter(User.email == data['email'], User.id != user_id).first():
            return jsonify({'success': False, 'message': '邮箱已被使用'}), 400
        user.email = data['email']
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({'success': True, 'message': '用户更新成功', 'data': user.to_dict()})

@users_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    operator_id = get_jwt_identity()
    current_user = User.query.get(operator_id)
    if not current_user:
        from models.user import Admin
        current_admin = Admin.query.get(operator_id)
        if not current_admin:
            return jsonify({'success': False, 'message': '权限不足'}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': '用户删除成功'})