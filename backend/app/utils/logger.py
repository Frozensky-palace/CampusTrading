import logging
import os
import datetime
import traceback
from flask import request, g


def setup_logger(name, log_file=None, level=logging.INFO):
    """设置日志记录器"""
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 创建文件处理器
    if log_file:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


class RequestLogger:
    """请求日志记录器"""
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化应用"""
        # 注册请求前处理
        @app.before_request
        def before_request():
            g.start_time = datetime.datetime.now()
            g.request_id = str(id(g))[:8]
            
            # 记录请求开始
            app.logger.info(f"请求开始 [ID:{g.request_id}] - {request.method} {request.path}")
            app.logger.debug(f"请求参数 - {request.args.to_dict()}")
            if request.is_json:
                app.logger.debug(f"请求体 - {request.get_json()}")
        
        # 注册请求后处理
        @app.after_request
        def after_request(response):
            # 计算请求处理时间
            processing_time = (datetime.datetime.now() - g.start_time).total_seconds() * 1000  # 毫秒
            
            # 记录请求结束
            app.logger.info(
                f"请求结束 [ID:{g.request_id}] - {request.method} {request.path} - 状态码: {response.status_code} - 处理时间: {processing_time:.2f}ms"
            )
            
            return response
        
        # 注册错误处理
        @app.errorhandler(Exception)
        def handle_exception(e):
            # 记录异常
            app.logger.error(f"请求异常 [ID:{getattr(g, 'request_id', 'unknown')}] - {str(e)}")
            app.logger.error(traceback.format_exc())
            
            # 重新抛出异常，让Flask默认处理
            raise


def log_info(logger, message, extra=None):
    """记录信息级日志"""
    logger.info(message, extra=extra)


def log_debug(logger, message, extra=None):
    """记录调试级日志"""
    logger.debug(message, extra=extra)


def log_warning(logger, message, extra=None):
    """记录警告级日志"""
    logger.warning(message, extra=extra)


def log_error(logger, message, extra=None):
    """记录错误级日志"""
    logger.error(message, extra=extra)


def log_critical(logger, message, extra=None):
    """记录严重级日志"""
    logger.critical(message, extra=extra)


def log_exception(logger, exception, message=None):
    """记录异常日志"""
    if message:
        logger.exception(f"{message}: {str(exception)}")
    else:
        logger.exception(str(exception))


def get_request_log_data():
    """获取请求相关的日志数据"""
    if not request:
        return {}
    
    # 获取客户端IP
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr
    
    return {
        'request_id': getattr(g, 'request_id', 'unknown'),
        'method': request.method,
        'path': request.path,
        'ip': ip,
        'user_agent': request.headers.get('User-Agent'),
        'referer': request.headers.get('Referer'),
        'params': dict(request.args),
        'data': request.get_json() if request.is_json else None
    }


def create_log_entry(log_type, action, details=None, user_id=None, admin_id=None, ip_address=None):
    """创建日志条目"""
    from app.modules.admin.models import SystemLog
    from app import db
    
    log_entry = SystemLog(
        log_type=log_type,
        user_id=user_id,
        admin_id=admin_id,
        action=action,
        details=details,
        ip_address=ip_address or (request.remote_addr if request else None),
        created_at=datetime.datetime.utcnow()
    )
    
    try:
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
    except Exception as e:
        db.session.rollback()
        # 如果保存日志失败，记录到应用日志
        if request and hasattr(request, 'app'):
            request.app.logger.error(f"保存系统日志失败: {str(e)}")
        return None


def get_log_filename(log_name):
    """获取日志文件名（包含日期）"""
    today = datetime.date.today().strftime('%Y-%m-%d')
    return f"{log_name}_{today}.log"


def get_log_directory(app=None):
    """获取日志目录"""
    if app and hasattr(app, 'config') and 'LOG_DIR' in app.config:
        log_dir = app.config['LOG_DIR']
    else:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'logs')
    
    # 确保日志目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    return log_dir


def get_full_log_path(log_name, app=None):
    """获取完整的日志文件路径"""
    log_dir = get_log_directory(app)
    log_filename = get_log_filename(log_name)
    return os.path.join(log_dir, log_filename)


def rotate_logs(log_dir, max_backups=7):
    """日志轮转（删除超过指定数量的旧日志文件）"""
    if not os.path.exists(log_dir):
        return
    
    # 获取所有日志文件并按修改时间排序
    log_files = []
    for filename in os.listdir(log_dir):
        if filename.endswith('.log'):
            file_path = os.path.join(log_dir, filename)
            if os.path.isfile(file_path):
                log_files.append((file_path, os.path.getmtime(file_path)))
    
    # 按修改时间排序（最新的在前）
    log_files.sort(key=lambda x: x[1], reverse=True)
    
    # 删除超过最大备份数量的旧日志文件
    for i in range(max_backups, len(log_files)):
        try:
            os.remove(log_files[i][0])
        except Exception as e:
            # 记录删除失败的日志
            print(f"删除旧日志文件失败: {log_files[i][0]}, 错误: {str(e)}")


def log_user_activity(user_id, action, details=None):
    """记录用户活动日志"""
    return create_log_entry(
        log_type='user_action',
        action=action,
        details=details,
        user_id=user_id
    )


def log_admin_activity(admin_id, action, details=None):
    """记录管理员活动日志"""
    return create_log_entry(
        log_type='admin_action',
        action=action,
        details=details,
        admin_id=admin_id
    )


def log_system_event(action, details=None):
    """记录系统事件日志"""
    return create_log_entry(
        log_type='system_event',
        action=action,
        details=details
    )


def log_error_event(error_type, details=None):
    """记录错误事件日志"""
    return create_log_entry(
        log_type='error',
        action=error_type,
        details=details
    )


def setup_application_logger(app):
    """设置应用日志记录器"""
    # 配置应用日志级别
    log_level = app.config.get('LOG_LEVEL', 'INFO').upper()
    app.logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # 清除默认处理器
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
    
    # 创建文件处理器
    if app.config.get('LOG_TO_FILE', False):
        log_dir = get_log_directory(app)
        log_file = os.path.join(log_dir, 'app.log')
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        
        # 设置日志轮转
        rotate_logs(log_dir, app.config.get('LOG_MAX_BACKUPS', 7))
    
    return app.logger