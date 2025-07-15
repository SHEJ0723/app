from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """获取订单列表，用户端只查自己，管理端可查全部"""
    user_id = get_jwt_identity()
    role = request.headers.get('X-Require-Role', 'user')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    query = Order.query
    if role != 'admin':
        query = query.filter_by(user_id=user_id)
    total = query.count()
    orders = query.order_by(Order.created_at.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({
        'success': True,
        'data': [o.to_dict() for o in orders],
        'total': total
    })

@orders_bp.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    """管理端新增订单"""
    data = request.get_json()
    order = Order(
        user_id=data['user_id'],
        spot_id=data['spot_id'],
        start_time=data['start_time'],
        end_time=data.get('end_time'),
        status=data.get('status', '未支付'),
        amount=data.get('amount', 0.0),
        pay_method=data.get('pay_method')
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({'success': True, 'data': order.to_dict()})

@orders_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    """管理端删除订单"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'success': False, 'message': '订单不存在'}), 404
    db.session.delete(order)
    db.session.commit()
    return jsonify({'success': True, 'message': '订单已删除'})

@orders_bp.route('/api/orders/<int:order_id>/pay', methods=['POST'])
@jwt_required()
def pay_order(order_id):
    """用户支付订单，支持支付宝/微信"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'success': False, 'message': '订单不存在'}), 404
    data = request.get_json()
    pay_method = data.get('pay_method')
    if pay_method not in ['支付宝', '微信']:
        return jsonify({'success': False, 'message': '不支持的支付方式'}), 400
    order.status = '已完成'
    order.pay_method = pay_method
    db.session.commit()
    return jsonify({'success': True, 'message': '支付成功', 'data': order.to_dict()}) 