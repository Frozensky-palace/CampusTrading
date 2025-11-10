from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# 创建main蓝图
main = Blueprint('main', __name__)


@main.route('/')
def index():
    """应用首页"""
    return jsonify({
        'message': '欢迎使用校园交易平台API',
        'version': '1.0.0',
        'api_endpoints': [
            '/api/user - 用户相关接口',
            '/api/item - 商品相关接口',
            '/api/transaction - 交易相关接口',
            '/api/request - 求购相关接口',
            '/api/compare - 比价相关接口',
            '/api/admin - 管理相关接口'
        ]
    })


@main.route('/ping')
def ping():
    """健康检查接口"""
    return jsonify({
        'message': 'pong',
        'timestamp': request.timestamp if hasattr(request, 'timestamp') else None
    })


@main.route('/api')
def api_docs():
    """API文档入口"""
    return jsonify({
        'message': '校园交易平台API文档',
        'version': '1.0.0',
        'modules': {
            'user': '/api/user - 用户管理',
            'item': '/api/item - 商品管理',
            'transaction': '/api/transaction - 交易管理',
            'request': '/api/request - 求购管理',
            'compare': '/api/compare - 比价管理',
            'admin': '/api/admin - 后台管理'
        },
        'swagger_ui': '/swagger-ui'  # 假设将来会添加Swagger UI
    })


@main.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    """受保护的测试接口"""
    current_user_id = get_jwt_identity()
    return jsonify({
        'message': '这是一个受保护的接口',
        'user_id': current_user_id
    })


@main.route('/api/version')
def get_version():
    """获取API版本信息"""
    return jsonify({
        'version': '1.0.0',
        'build_time': '2023-11-15',
        'features': [
            '用户认证与授权',
            '商品发布与管理',
            '在线交易与支付',
            '求购信息发布',
            '价格比较功能',
            '后台管理系统'
        ]
    })


@main.app_errorhandler(404)
def not_found(error):
    """处理404错误"""
    return jsonify({
        'error': 'Not Found',
        'message': '请求的资源不存在',
        'status_code': 404,
        'path': request.path
    }), 404


@main.app_errorhandler(400)
def bad_request(error):
    """处理400错误"""
    return jsonify({
        'error': 'Bad Request',
        'message': str(error),
        'status_code': 400
    }), 400


@main.app_errorhandler(401)
def unauthorized(error):
    """处理401错误"""
    return jsonify({
        'error': 'Unauthorized',
        'message': '未授权，请先登录',
        'status_code': 401
    }), 401


@main.app_errorhandler(403)
def forbidden(error):
    """处理403错误"""
    return jsonify({
        'error': 'Forbidden',
        'message': '权限不足，无法访问',
        'status_code': 403
    }), 403


@main.app_errorhandler(500)
def internal_server_error(error):
    """处理500错误"""
    return jsonify({
        'error': 'Internal Server Error',
        'message': '服务器内部错误，请稍后重试',
        'status_code': 500
    }), 500


@main.before_app_request
def before_request():
    """请求前处理"""
    # 可以在这里添加请求前的通用处理逻辑
    # 例如：记录请求日志、检查请求头、设置请求时间戳等
    request.timestamp = request.args.get('timestamp') or str(int(request.environ.get('REQUEST_START_TIME', 0)))


@main.after_app_request
def after_request(response):
    """请求后处理"""
    # 可以在这里添加请求后的通用处理逻辑
    # 例如：添加响应头、记录响应日志等
    # 添加CORS头
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@main.route('/api/status')
def get_status():
    """获取系统状态"""
    from app import db
    from sqlalchemy import text
    
    # 检查数据库连接
    try:
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
    except Exception:
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'running',
        'database': db_status,
        'uptime': 'unknown',  # 可以添加实际的运行时间
        'memory_usage': 'unknown',  # 可以添加实际的内存使用情况
        'cpu_usage': 'unknown'  # 可以添加实际的CPU使用情况
    })


@main.route('/api/constants')
def get_constants():
    """获取系统常量"""
    return jsonify({
        'max_file_size': 5 * 1024 * 1024,  # 5MB
        'max_images_per_item': 9,
        'default_page_size': 10,
        'max_page_size': 100,
        'jwt_expiration_hours': 24,
        'cache_ttl_seconds': 3600
    })