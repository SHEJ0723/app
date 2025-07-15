from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Bill

bills_bp = Blueprint('bills', __name__)

@bills_bp.route('/api/bills', methods=['GET'])
@jwt_required()
def get_bills():
    """获取账单列表，用户端只查自己，管理端可查全部"""
    user_id = get_jwt_identity()
    role = request.headers.get('X-Require-Role', 'user')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    query = Bill.query
    if role != 'admin':
        query = query.filter_by(user_id=user_id)
    total = query.count()
    bills = query.order_by(Bill.created_at.desc()).offset((page-1)*per_page).limit(per_page).all()
    return jsonify({
        'success': True,
        'data': [b.to_dict() for b in bills],
        'total': total
    })

@bills_bp.route('/api/bills', methods=['POST'])
@jwt_required()
def create_bill():
    """管理端新增账单"""
    data = request.get_json()
    bill = Bill(
        user_id=data['user_id'],
        order_id=data['order_id'],
        amount=data.get('amount', 0.0),
        pay_time=data.get('pay_time'),
        status=data.get('status', '未支付'),
        pay_method=data.get('pay_method')
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify({'success': True, 'data': bill.to_dict()})

@bills_bp.route('/api/bills/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(bill_id):
    """管理端删除账单"""
    bill = Bill.query.get(bill_id)
    if not bill:
        return jsonify({'success': False, 'message': '账单不存在'}), 404
    db.session.delete(bill)
    db.session.commit()
    return jsonify({'success': True, 'message': '账单已删除'}) 