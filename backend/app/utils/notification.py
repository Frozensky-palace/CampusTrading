import smtplib
import datetime
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import requests
from flask import current_app, render_template_string
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """通知服务类"""
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化应用配置"""
        self.app = app
        
        # 邮件配置
        self.email_enabled = app.config.get('EMAIL_ENABLED', False)
        self.email_server = app.config.get('EMAIL_SERVER')
        self.email_port = app.config.get('EMAIL_PORT')
        self.email_username = app.config.get('EMAIL_USERNAME')
        self.email_password = app.config.get('EMAIL_PASSWORD')
        self.email_use_tls = app.config.get('EMAIL_USE_TLS', True)
        self.email_sender = app.config.get('EMAIL_SENDER')
        
        # SMS配置
        self.sms_enabled = app.config.get('SMS_ENABLED', False)
        self.sms_api_url = app.config.get('SMS_API_URL')
        self.sms_api_key = app.config.get('SMS_API_KEY')
        self.sms_sign = app.config.get('SMS_SIGN')
        
        # 站内信配置
        self.message_enabled = app.config.get('MESSAGE_ENABLED', True)
    
    def send_email(self, to, subject, content, is_html=False):
        """发送邮件通知"""
        if not self.email_enabled:
            logger.warning("邮件功能未启用")
            return False, "邮件功能未启用"
        
        if not self.email_server or not self.email_port:
            logger.error("邮件服务器配置不完整")
            return False, "邮件服务器配置不完整"
        
        try:
            # 创建邮件消息
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = to
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 添加邮件内容
            if is_html:
                msg.attach(MIMEText(content, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # 连接邮件服务器
            server = smtplib.SMTP(self.email_server, self.email_port)
            if self.email_use_tls:
                server.starttls()
            
            # 登录邮件服务器
            if self.email_username and self.email_password:
                server.login(self.email_username, self.email_password)
            
            # 发送邮件
            server.send_message(msg)
            server.quit()
            
            logger.info(f"邮件发送成功: {to}, 主题: {subject}")
            return True, "邮件发送成功"
        except Exception as e:
            logger.error(f"邮件发送失败: {str(e)}")
            return False, f"邮件发送失败: {str(e)}"
    
    def send_sms(self, phone, template_code, template_params=None):
        """发送短信通知"""
        if not self.sms_enabled:
            logger.warning("短信功能未启用")
            return False, "短信功能未启用"
        
        if not self.sms_api_url or not self.sms_api_key:
            logger.error("短信API配置不完整")
            return False, "短信API配置不完整"
        
        try:
            # 准备请求参数
            params = {
                'phone': phone,
                'template_code': template_code,
                'sign': self.sms_sign,
                'params': template_params or {},
                'api_key': self.sms_api_key
            }
            
            # 发送请求
            response = requests.post(self.sms_api_url, json=params, timeout=30)
            result = response.json()
            
            if result.get('success'):
                logger.info(f"短信发送成功: {phone}, 模板: {template_code}")
                return True, "短信发送成功"
            else:
                error_msg = result.get('message', '未知错误')
                logger.error(f"短信发送失败: {error_msg}")
                return False, f"短信发送失败: {error_msg}"
        except Exception as e:
            logger.error(f"短信发送异常: {str(e)}")
            return False, f"短信发送异常: {str(e)}"
    
    def send_system_message(self, user_id, title, content, message_type='system', related_id=None):
        """发送系统消息（站内信）"""
        if not self.message_enabled:
            logger.warning("站内信功能未启用")
            return False, "站内信功能未启用"
        
        try:
            from app.modules.user.models_message import Message
            from app import db
            
            # 创建消息对象
            message = Message(
                user_id=user_id,
                title=title,
                content=content,
                message_type=message_type,
                related_id=related_id,
                is_read=False,
                created_at=datetime.datetime.utcnow()
            )
            
            # 保存到数据库
            db.session.add(message)
            db.session.commit()
            
            logger.info(f"站内信发送成功: 用户ID={user_id}, 标题={title}")
            return True, "站内信发送成功"
        except Exception as e:
            logger.error(f"站内信发送失败: {str(e)}")
            if 'db' in locals() and db.session.is_active:
                db.session.rollback()
            return False, f"站内信发送失败: {str(e)}"
    
    def send_notification(self, user, notification_type, data, channels=None):
        """发送通知（支持多渠道）"""
        # 默认为所有启用的渠道
        if not channels:
            channels = []
            if self.email_enabled and hasattr(user, 'email') and user.email:
                channels.append('email')
            if self.sms_enabled and hasattr(user, 'phone') and user.phone:
                channels.append('sms')
            if self.message_enabled:
                channels.append('message')
        
        results = {}
        
        # 根据通知类型获取模板
        template = self._get_notification_template(notification_type)
        if not template:
            logger.error(f"未找到通知模板: {notification_type}")
            return False, "未找到通知模板"
        
        # 处理邮件通知
        if 'email' in channels and hasattr(user, 'email') and user.email:
            email_subject = self._render_template(template.get('email_subject'), data)
            email_content = self._render_template(template.get('email_content'), data)
            email_is_html = template.get('email_is_html', False)
            
            success, msg = self.send_email(
                user.email,
                email_subject,
                email_content,
                email_is_html
            )
            results['email'] = {'success': success, 'message': msg}
        
        # 处理短信通知
        if 'sms' in channels and hasattr(user, 'phone') and user.phone:
            sms_template_code = template.get('sms_template_code')
            sms_params = self._prepare_sms_params(template.get('sms_params'), data)
            
            success, msg = self.send_sms(
                user.phone,
                sms_template_code,
                sms_params
            )
            results['sms'] = {'success': success, 'message': msg}
        
        # 处理站内信通知
        if 'message' in channels:
            message_title = self._render_template(template.get('message_title'), data)
            message_content = self._render_template(template.get('message_content'), data)
            message_type = template.get('message_type', 'system')
            related_id = data.get('related_id')
            
            success, msg = self.send_system_message(
                user.id,
                message_title,
                message_content,
                message_type,
                related_id
            )
            results['message'] = {'success': success, 'message': msg}
        
        # 检查是否有至少一个渠道发送成功
        has_success = any(result['success'] for result in results.values())
        
        return has_success, results
    
    def _get_notification_template(self, notification_type):
        """获取通知模板"""
        # 这里可以从数据库或配置中获取模板
        # 为简单起见，这里直接返回预定义的模板
        templates = {
            'user_register': {
                'email_subject': '欢迎注册校园交易平台',
                'email_content': '尊敬的 {{username}}，\n\n欢迎注册校园交易平台！您的账号已成功创建，\n请点击以下链接完成邮箱验证：{{verification_link}}\n\n祝您使用愉快！',
                'email_is_html': False,
                'sms_template_code': 'SMS_REGISTER',
                'sms_params': {'username': '{{username}}', 'code': '{{verification_code}}'},
                'message_title': '账号注册成功',
                'message_content': '尊敬的 {{username}}，\n\n您的账号已成功注册，感谢您加入校园交易平台！',
                'message_type': 'system'
            },
            'order_created': {
                'email_subject': '您有新的订单',
                'email_content': '尊敬的 {{username}}，\n\n您有一个新的订单 #{{order_id}}，\n商品：{{item_name}}\n金额：￥{{amount}}\n\n请及时处理。',
                'email_is_html': False,
                'sms_template_code': 'SMS_ORDER_CREATED',
                'sms_params': {'order_id': '{{order_id}}', 'item_name': '{{item_name}}'},
                'message_title': '新订单通知',
                'message_content': '您有一个新的订单 #{{order_id}}，请及时处理。',
                'message_type': 'order'
            },
            'order_updated': {
                'email_subject': '订单状态更新',
                'email_content': '尊敬的 {{username}}，\n\n您的订单 #{{order_id}} 状态已更新为 {{status}}。\n\n感谢您的支持！',
                'email_is_html': False,
                'sms_template_code': 'SMS_ORDER_UPDATED',
                'sms_params': {'order_id': '{{order_id}}', 'status': '{{status}}'},
                'message_title': '订单状态更新',
                'message_content': '您的订单 #{{order_id}} 状态已更新为 {{status}}。',
                'message_type': 'order'
            },
            'password_reset': {
                'email_subject': '密码重置',
                'email_content': '尊敬的 {{username}}，\n\n您请求重置密码，\n请点击以下链接重置密码：{{reset_link}}\n\n如非本人操作，请忽略此邮件。',
                'email_is_html': False,
                'sms_template_code': 'SMS_PASSWORD_RESET',
                'sms_params': {'code': '{{reset_code}}'},
                'message_title': '密码重置请求',
                'message_content': '您请求重置密码，请使用验证码 {{reset_code}} 进行操作。',
                'message_type': 'account'
            }
        }
        
        return templates.get(notification_type)
    
    def _render_template(self, template_str, data):
        """渲染模板内容"""
        if not template_str:
            return ''
        
        try:
            return render_template_string(template_str, **data)
        except Exception as e:
            logger.error(f"模板渲染失败: {str(e)}")
            return template_str
    
    def _prepare_sms_params(self, param_template, data):
        """准备短信参数"""
        if not param_template:
            return {}
        
        params = {}
        for key, value_template in param_template.items():
            params[key] = self._render_template(value_template, data)
        
        return params


# 常用通知快捷函数

def notify_user_register(user, verification_link=None, verification_code=None):
    """通知用户注册"""
    notification_service = NotificationService(current_app)
    return notification_service.send_notification(
        user,
        'user_register',
        {
            'username': getattr(user, 'username', ''),
            'verification_link': verification_link,
            'verification_code': verification_code
        }
    )


def notify_order_created(user, order):
    """通知订单创建"""
    notification_service = NotificationService(current_app)
    return notification_service.send_notification(
        user,
        'order_created',
        {
            'username': getattr(user, 'username', ''),
            'order_id': order.id,
            'item_name': getattr(order, 'item_name', ''),
            'amount': getattr(order, 'amount', 0),
            'related_id': order.id
        }
    )


def notify_order_updated(user, order, status):
    """通知订单更新"""
    notification_service = NotificationService(current_app)
    return notification_service.send_notification(
        user,
        'order_updated',
        {
            'username': getattr(user, 'username', ''),
            'order_id': order.id,
            'status': status,
            'related_id': order.id
        }
    )


def notify_password_reset(user, reset_link=None, reset_code=None):
    """通知密码重置"""
    notification_service = NotificationService(current_app)
    return notification_service.send_notification(
        user,
        'password_reset',
        {
            'username': getattr(user, 'username', ''),
            'reset_link': reset_link,
            'reset_code': reset_code
        }
    )


def notify_admin_new_complaint(complaint):
    """通知管理员有新投诉"""
    # 这里可以实现通知管理员的逻辑
    # 例如：发送邮件给所有管理员或发送站内信
    try:
        from app.modules.admin.models import AdminUser
        from app import db
        
        # 获取所有管理员
        admins = AdminUser.query.filter_by(is_active=True).all()
        
        for admin in admins:
            # 发送站内信通知
            NotificationService(current_app).send_system_message(
                admin.id,
                '新投诉通知',
                f'您有一个新的投诉需要处理，投诉ID：{complaint.id}，\n投诉内容：{complaint.content[:100]}...',
                'complaint',
                complaint.id
            )
        
        return True, f"已通知 {len(admins)} 位管理员"
    except Exception as e:
        logger.error(f"通知管理员失败: {str(e)}")
        return False, f"通知管理员失败: {str(e)}"


def notify_price_change(user, item, old_price, new_price):
    """通知价格变动"""
    notification_service = NotificationService(current_app)
    
    # 构建通知数据
    data = {
        'username': getattr(user, 'username', ''),
        'item_name': getattr(item, 'name', ''),
        'old_price': old_price,
        'new_price': new_price,
        'price_diff': new_price - old_price,
        'item_id': item.id,
        'related_id': item.id
    }
    
    # 发送通知
    return notification_service.send_notification(
        user,
        'price_change',  # 这里需要在templates中定义price_change模板
        data
    )


def send_batch_notifications(users, notification_type, data_template):
    """批量发送通知"""
    results = []
    notification_service = NotificationService(current_app)
    
    for user in users:
        # 为每个用户准备数据
        user_data = {}
        for key, value in data_template.items():
            if callable(value):
                # 如果是可调用对象，传入user执行
                user_data[key] = value(user)
            else:
                user_data[key] = value
        
        # 发送通知
        success, msg = notification_service.send_notification(
            user,
            notification_type,
            user_data
        )
        
        results.append({
            'user_id': user.id,
            'success': success,
            'message': msg
        })
    
    # 统计结果
    success_count = sum(1 for r in results if r['success'])
    
    return {
        'total': len(results),
        'success': success_count,
        'failure': len(results) - success_count,
        'details': results
    }


def format_notification_content(template, **kwargs):
    """格式化通知内容"""
    try:
        return template.format(**kwargs)
    except Exception as e:
        logger.error(f"格式化通知内容失败: {str(e)}")
        return template


def get_unread_count(user_id):
    """获取用户未读消息数量"""
    try:
        from app.modules.user.models import Message
        from app import db
        
        count = Message.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()
        
        return count
    except Exception as e:
        logger.error(f"获取未读消息数量失败: {str(e)}")
        return 0


def mark_as_read(message_id, user_id):
    """标记消息为已读"""
    try:
        from app.modules.user.models import Message
        from app import db
        
        message = Message.query.filter_by(
            id=message_id,
            user_id=user_id
        ).first()
        
        if message:
            message.is_read = True
            message.read_at = datetime.datetime.utcnow()
            db.session.commit()
            return True, "标记成功"
        else:
            return False, "消息不存在"
    except Exception as e:
        logger.error(f"标记消息为已读失败: {str(e)}")
        if 'db' in locals() and db.session.is_active:
            db.session.rollback()
        return False, f"标记失败: {str(e)}"


def mark_all_as_read(user_id):
    """标记所有消息为已读"""
    try:
        from app.modules.user.models_message import Message
        from app import db
        
        messages = Message.query.filter_by(
            user_id=user_id,
            is_read=False
        ).all()
        
        for message in messages:
            message.is_read = True
            message.read_at = datetime.datetime.utcnow()
        
        db.session.commit()
        return True, f"已标记 {len(messages)} 条消息为已读"
    except Exception as e:
        logger.error(f"标记所有消息为已读失败: {str(e)}")
        if 'db' in locals() and db.session.is_active:
            db.session.rollback()
        return False, f"标记失败: {str(e)}"