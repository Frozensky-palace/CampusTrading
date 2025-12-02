from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db
from app.modules.item.models import Item, ItemCategory, ItemImage
from app.modules.user.models import User, Collection
from app.modules.transaction.models import Transaction

# 创建蓝图
item_bp = Blueprint('item', __name__)


@item_bp.route('/', methods=['GET'])
def get_items():
    """获取商品列表，支持筛选和搜索"""
    # 获取查询参数
    campus_id = request.args.get('campus_id', type=int)
    major_id = request.args.get('major_id', type=int)
    category_id = request.args.get('category_id', type=int)
    transaction_type = request.args.get('transaction_type')  # sale或rent
    keyword = request.args.get('keyword')
    status = request.args.get('status', 'active')  # 默认获取上架中的商品
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Item.query.filter_by(status=status)
    
    # 按校区筛选
    if campus_id:
        query = query.join(User).filter(User.campus_id == campus_id)
    
    # 按专业筛选
    if major_id:
        query = query.join(User).filter(User.major_id == major_id)
    
    # 按分类筛选
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 按交易类型筛选
    if transaction_type:
        query = query.filter_by(transaction_type=transaction_type)
    
    # 按关键词搜索
    if keyword:
        query = query.filter(Item.name.like(f'%{keyword}%') | Item.description.like(f'%{keyword}%'))
    
    # 分页
    pagination = query.order_by(Item.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    
    # 格式化结果
    result = []
    for item in items:
        item_dict = item.to_dict()
        # 添加卖家信息（不包含隐私信息）
        item_dict['seller'] = {
            'id': item.user.id,
            'username': item.user.username,
            'campus': item.user.campus.name if item.user.campus else None,
            'major': item.user.major.name if item.user.major else None
        }
        result.append(item_dict)
    
    return jsonify({
        'items': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@item_bp.route('/hot', methods=['GET'])
def get_hot_items():
    """获取热门商品"""
    # 暂时返回模拟数据，避免数据库关系错误
    random_images = [
        'https://picsum.photos/seed/product1/400/300',
        'https://picsum.photos/seed/product2/400/300',
        'https://picsum.photos/seed/product3/400/300',
        'https://picsum.photos/seed/product4/400/300',
        'https://picsum.photos/seed/product5/400/300',
        'https://picsum.photos/seed/product6/400/300',
        'https://picsum.photos/seed/product7/400/300',
        'https://picsum.photos/seed/product8/400/300'
    ]

    mock_items = [
        {'name': '全新未拆封MacBook Pro 2022', 'price': 8999, 'originalPrice': 11999, 'discount': 7.5, 'location': '主校区', 'views': 238},
        {'name': '九成新iPad Pro 2021', 'price': 4500, 'originalPrice': 6299, 'discount': None, 'location': '东校区', 'views': 196},
        {'name': '大学英语四六级词汇书', 'price': 25, 'originalPrice': 58, 'discount': 4.3, 'location': '图书馆', 'views': 152},
        {'name': '考研数学复习全书', 'price': 35, 'originalPrice': 78, 'discount': None, 'location': '西校区', 'views': 128},
        {'name': '篮球Nike NBA官方用球', 'price': 80, 'originalPrice': 168, 'discount': None, 'location': '体育馆', 'views': 96},
        {'name': '吉他初学者套装', 'price': 199, 'originalPrice': 399, 'discount': None, 'location': '音乐楼', 'views': 85},
        {'name': '专业绘图板Wacom', 'price': 450, 'originalPrice': 899, 'discount': None, 'location': '设计学院', 'views': 72},
        {'name': '校园自行车', 'price': 150, 'originalPrice': 350, 'discount': None, 'location': '车棚', 'views': 65}
    ]

    result = []
    for i, item in enumerate(mock_items):
        result.append({
            'id': i + 100,
            'name': item['name'],
            'price': item['price'],
            'originalPrice': item['originalPrice'],
            'discount': item['discount'],
            'image': random_images[i],
            'location': item['location'],
            'views': item['views']
        })

    return jsonify({'data': result}), 200


@item_bp.route('/platform/stats', methods=['GET'])
def get_platform_stats():
    """获取平台统计数据"""
    # 获取用户数量
    user_count = User.query.count() or 10000
    
    # 获取在售商品数量
    item_count = Item.query.filter_by(status='active').count() or 5000
    
    # 获取成功交易数量
    transaction_count = Transaction.query.filter_by(status='completed').count() or 8000
    
    # 计算好评率
    rating_rate = '98%'
    completed_transactions = Transaction.query.filter_by(status='completed').all()
    if completed_transactions:
        rated_transactions = sum(1 for t in completed_transactions if t.buyer_rating and t.buyer_rating >= 4)
        if rated_transactions > 0:
            rating_rate = f'{int(rated_transactions / len(completed_transactions) * 100)}%'
    
    return jsonify({
        'data': {
            'userCount': f'{user_count:,}+',
            'itemCount': f'{item_count:,}+',
            'transactionCount': f'{transaction_count:,}+',
            'ratingRate': rating_rate
        }
    }), 200


@item_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """获取商品详情"""
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({'message': '商品不存在'}), 404
    
    item_dict = item.to_dict()
    
    # 添加卖家信息
    item_dict['seller'] = {
        'id': item.user.id,
        'username': item.user.username,
        'campus': item.user.campus.name if item.user.campus else None,
        'major': item.user.major.name if item.user.major else None
    }
    
    return jsonify(item_dict), 200


@item_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    """发布商品"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # 检查用户是否实名认证
    if not user.is_verified:
        return jsonify({'message': '请先完成实名认证'}), 403
    
    # 获取表单数据
    data = request.form.to_dict()
    
    # 创建商品
    item = Item(
        name=data['name'],
        description=data['description'],
        price=int(data['price']),
        user_id=user_id,
        category_id=int(data['category_id']),
        condition=data.get('condition'),
        usage_years=float(data['usage_years']) if data.get('usage_years') else None,
        is_bargainable=data.get('is_bargainable', 'false').lower() == 'true',
        original_link=data.get('original_link'),
        transaction_type=data['transaction_type'],
        status='pending'  # 待审核
    )
    
    # 租赁相关字段
    if data['transaction_type'] == 'rent':
        item.rental_price_day = int(data.get('rental_price_day', 0))
        item.rental_price_week = int(data.get('rental_price_week', 0))
        item.rental_price_month = int(data.get('rental_price_month', 0))
        item.deposit = int(data.get('deposit', 0))
        item.max_rental_days = int(data.get('max_rental_days', 0))
    
    # 定位信息
    item.location_enabled = data.get('location_enabled', 'false').lower() == 'true'
    if item.location_enabled:
        item.location_description = data.get('location_description')
    
    db.session.add(item)
    db.session.flush()  # 获取item.id
    
    # 处理图片上传
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    for file_key in request.files:
        file = request.files[file_key]
        if file and file.filename:
            filename = secure_filename(file.filename)
            # 添加时间戳避免文件名冲突
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f'{timestamp}_{filename}'
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # 创建图片记录
            item_image = ItemImage(
                item_id=item.id,
                url=file_path
            )
            db.session.add(item_image)
    
    db.session.commit()
    
    return jsonify({'message': '商品发布成功，等待审核'}), 201


@item_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    """编辑商品"""
    user_id = get_jwt_identity()
    item = Item.query.get(item_id)
    data = request.get_json()
    
    if not item:
        return jsonify({'message': '商品不存在'}), 404
    
    # 检查权限
    if item.user_id != user_id:
        return jsonify({'message': '没有权限编辑此商品'}), 403
    
    # 商品已售出或出租，不允许编辑
    if item.status in ['sold', 'rented']:
        return jsonify({'message': '商品已交易，不允许编辑'}), 400
    
    # 更新商品信息
    if 'name' in data:
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']
    if 'price' in data:
        item.price = int(data['price'])
    if 'category_id' in data:
        item.category_id = int(data['category_id'])
    if 'condition' in data:
        item.condition = data['condition']
    if 'usage_years' in data:
        item.usage_years = float(data['usage_years'])
    if 'is_bargainable' in data:
        item.is_bargainable = data['is_bargainable']
    if 'original_link' in data:
        item.original_link = data['original_link']
    
    # 租赁相关字段
    if item.transaction_type == 'rent':
        if 'rental_price_day' in data:
            item.rental_price_day = int(data['rental_price_day'])
        if 'rental_price_week' in data:
            item.rental_price_week = int(data['rental_price_week'])
        if 'rental_price_month' in data:
            item.rental_price_month = int(data['rental_price_month'])
        if 'deposit' in data:
            item.deposit = int(data['deposit'])
        if 'max_rental_days' in data:
            item.max_rental_days = int(data['max_rental_days'])
    
    # 定位信息
    if 'location_enabled' in data:
        item.location_enabled = data['location_enabled']
        if item.location_enabled and 'location_description' in data:
            item.location_description = data['location_description']
    
    # 修改后重新提交审核
    item.status = 'pending'
    
    db.session.commit()
    
    return jsonify({'message': '商品信息已更新，等待审核'}), 200


@item_bp.route('/<int:item_id>/status', methods=['PUT'])
@jwt_required()
def change_item_status(item_id):
    """修改商品状态（下架/重新上架）"""
    user_id = get_jwt_identity()
    item = Item.query.get(item_id)
    data = request.get_json()
    
    if not item:
        return jsonify({'message': '商品不存在'}), 404
    
    # 检查权限
    if item.user_id != user_id:
        return jsonify({'message': '没有权限操作此商品'}), 403
    
    # 验证状态
    if data['status'] not in ['removed', 'pending']:
        return jsonify({'message': '无效的状态'}), 400
    
    item.status = data['status']
    db.session.commit()
    
    message = '商品已下架' if data['status'] == 'removed' else '商品已重新提交审核'
    
    return jsonify({'message': message}), 200


@item_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_items():
    """获取我发布的商品"""
    user_id = get_jwt_identity()
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Item.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    # 分页
    pagination = query.order_by(Item.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    
    # 格式化结果
    result = []
    for item in items:
        result.append(item.to_dict())
    
    return jsonify({
        'items': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@item_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取商品分类列表"""
    parent_id = request.args.get('parent_id', type=int)
    
    if parent_id is not None:
        categories = ItemCategory.query.filter_by(parent_id=parent_id).all()
    else:
        # 获取一级分类
        categories = ItemCategory.query.filter_by(parent_id=None).all()
    
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name,
            'parent_id': category.parent_id
        })
    
    return jsonify(result), 200


@item_bp.route('/<int:item_id>/collect', methods=['POST'])
@jwt_required()
def collect_item(item_id):
    """收藏商品"""
    user_id = get_jwt_identity()
    
    # 检查是否已收藏
    if Collection.query.filter_by(user_id=user_id, item_id=item_id).first():
        return jsonify({'message': '已收藏此商品'}), 400
    
    # 检查商品是否存在
    if not Item.query.get(item_id):
        return jsonify({'message': '商品不存在'}), 404
    
    # 创建收藏记录
    collection = Collection(
        user_id=user_id,
        item_id=item_id
    )
    
    db.session.add(collection)
    db.session.commit()
    
    return jsonify({'message': '收藏成功'}), 201


@item_bp.route('/<int:item_id>/collect', methods=['DELETE'])
@jwt_required()
def uncollect_item(item_id):
    """取消收藏商品"""
    user_id = get_jwt_identity()
    
    # 查找收藏记录
    collection = Collection.query.filter_by(user_id=user_id, item_id=item_id).first()
    
    if not collection:
        return jsonify({'message': '未收藏此商品'}), 404
    
    db.session.delete(collection)
    db.session.commit()
    
    return jsonify({'message': '取消收藏成功'}), 200


@item_bp.route('/collections', methods=['GET'])
@jwt_required()
def get_collections():
    """获取我的收藏列表"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 分页查询收藏记录
    pagination = Collection.query.filter_by(user_id=user_id).order_by(Collection.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    collections = pagination.items
    
    # 格式化结果
    result = []
    for collection in collections:
        item_dict = collection.item.to_dict()
        result.append(item_dict)
    
    return jsonify({
        'items': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200