from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from app import db
from app.modules.transaction.models import Transaction, Offer, Complaint
from app.modules.item.models import Item
from app.modules.user.models import User, CoinLog

# 创建蓝图
transaction_bp = Blueprint('transaction', __name__)


@transaction_bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    """创建交易订单"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 获取商品信息
    item = Item.query.get(data['item_id'])
    if not item:
        return jsonify({'message': '商品不存在'}), 404
    
    # 检查商品状态
    if item.status != 'active':
        return jsonify({'message': '商品状态不正确'}), 400
    
    # 检查卖家和买家是否为同一人
    if item.user_id == user_id:
        return jsonify({'message': '不能购买自己的商品'}), 400
    
    # 获取买家和卖家信息
    buyer = User.query.get(user_id)
    seller = User.query.get(item.user_id)
    
    # 计算交易金额
    if item.transaction_type == 'rent':
        # 租赁交易
        rental_days = data.get('rental_days', 1)
        if rental_days > item.max_rental_days:
            return jsonify({'message': '租赁天数超过最大允许天数'}), 400
        
        # 根据租赁天数计算租金
        if rental_days == 1:
            amount = item.rental_price_day
        elif rental_days <= 7:
            amount = item.rental_price_week
        else:
            # 按月计算
            months = rental_days // 30
            remaining_days = rental_days % 30
            amount = months * item.rental_price_month + remaining_days * (item.rental_price_day)
        
        # 加上押金
        total_amount = amount + item.deposit
        
        # 检查买家余额
        if buyer.coins < total_amount:
            return jsonify({'message': '校园币余额不足'}), 400
        
        # 创建交易记录
        transaction = Transaction(
            buyer_id=user_id,
            seller_id=item.user_id,
            item_id=item.id,
            amount=amount,
            deposit_paid=item.deposit,
            transaction_type='rent',
            rental_days=rental_days,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=rental_days),
            status='paid',
            is_escrowed=True
        )
        
        # 冻结买家资金
        buyer.coins -= total_amount
        
        # 记录资金变动
        coin_log = CoinLog(
            user_id=user_id,
            amount=-total_amount,
            type='rental_payment',
            related_id=transaction.id,
            description=f'租赁商品 {item.name} 支付'
        )
        
    else:
        # 出售交易
        # 检查是否使用还价
        final_price = item.price
        if data.get('offer_id'):
            offer = Offer.query.get(data['offer_id'])
            if not offer or offer.item_id != item.id or offer.buyer_id != user_id or offer.status != 'accepted':
                return jsonify({'message': '无效的还价'}), 400
            final_price = offer.offer_amount
        
        # 检查买家余额
        if buyer.coins < final_price:
            return jsonify({'message': '校园币余额不足'}), 400
        
        # 创建交易记录
        transaction = Transaction(
            buyer_id=user_id,
            seller_id=item.user_id,
            item_id=item.id,
            amount=final_price,
            transaction_type='sale',
            status='paid',
            is_escrowed=True
        )
        
        # 冻结买家资金
        buyer.coins -= final_price
        
        # 记录资金变动
        coin_log = CoinLog(
            user_id=user_id,
            amount=-final_price,
            type='purchase_payment',
            related_id=transaction.id,
            description=f'购买商品 {item.name} 支付'
        )
    
    db.session.add(transaction)
    db.session.add(coin_log)
    db.session.commit()
    
    return jsonify({'message': '交易创建成功', 'transaction_id': transaction.id}), 201


@transaction_bp.route('/<int:transaction_id>/confirm', methods=['POST'])
@jwt_required()
def confirm_transaction(transaction_id):
    """确认交易完成"""
    user_id = get_jwt_identity()
    transaction = Transaction.query.get(transaction_id)
    
    if not transaction:
        return jsonify({'message': '交易不存在'}), 404
    
    # 只有买家可以确认交易
    if transaction.buyer_id != user_id:
        return jsonify({'message': '没有权限确认此交易'}), 403
    
    # 检查交易状态
    if transaction.status != 'paid':
        return jsonify({'message': '交易状态不正确'}), 400
    
    # 更新交易状态
    transaction.status = 'completed'
    transaction.completed_at = datetime.utcnow()
    transaction.escrow_released_at = datetime.utcnow()
    
    # 获取卖家信息
    seller = User.query.get(transaction.seller_id)
    
    # 将资金转给卖家
    seller.coins += transaction.amount
    
    # 记录资金变动
    seller_coin_log = CoinLog(
        user_id=seller.id,
        amount=transaction.amount,
        type='transaction_receipt',
        related_id=transaction.id,
        description=f'销售商品收款'
    )
    
    # 更新商品状态
    item = Item.query.get(transaction.item_id)
    if transaction.transaction_type == 'sale':
        item.status = 'sold'
    else:
        item.status = 'active'  # 租赁结束后商品可再次出租
    
    db.session.add(seller_coin_log)
    db.session.commit()
    
    return jsonify({'message': '交易已完成'}), 200


@transaction_bp.route('/<int:transaction_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_transaction(transaction_id):
    """取消交易"""
    user_id = get_jwt_identity()
    transaction = Transaction.query.get(transaction_id)
    
    if not transaction:
        return jsonify({'message': '交易不存在'}), 404
    
    # 只有买家可以取消交易
    if transaction.buyer_id != user_id:
        return jsonify({'message': '没有权限取消此交易'}), 403
    
    # 检查交易状态
    if transaction.status != 'paid':
        return jsonify({'message': '交易状态不正确'}), 400
    
    # 更新交易状态
    transaction.status = 'canceled'
    transaction.canceled_at = datetime.utcnow()
    
    # 获取买家信息
    buyer = User.query.get(user_id)
    
    # 退还买家资金
    refund_amount = transaction.amount
    if transaction.transaction_type == 'rent':
        refund_amount += transaction.deposit
    
    buyer.coins += refund_amount
    
    # 记录资金变动
    coin_log = CoinLog(
        user_id=user_id,
        amount=refund_amount,
        type='transaction_refund',
        related_id=transaction.id,
        description=f'交易取消退款'
    )
    
    # 更新商品状态
    item = Item.query.get(transaction.item_id)
    item.status = 'active'
    
    db.session.add(coin_log)
    db.session.commit()
    
    return jsonify({'message': '交易已取消，资金已退还'}), 200


@transaction_bp.route('/my/purchases', methods=['GET'])
@jwt_required()
def get_my_purchases():
    """获取我的购买记录"""
    user_id = get_jwt_identity()
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Transaction.query.filter_by(buyer_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    # 分页
    pagination = query.order_by(Transaction.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    transactions = pagination.items
    
    # 格式化结果
    result = []
    for transaction in transactions:
        transaction_dict = transaction.to_dict()
        # 添加商品信息
        transaction_dict['item'] = {
            'id': transaction.item.id,
            'name': transaction.item.name,
            'images': [img.url for img in transaction.item.item_images]
        }
        result.append(transaction_dict)
    
    return jsonify({
        'transactions': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@transaction_bp.route('/my/sales', methods=['GET'])
@jwt_required()
def get_my_sales():
    """获取我的销售记录"""
    user_id = get_jwt_identity()
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Transaction.query.filter_by(seller_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    # 分页
    pagination = query.order_by(Transaction.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    transactions = pagination.items
    
    # 格式化结果
    result = []
    for transaction in transactions:
        transaction_dict = transaction.to_dict()
        # 添加商品信息
        transaction_dict['item'] = {
            'id': transaction.item.id,
            'name': transaction.item.name,
            'images': [img.url for img in transaction.item.item_images]
        }
        # 添加买家信息（匿名）
        transaction_dict['buyer'] = {
            'id': transaction.buyer.id,
            'username': transaction.buyer.username
        }
        result.append(transaction_dict)
    
    return jsonify({
        'transactions': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@transaction_bp.route('/<int:transaction_id>/review', methods=['POST'])
@jwt_required()
def review_transaction(transaction_id):
    """评价交易"""
    user_id = get_jwt_identity()
    data = request.get_json()
    transaction = Transaction.query.get(transaction_id)
    
    if not transaction:
        return jsonify({'message': '交易不存在'}), 404
    
    # 检查交易是否已完成
    if transaction.status != 'completed':
        return jsonify({'message': '交易未完成，无法评价'}), 400
    
    # 获取评价奖励
    from config.development import DevelopmentConfig
    reward_coins = DevelopmentConfig.REVIEW_REWARD_COINS
    
    if transaction.buyer_id == user_id:
        # 买家评价卖家
        transaction.buyer_rating = data.get('rating')
        transaction.buyer_comment = data.get('comment')
        
        # 奖励买家校园币
        buyer = User.query.get(user_id)
        buyer.coins += reward_coins
        
        # 记录资金变动
        coin_log = CoinLog(
            user_id=user_id,
            amount=reward_coins,
            type='review_reward',
            related_id=transaction.id,
            description='评价奖励'
        )
        
        db.session.add(coin_log)
    elif transaction.seller_id == user_id:
        # 卖家评价买家
        transaction.seller_rating = data.get('rating')
        transaction.seller_comment = data.get('comment')
        
        # 奖励卖家校园币
        seller = User.query.get(user_id)
        seller.coins += reward_coins
        
        # 记录资金变动
        coin_log = CoinLog(
            user_id=user_id,
            amount=reward_coins,
            type='review_reward',
            related_id=transaction.id,
            description='评价奖励'
        )
        
        db.session.add(coin_log)
    else:
        return jsonify({'message': '没有权限评价此交易'}), 403
    
    db.session.commit()
    
    return jsonify({'message': '评价成功，已获得奖励'}), 200


@transaction_bp.route('/offers', methods=['POST'])
@jwt_required()
def create_offer():
    """发起还价"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 获取商品信息
    item = Item.query.get(data['item_id'])
    if not item:
        return jsonify({'message': '商品不存在'}), 404
    
    # 检查商品是否支持砍价
    if not item.is_bargainable:
        return jsonify({'message': '该商品不支持砍价'}), 400
    
    # 检查商品状态
    if item.status != 'active':
        return jsonify({'message': '商品状态不正确'}), 400
    
    # 检查是否为自己的商品
    if item.user_id == user_id:
        return jsonify({'message': '不能对自己的商品还价'}), 400
    
    # 创建还价记录
    offer = Offer(
        buyer_id=user_id,
        item_id=item.id,
        offer_amount=data['offer_amount']
    )
    
    db.session.add(offer)
    db.session.commit()
    
    return jsonify({'message': '还价请求已发送'}), 201


