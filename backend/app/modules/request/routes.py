from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.modules.request.models import ItemRequest, RequestResponse
from app.modules.item.models import ItemCategory

# 创建蓝图
request_bp = Blueprint('request', __name__)


@request_bp.route('/', methods=['POST'])
@jwt_required()
def create_item_request():
    """发布求购信息"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 创建求购信息
    item_request = ItemRequest(
        user_id=user_id,
        title=data['title'],
        description=data['description'],
        expected_price=int(data['expected_price']),
        category_id=int(data['category_id'])
    )
    
    # 设置专业和校区范围
    if 'major_id' in data:
        item_request.major_id = data['major_id']
    if 'campus_id' in data:
        item_request.campus_id = data['campus_id']
    
    db.session.add(item_request)
    db.session.commit()
    
    return jsonify({'message': '求购信息发布成功', 'request_id': item_request.id}), 201


@request_bp.route('/', methods=['GET'])
def get_item_requests():
    """获取求购信息列表，支持筛选和搜索"""
    # 获取查询参数
    campus_id = request.args.get('campus_id', type=int)
    major_id = request.args.get('major_id', type=int)
    category_id = request.args.get('category_id', type=int)
    keyword = request.args.get('keyword')
    status = request.args.get('status', 'active')  # 默认获取有效的求购信息
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = ItemRequest.query.filter_by(status=status)
    
    # 按校区筛选
    if campus_id:
        query = query.filter_by(campus_id=campus_id)
    
    # 按专业筛选
    if major_id:
        query = query.filter_by(major_id=major_id)
    
    # 按分类筛选
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 按关键词搜索
    if keyword:
        query = query.filter(ItemRequest.title.like(f'%{keyword}%') | ItemRequest.description.like(f'%{keyword}%'))
    
    # 分页
    pagination = query.order_by(ItemRequest.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    requests = pagination.items
    
    # 格式化结果
    result = []
    for item_request in requests:
        request_dict = item_request.to_dict()
        # 添加分类信息
        category = ItemCategory.query.get(item_request.category_id)
        if category:
            request_dict['category_name'] = category.name
        result.append(request_dict)
    
    return jsonify({
        'requests': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@request_bp.route('/latest', methods=['GET'])
def get_latest_requests():
    """获取最新求购信息"""
    from datetime import datetime

    # 暂时返回模拟数据
    mock_requests = [
        {'id': 1, 'title': '求购二手考研政治资料', 'content': '求购最新版考研政治全套资料...', 'tags': ['考研', '政治'], 'minPrice': 50, 'maxPrice': 150, 'createdAt': int(datetime.utcnow().timestamp() * 1000) - 3600000},
        {'id': 2, 'title': '寻找二手专业相机', 'content': '求购一台入门级单反或微单相机...', 'tags': ['相机', '数码'], 'minPrice': 1500, 'maxPrice': 2500, 'createdAt': int(datetime.utcnow().timestamp() * 1000) - 7200000},
        {'id': 3, 'title': '求购二手电动车', 'content': '求购一辆二手电动车，电池续航至少30公里...', 'tags': ['电动车', '出行'], 'minPrice': 800, 'maxPrice': 1500, 'createdAt': int(datetime.utcnow().timestamp() * 1000) - 10800000},
        {'id': 4, 'title': '收购计算机专业教材', 'content': '收购计算机科学与技术专业大二教材...', 'tags': ['教材', '计算机'], 'minPrice': 100, 'maxPrice': 300, 'createdAt': int(datetime.utcnow().timestamp() * 1000) - 14400000},
        {'id': 5, 'title': '求购二手空调', 'content': '求购一台1.5匹二手空调...', 'tags': ['电器', '空调'], 'minPrice': 800, 'maxPrice': 1200, 'createdAt': int(datetime.utcnow().timestamp() * 1000) - 18000000},
    ]

    return jsonify({'data': mock_requests}), 200


# get_my_requests函数将在后面定义


@request_bp.route('/<int:request_id>', methods=['GET'])
def get_item_request(request_id):
    """获取求购信息详情"""
    item_request = ItemRequest.query.get(request_id)
    
    if not item_request:
        return jsonify({'message': '求购信息不存在'}), 404
    
    request_dict = item_request.to_dict()
    
    # 添加分类信息
    category = ItemCategory.query.get(item_request.category_id)
    if category:
        request_dict['category_name'] = category.name
    
    return jsonify(request_dict), 200


@request_bp.route('/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_item_request(request_id):
    """更新求购信息"""
    user_id = get_jwt_identity()
    item_request = ItemRequest.query.get(request_id)
    data = request.get_json()
    
    if not item_request:
        return jsonify({'message': '求购信息不存在'}), 404
    
    # 检查权限
    if item_request.user_id != user_id:
        return jsonify({'message': '没有权限更新此求购信息'}), 403
    
    # 检查求购信息状态
    if item_request.status != 'active':
        return jsonify({'message': '求购信息状态不正确'}), 400
    
    # 更新求购信息
    if 'title' in data:
        item_request.title = data['title']
    if 'description' in data:
        item_request.description = data['description']
    if 'expected_price' in data:
        item_request.expected_price = int(data['expected_price'])
    if 'category_id' in data:
        item_request.category_id = int(data['category_id'])
    if 'major_id' in data:
        item_request.major_id = data['major_id']
    if 'campus_id' in data:
        item_request.campus_id = data['campus_id']
    
    db.session.commit()
    
    return jsonify({'message': '求购信息已更新'}), 200


@request_bp.route('/<int:request_id>/status', methods=['PUT'])
@jwt_required()
def change_request_status(request_id):
    """修改求购信息状态（取消/标记为已匹配）"""
    user_id = get_jwt_identity()
    item_request = ItemRequest.query.get(request_id)
    data = request.get_json()
    
    if not item_request:
        return jsonify({'message': '求购信息不存在'}), 404
    
    # 检查权限
    if item_request.user_id != user_id:
        return jsonify({'message': '没有权限操作此求购信息'}), 403
    
    # 验证状态
    if data['status'] not in ['canceled', 'matched']:
        return jsonify({'message': '无效的状态'}), 400
    
    item_request.status = data['status']
    db.session.commit()
    
    message = '求购信息已取消' if data['status'] == 'canceled' else '求购信息已标记为已匹配'
    
    return jsonify({'message': message}), 200


@request_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_requests():
    """获取我发布的求购信息"""
    user_id = get_jwt_identity()
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = ItemRequest.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    # 分页
    pagination = query.order_by(ItemRequest.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    requests = pagination.items
    
    # 格式化结果
    result = []
    for item_request in requests:
        result.append(item_request.to_dict())
    
    return jsonify({
        'requests': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@request_bp.route('/<int:request_id>/responses', methods=['POST'])
@jwt_required()
def respond_to_request(request_id):
    """响应求购信息（报价）"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 获取求购信息
    item_request = ItemRequest.query.get(request_id)
    if not item_request:
        return jsonify({'message': '求购信息不存在'}), 404
    
    # 检查求购信息状态
    if item_request.status != 'active':
        return jsonify({'message': '求购信息状态不正确'}), 400
    
    # 检查是否为自己的求购信息
    if item_request.user_id == user_id:
        return jsonify({'message': '不能响应自己的求购信息'}), 400
    
    # 创建求购响应
    request_response = RequestResponse(
        request_id=request_id,
        responder_id=user_id,
        offer_amount=int(data['offer_amount']),
        message=data.get('message')
    )
    
    db.session.add(request_response)
    db.session.commit()
    
    return jsonify({'message': '报价已提交'}), 201


