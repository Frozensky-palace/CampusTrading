from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
from app import db
from app.modules.admin.models import (
    AdminUser, ItemReview, Complaint, School, Campus,
    Major, ItemCategory, SystemLog, SystemConfig
)
from app.modules.item.models import Item
from app.modules.transaction.models import Transaction
from app.modules.user.models import User
import functools

# 创建蓝图
admin_bp = Blueprint('admin', __name__)


# 管理员权限验证装饰器
def admin_required(role=None):
    def decorator(f):
        @jwt_required()
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            admin_user = AdminUser.query.get(user_id)
            
            if not admin_user:
                return jsonify({'message': '管理员权限不足'}), 403
            
            if role and admin_user.role != role:
                return jsonify({'message': '角色权限不足'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空'}), 400
    
    # 查找管理员用户
    admin_user = AdminUser.query.filter_by(username=username).first()
    
    if not admin_user or not admin_user.check_password(password):
        return jsonify({'message': '用户名或密码错误'}), 401
    
    # 创建token
    access_token = create_access_token(
        identity=admin_user.id,
        additional_claims={'user_type': 'admin', 'role': admin_user.role},
        expires_delta=timedelta(hours=24)
    )
    
    # 记录登录日志
    log = SystemLog(
        log_type='admin_action',
        admin_id=admin_user.id,
        action='login',
        details=f'管理员{admin_user.username}登录成功',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'access_token': access_token,
        'admin_info': admin_user.to_dict()
    }), 200


@admin_bp.route('/profile', methods=['GET'])
@admin_required()
def get_admin_profile():
    """获取管理员个人信息"""
    admin_id = get_jwt_identity()
    admin_user = AdminUser.query.get(admin_id)
    
    return jsonify(admin_user.to_dict()), 200


@admin_bp.route('/profile/password', methods=['PUT'])
@admin_required()
def change_admin_password():
    """修改管理员密码"""
    admin_id = get_jwt_identity()
    admin_user = AdminUser.query.get(admin_id)
    data = request.get_json()
    
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'message': '当前密码和新密码不能为空'}), 400
    
    # 验证当前密码
    if not admin_user.check_password(current_password):
        return jsonify({'message': '当前密码错误'}), 401
    
    # 设置新密码
    admin_user.set_password(new_password)
    db.session.commit()
    
    # 记录日志
    log = SystemLog(
        log_type='admin_action',
        admin_id=admin_id,
        action='change_password',
        details='修改密码成功'
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': '密码修改成功'}), 200


@admin_bp.route('/item_reviews', methods=['GET'])
@admin_required()
def get_item_reviews():
    """获取待审核商品列表"""
    status = request.args.get('status', 'pending')  # 默认获取待审核商品
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = ItemReview.query.filter_by(status=status).order_by(ItemReview.created_at.desc())
    
    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    reviews = pagination.items
    
    # 格式化结果
    result = []
    for review in reviews:
        review_dict = review.to_dict()
        # 添加商品详细信息
        if review.item:
            review_dict['item_details'] = {
                'id': review.item.id,
                'title': review.item.title,
                'description': review.item.description,
                'price': review.item.price,
                'images': [img.url for img in review.item.images],
                'user_info': {
                    'id': review.item.user.id,
                    'username': review.item.user.username,
                    'school': review.item.user.school.name if review.item.user.school else None,
                    'campus': review.item.user.campus.name if review.item.user.campus else None,
                    'major': review.item.user.major.name if review.item.user.major else None
                }
            }
        result.append(review_dict)
    
    return jsonify({
        'reviews': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@admin_bp.route('/item_reviews/<int:review_id>', methods=['PUT'])
@admin_required()
def review_item(review_id):
    """审核商品"""
    admin_id = get_jwt_identity()
    review = ItemReview.query.get(review_id)
    data = request.get_json()
    
    if not review:
        return jsonify({'message': '审核记录不存在'}), 404
    
    # 检查状态
    if review.status != 'pending':
        return jsonify({'message': '商品已审核'}), 400
    
    # 验证审核结果
    status = data.get('status')
    if status not in ['approved', 'rejected']:
        return jsonify({'message': '无效的审核结果'}), 400
    
    # 更新审核记录
    review.status = status
    review.admin_id = admin_id
    review.comment = data.get('comment')
    review.reviewed_at = datetime.utcnow()
    
    # 更新商品状态
    if review.item:
        review.item.status = 'active' if status == 'approved' else 'rejected'
    
    db.session.commit()
    
    # 记录日志
    log = SystemLog(
        log_type='admin_action',
        admin_id=admin_id,
        action='review_item',
        details=f'商品ID {review.item_id} 审核结果: {status}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    message = '商品审核通过' if status == 'approved' else '商品审核拒绝'
    
    return jsonify({'message': message}), 200


@admin_bp.route('/complaints', methods=['GET'])
@admin_required()
def get_complaints():
    """获取投诉列表"""
    status = request.args.get('status')
    target_type = request.args.get('target_type')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Complaint.query.order_by(Complaint.created_at.desc())
    
    # 按状态筛选
    if status:
        query = query.filter_by(status=status)
    
    # 按目标类型筛选
    if target_type:
        query = query.filter_by(target_type=target_type)
    
    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    complaints = pagination.items
    
    # 格式化结果
    result = []
    for complaint in complaints:
        result.append(complaint.to_dict())
    
    return jsonify({
        'complaints': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@admin_bp.route('/complaints/<int:complaint_id>', methods=['PUT'])
@admin_required()
def handle_complaint(complaint_id):
    """处理投诉"""
    admin_id = get_jwt_identity()
    complaint = Complaint.query.get(complaint_id)
    data = request.get_json()
    
    if not complaint:
        return jsonify({'message': '投诉记录不存在'}), 404
    
    # 更新投诉状态
    complaint.status = data.get('status', 'processing')
    complaint.admin_id = admin_id
    complaint.admin_comment = data.get('comment')
    
    db.session.commit()
    
    # 记录日志
    log = SystemLog(
        log_type='admin_action',
        admin_id=admin_id,
        action='handle_complaint',
        details=f'投诉ID {complaint_id} 处理结果: {complaint.status}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': '投诉处理成功'}), 200


@admin_bp.route('/users', methods=['GET'])
@admin_required()
def get_users():
    """获取用户列表"""
    school_id = request.args.get('school_id', type=int)
    campus_id = request.args.get('campus_id', type=int)
    major_id = request.args.get('major_id', type=int)
    verified = request.args.get('verified', type=bool)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = User.query
    
    # 按学校筛选
    if school_id:
        query = query.filter_by(school_id=school_id)
    
    # 按校区筛选
    if campus_id:
        query = query.filter_by(campus_id=campus_id)
    
    # 按专业筛选
    if major_id:
        query = query.filter_by(major_id=major_id)
    
    # 按实名认证状态筛选
    if verified is not None:
        query = query.filter_by(verified=verified)
    
    # 分页
    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items
    
    # 格式化结果
    result = []
    for user in users:
        user_dict = user.to_dict()
        # 简化用户信息，不包含敏感信息
        user_dict.pop('student_id', None)
        user_dict.pop('email', None)
        user_dict.pop('real_name', None)
        result.append(user_dict)
    
    return jsonify({
        'users': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required()
def get_user_detail(user_id):
    """获取用户详细信息"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    return jsonify(user.to_dict()), 200


@admin_bp.route('/schools', methods=['GET'])
@admin_required()
def get_schools():
    """获取学校列表"""
    province = request.args.get('province')
    city = request.args.get('city')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = School.query
    
    # 按省份筛选
    if province:
        query = query.filter_by(province=province)
    
    # 按城市筛选
    if city:
        query = query.filter_by(city=city)
    
    # 分页
    pagination = query.order_by(School.name).paginate(page=page, per_page=per_page, error_out=False)
    schools = pagination.items
    
    # 格式化结果
    result = []
    for school in schools:
        result.append(school.to_dict())
    
    return jsonify({
        'schools': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@admin_bp.route('/schools', methods=['POST'])
@admin_required(role='super_admin')
def create_school():
    """添加学校"""
    data = request.get_json()
    
    # 检查学校是否已存在
    if School.query.filter_by(name=data['name']).first():
        return jsonify({'message': '学校已存在'}), 400
    
    # 创建学校
    school = School(
        name=data['name'],
        province=data.get('province'),
        city=data.get('city')
    )
    
    db.session.add(school)
    db.session.commit()
    
    # 记录日志
    admin_id = get_jwt_identity()
    log = SystemLog(
        log_type='admin_action',
        admin_id=admin_id,
        action='create_school',
        details=f'添加学校: {school.name}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'message': '学校添加成功',
        'school': school.to_dict()
    }), 201


@admin_bp.route('/campuses', methods=['GET'])
@admin_required()
def get_campuses():
    """获取校区列表"""
    school_id = request.args.get('school_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Campus.query
    
    # 按学校筛选
    if school_id:
        query = query.filter_by(school_id=school_id)
    
    # 分页
    pagination = query.order_by(Campus.name).paginate(page=page, per_page=per_page, error_out=False)
    campuses = pagination.items
    
    # 格式化结果
    result = []
    for campus in campuses:
        result.append(campus.to_dict())
    
    return jsonify({
        'campuses': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@admin_bp.route('/campuses', methods=['POST'])
@admin_required()
def create_campus():
    """添加校区"""
    data = request.get_json()
    
    # 创建校区
    campus = Campus(
        school_id=data['school_id'],
        name=data['name'],
        address=data.get('address')
    )
    
    db.session.add(campus)
    db.session.commit()
    
    # 记录日志
    admin_id = get_jwt_identity()
    log = SystemLog(
        log_type='admin_action',
        admin_id=admin_id,
        action='create_campus',
        details=f'添加校区: {campus.name} (学校ID: {campus.school_id})',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'message': '校区添加成功',
        'campus': campus.to_dict()
    }), 201


@admin_bp.route('/majors', methods=['GET'])
@admin_required()
def get_majors():
    """获取专业列表"""
    school_id = request.args.get('school_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Major.query
    
    # 按学校筛选
    if school_id:
        query = query.filter_by(school_id=school_id)
    
    # 分页
    pagination = query.order_by(Major.name).paginate(page=page, per_page=per_page, error_out=False)
    majors = pagination.items
    
    # 格式化结果
    result = []
    for major in majors:
        result.append(major.to_dict())
    
    return jsonify({
        'majors': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@admin_bp.route('/majors', methods=['POST'])
@admin_required()
def create_major():
    """添加专业"""
    data = request.get_json()
    
    # 创建专业
    major = Major(
        name=data['name'],
        school_id=data['school_id']
    )
    
    db.session.add(major)
    db.session.commit()
    
    # 记录日志
    admin_id = get_jwt_identity()
    log = SystemLog(
        log_type='admin_action',
        admin_id=admin_id,
        action='create_major',
        details=f'添加专业: {major.name} (学校ID: {major.school_id})',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'message': '专业添加成功',
        'major': major.to_dict()
    }), 201


@admin_bp.route('/system_logs', methods=['GET'])
@admin_required(role='super_admin')
def get_system_logs():
    """获取系统日志"""
    log_type = request.args.get('log_type')
    user_id = request.args.get('user_id', type=int)
    admin_id = request.args.get('admin_id', type=int)
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = SystemLog.query.order_by(SystemLog.created_at.desc())
    
    # 按日志类型筛选
    if log_type:
        query = query.filter_by(log_type=log_type)
    
    # 按用户ID筛选
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    # 按管理员ID筛选
    if admin_id:
        query = query.filter_by(admin_id=admin_id)
    
    # 按时间范围筛选
    if start_time:
        start_datetime = datetime.fromisoformat(start_time)
        query = query.filter(SystemLog.created_at >= start_datetime)
    
    if end_time:
        end_datetime = datetime.fromisoformat(end_time)
        query = query.filter(SystemLog.created_at <= end_datetime)
    
    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    logs = pagination.items
    
    # 格式化结果
    result = []
    for log in logs:
        result.append(log.to_dict())
    
    return jsonify({
        'logs': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@admin_bp.route('/system_configs', methods=['GET'])
@admin_required()
def get_system_configs():
    """获取系统配置"""
    configs = SystemConfig.query.all()
    
    # 格式化结果
    result = {}
    for config in configs:
        result[config.key] = config.to_dict()
    
    return jsonify(result), 200


@admin_bp.route('/system_configs/<string:key>', methods=['PUT'])
@admin_required(role='super_admin')
def update_system_config(key):
    """更新系统配置"""
    config = SystemConfig.query.filter_by(key=key).first()
    data = request.get_json()
    
    if not config:
        # 创建新配置
        config = SystemConfig(
            key=key,
            value=data['value'],
            description=data.get('description')
        )
        db.session.add(config)
    else:
        # 更新配置
        config.value = data['value']
        if 'description' in data:
            config.description = data['description']
    
    db.session.commit()
    
    # 记录日志
    admin_id = get_jwt_identity()
    log = SystemLog(
        log_type='admin_action',
        admin_id=admin_id,
        action='update_system_config',
        details=f'更新系统配置: {key}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'message': '系统配置更新成功',
        'config': config.to_dict()
    }), 200