@transaction_bp.route('/offers/my', methods=['GET'])
@jwt_required()
def get_my_offers():
    """获取我发起的还价"""
    user_id = get_jwt_identity()
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Offer.query.filter_by(buyer_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    # 分页
    pagination = query.order_by(Offer.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    offers = pagination.items
    
    # 格式化结果
    result = []
    for offer in offers:
        offer_dict = offer.to_dict()
        # 添加商品信息
        offer_dict['item'] = {
            'id': offer.item.id,
            'name': offer.item.name,
            'price': offer.item.price
        }
        result.append(offer_dict)
    
    return jsonify({
        'offers': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@transaction_bp.route('/offers/received', methods=['GET'])
@jwt_required()
def get_received_offers():
    """获取收到的还价"""
    user_id = get_jwt_identity()
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Offer.query.join(Item).filter(Item.user_id == user_id)
    if status:
        query = query.filter_by(status=status)
    
    # 分页
    pagination = query.order_by(Offer.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    offers = pagination.items
    
    # 格式化结果
    result = []
    for offer in offers:
        offer_dict = offer.to_dict()
        # 添加商品信息
        offer_dict['item'] = {
            'id': offer.item.id,
            'name': offer.item.name,
            'price': offer.item.price
        }
        # 添加买家信息（匿名）
        offer_dict['buyer'] = {
            'id': offer.buyer.id,
            'username': offer.buyer.username
        }
        result.append(offer_dict)
    
    return jsonify({
        'offers': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@transaction_bp.route('/offers/<int:offer_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_offer(offer_id):
    """回应还价请求"""
    user_id = get_jwt_identity()
    data = request.get_json()
    offer = Offer.query.get(offer_id)
    
    if not offer:
        return jsonify({'message': '还价请求不存在'}), 404
    
    # 检查是否为商品卖家
    if offer.item.user_id != user_id:
        return jsonify({'message': '没有权限回应此还价'}), 403
    
    # 检查还价状态
    if offer.status != 'pending':
        return jsonify({'message': '还价请求状态不正确'}), 400
    
    # 检查回应类型
    if data['action'] not in ['accept', 'reject']:
        return jsonify({'message': '无效的回应类型'}), 400
    
    # 更新还价状态
    offer.status = 'accepted' if data['action'] == 'accept' else 'rejected'
    offer.responded_at = datetime.utcnow()
    
    db.session.commit()
    
    message = '还价已接受' if data['action'] == 'accept' else '还价已拒绝'
    
    return jsonify({'message': message}), 200


@transaction_bp.route('/complaints', methods=['POST'])
@jwt_required()
def create_complaint():
    """提交投诉"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 检查交易是否存在
    transaction = Transaction.query.get(data['transaction_id'])
    if not transaction:
        return jsonify({'message': '交易不存在'}), 404
    
    # 检查用户是否为交易参与方
    if transaction.buyer_id != user_id and transaction.seller_id != user_id:
        return jsonify({'message': '没有权限投诉'}), 403
    
    # 确定被投诉方
    defendant_id = transaction.seller_id if transaction.buyer_id == user_id else transaction.buyer_id
    
    # 创建投诉记录
    complaint = Complaint(
        complainant_id=user_id,
        defendant_id=defendant_id,
        transaction_id=transaction.id,
        reason=data['reason']
    )
    
    # 更新交易状态为纠纷中
    transaction.status = 'disputed'
    
    db.session.add(complaint)
    db.session.commit()
    
    return jsonify({'message': '投诉已提交，请等待管理员处理'}), 201