@request_bp.route('/my/responses', methods=['GET'])
@jwt_required()
def get_my_responses():
    """获取我收到的报价（我发布的求购信息的响应）"""
    user_id = get_jwt_identity()
    request_id = request.args.get('request_id', type=int)
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = RequestResponse.query.join(ItemRequest).filter(ItemRequest.user_id == user_id)
    
    # 按求购信息ID筛选
    if request_id:
        query = query.filter(RequestResponse.request_id == request_id)
    
    # 按状态筛选
    if status:
        query = query.filter_by(status=status)
    
    # 分页
    pagination = query.order_by(RequestResponse.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    responses = pagination.items
    
    # 格式化结果
    result = []
    for response in responses:
        response_dict = response.to_dict()
        # 添加求购信息
        response_dict['request'] = {
            'id': response.item_request.id,
            'title': response.item_request.title
        }
        # 添加响应者信息（匿名）
        response_dict['responder'] = {
            'id': response.responder.id,
            'username': response.responder.username,
            'campus': response.responder.campus.name if response.responder.campus else None,
            'major': response.responder.major.name if response.responder.major else None
        }
        result.append(response_dict)
    
    return jsonify({
        'responses': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@request_bp.route('/my/offers', methods=['GET'])
@jwt_required()
def get_my_offers():
    """获取我发出的报价（我响应的求购信息）"""
    user_id = get_jwt_identity()
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = RequestResponse.query.filter_by(responder_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    # 分页
    pagination = query.order_by(RequestResponse.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    responses = pagination.items
    
    # 格式化结果
    result = []
    for response in responses:
        response_dict = response.to_dict()
        # 添加求购信息
        response_dict['request'] = {
            'id': response.item_request.id,
            'title': response.item_request.title,
            'expected_price': response.item_request.expected_price
        }
        result.append(response_dict)
    
    return jsonify({
        'offers': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@request_bp.route('/responses/<int:response_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_response(response_id):
    """回应报价（接受/拒绝）"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 获取报价
    request_response = RequestResponse.query.get(response_id)
    if not request_response:
        return jsonify({'message': '报价不存在'}), 404
    
    # 检查是否为求购信息发布者
    if request_response.item_request.user_id != user_id:
        return jsonify({'message': '没有权限回应此报价'}), 403
    
    # 检查报价状态
    if request_response.status != 'pending':
        return jsonify({'message': '报价状态不正确'}), 400
    
    # 检查回应类型
    if data['action'] not in ['accept', 'reject']:
        return jsonify({'message': '无效的回应类型'}), 400
    
    # 更新报价状态
    request_response.status = 'accepted' if data['action'] == 'accept' else 'rejected'
    request_response.responded_at = datetime.utcnow()
    
    # 如果接受报价，更新求购信息状态为已匹配
    if data['action'] == 'accept':
        request_response.item_request.status = 'matched'
    
    db.session.commit()
    
    message = '报价已接受' if data['action'] == 'accept' else '报价已拒绝'
    
    return jsonify({'message': message}), 200