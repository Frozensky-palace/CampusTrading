from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db
from app.modules.user.models import User, School, Campus, Major, CoinLog, Collection

# 创建蓝图
user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    # 检查用户是否已存在
    if User.query.filter_by(student_id=data['student_id']).first():
        return jsonify({'message': '该学号已注册'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': '该邮箱已注册'}), 400
    
    # 创建新用户
    user = User(
        student_id=data['student_id'],
        email=data['email'],
        username=data['username'],
        password=data['password']
    )
    
    # 设置校园币初始值
    from config.development import DevelopmentConfig
    user.coins = DevelopmentConfig.INITIAL_COINS
    
    # 先添加用户到数据库，获取用户ID
    db.session.add(user)
    db.session.flush()  # 刷新数据库会话以获取用户ID
    
    # 然后记录校园币变动日志
    coin_log = CoinLog(
        user_id=user.id,
        amount=user.coins,
        type='register_reward',
        description='注册奖励'
    )
    
    db.session.add(coin_log)
    db.session.commit()
    
    return jsonify({'message': '注册成功'}), 201


@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    # 检查用户是否存在
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({'message': '邮箱或密码错误'}), 401
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # 创建JWT令牌
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户个人信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    return jsonify(user.to_dict()), 200


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新用户个人信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    # 更新用户信息
    if 'username' in data:
        user.username = data['username']
    if 'campus_id' in data:
        user.campus_id = data['campus_id']
    if 'major_id' in data:
        user.major_id = data['major_id']
    
    db.session.commit()
    
    return jsonify({'message': '个人信息更新成功'}), 200


@user_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify_user():
    """用户实名认证"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    # 检查是否已经实名认证
    if user.is_verified:
        return jsonify({'message': '您已完成实名认证'}), 400
    
    # 处理文件上传
    if 'id_card_photo' not in request.files:
        return jsonify({'message': '请上传学生证照片'}), 400
    
    file = request.files['id_card_photo']
    if file.filename == '':
        return jsonify({'message': '请选择照片'}), 400
    
    # 保存文件
    filename = secure_filename(file.filename)
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    
    # 更新用户认证信息
    user.id_card_photo = file_path
    user.is_verified = False  # 待管理员审核
    
    db.session.commit()
    
    return jsonify({'message': '认证信息已提交，请等待管理员审核'}), 200


@user_bp.route('/coins', methods=['GET'])
@jwt_required()
def get_coins():
    """获取用户校园币余额"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    return jsonify({'coins': user.coins}), 200


@user_bp.route('/coins/logs', methods=['GET'])
@jwt_required()
def get_coin_logs():
    """获取用户校园币变动记录"""
    user_id = get_jwt_identity()
    logs = CoinLog.query.filter_by(user_id=user_id).order_by(CoinLog.created_at.desc()).all()
    
    result = []
    for log in logs:
        result.append({
            'amount': log.amount,
            'type': log.type,
            'description': log.description,
            'created_at': log.created_at.isoformat()
        })
    
    return jsonify(result), 200


@user_bp.route('/schools', methods=['GET'])
def get_schools():
    """获取学校列表"""
    schools = School.query.all()
    
    result = []
    for school in schools:
        result.append({
            'id': school.id,
            'name': school.name,
            'province': school.province
        })
    
    return jsonify(result), 200


@user_bp.route('/campuses/<int:school_id>', methods=['GET'])
def get_campuses(school_id):
    """获取指定学校的校区列表"""
    campuses = Campus.query.filter_by(school_id=school_id).all()
    
    result = []
    for campus in campuses:
        result.append({
            'id': campus.id,
            'name': campus.name
        })
    
    return jsonify(result), 200


@user_bp.route('/majors/<int:campus_id>', methods=['GET'])
def get_majors(campus_id):
    """获取指定校区的专业列表"""
    majors = Major.query.filter_by(campus_id=campus_id).all()
    
    result = []
    for major in majors:
        result.append({
            'id': major.id,
            'name': major.name
        })
    
    return jsonify(result), 200