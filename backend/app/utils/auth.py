import re
import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.modules.user.models import User
from app.modules.admin.models import AdminUser


def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """验证手机号格式"""
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None


def validate_password_strength(password):
    """验证密码强度（至少8位，包含字母和数字）"""
    if len(password) < 8:
        return False, "密码长度至少为8位"
    if not re.search(r'[a-zA-Z]', password):
        return False, "密码必须包含字母"
    if not re.search(r'\d', password):
        return False, "密码必须包含数字"
    return True, "密码强度符合要求"


def create_jwt_token(user_id, user_type='user', expires_delta=None):
    """创建JWT令牌"""
    if expires_delta is None:
        expires_delta = timedelta(hours=24)
    
    now = datetime.utcnow()
    expire = now + expires_delta
    
    payload = {
        'exp': expire,
        'iat': now,
        'sub': user_id,
        'user_type': user_type
    }
    
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token


def decode_jwt_token(token):
    """解码JWT令牌"""
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "令牌已过期"
    except jwt.InvalidTokenError:
        return None, "无效的令牌"
    except Exception as e:
        return None, str(e)


def verify_token(token):
    """验证JWT令牌"""
    payload, error = decode_jwt_token(token)
    if error:
        return None, error
    
    user_id = payload.get('sub')
    user_type = payload.get('user_type', 'user')
    
    # 根据用户类型获取用户
    if user_type == 'admin':
        user = AdminUser.query.get(user_id)
    else:
        user = User.query.get(user_id)
    
    if not user:
        return None, "用户不存在"
    
    return {
        'user_id': user_id,
        'user_type': user_type,
        'user': user
    }, None


def generate_token(user_id, user_type='user'):
    """生成访问令牌和刷新令牌"""
    # 创建访问令牌（有效期24小时）
    access_token = create_jwt_token(user_id, user_type, timedelta(hours=24))
    
    # 创建刷新令牌（有效期7天）
    refresh_token = create_jwt_token(user_id, user_type, timedelta(days=7))
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'expires_in': 86400  # 24小时（秒）
    }


def get_current_user():
    """获取当前登录用户"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, "未提供认证信息"
    
    try:
        token_type, token = auth_header.split(' ')
        if token_type.lower() != 'bearer':
            return None, "无效的认证类型"
    except ValueError:
        return None, "无效的认证格式"
    
    return verify_token(token)


def login_required(f):
    """用户登录装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_info, error = get_current_user()
        if error:
            return jsonify({'message': error}), 401
        
        # 检查用户类型是否为普通用户
        if user_info['user_type'] != 'user':
            return jsonify({'message': '需要用户权限'}), 403
        
        # 将用户信息添加到请求对象中
        request.current_user = user_info['user']
        request.user_info = user_info
        
        return f(*args, **kwargs)
    return decorated_function


def admin_login_required(f):
    """管理员登录装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_info, error = get_current_user()
        if error:
            return jsonify({'message': error}), 401
        
        # 检查用户类型是否为管理员
        if user_info['user_type'] != 'admin':
            return jsonify({'message': '需要管理员权限'}), 403
        
        # 将管理员信息添加到请求对象中
        request.current_admin = user_info['user']
        request.user_info = user_info
        
        return f(*args, **kwargs)
    return decorated_function


def hash_password(password):
    """对密码进行哈希处理"""
    return generate_password_hash(password)


def verify_password(hashed_password, password):
    """验证密码"""
    return check_password_hash(hashed_password, password)


def generate_verification_code(length=6):
    """生成验证码"""
    import random
    import string
    return ''.join(random.choices(string.digits, k=length))


def send_verification_email(email, code):
    """发送验证邮件（示例实现）"""
    # 实际项目中需要配置邮件服务器并发送真实邮件
    print(f"发送验证码 {code} 到邮箱 {email}")
    return True


def send_verification_sms(phone, code):
    """发送验证短信（示例实现）"""
    # 实际项目中需要接入短信服务API
    print(f"发送验证码 {code} 到手机号 {phone}")
    return True


def record_login_history(user_id, ip_address, user_agent):
    """记录登录历史"""
    from app.modules.user.models import LoginHistory
    
    login_history = LoginHistory(
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        login_time=datetime.utcnow()
    )
    
    db.session.add(login_history)
    db.session.commit()


def get_client_ip():
    """获取客户端IP地址"""
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip