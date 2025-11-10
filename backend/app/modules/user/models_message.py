from datetime import datetime
from app import db


class Message(db.Model):
    """用户消息模型"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50), default='system')
    related_id = db.Column(db.Integer, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # 关系
    user = db.relationship('User', backref=db.backref('messages', lazy=True))
    
    def __repr__(self):
        return f'<Message {self.id}: {self.title}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'message_type': self.message_type,
            'related_id': self.related_id,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    @classmethod
    def create(cls, user_id, title, content, message_type='system', related_id=None):
        """创建新消息"""
        message = cls(
            user_id=user_id,
            title=title,
            content=content,
            message_type=message_type,
            related_id=related_id,
            is_read=False,
            created_at=datetime.utcnow()
        )
        db.session.add(message)
        db.session.commit()
        return message
    
    def mark_as_read(self):
        """标记为已读"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    def update(self, title=None, content=None, message_type=None):
        """更新消息"""
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if message_type is not None:
            self.message_type = message_type
        db.session.commit()
        return self
    
    @classmethod
    def get_unread_count(cls, user_id):
        """获取用户未读消息数量"""
        return cls.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()
    
    @classmethod
    def get_by_user(cls, user_id, page=1, per_page=10, is_read=None, message_type=None):
        """获取用户的消息列表"""
        query = cls.query.filter_by(user_id=user_id)
        
        if is_read is not None:
            query = query.filter_by(is_read=is_read)
        
        if message_type:
            query = query.filter_by(message_type=message_type)
        
        # 按创建时间倒序排列（最新的在前）
        query = query.order_by(cls.created_at.desc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': [message.to_dict() for message in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    
    @classmethod
    def mark_all_as_read(cls, user_id):
        """将用户的所有消息标记为已读"""
        messages = cls.query.filter_by(
            user_id=user_id,
            is_read=False
        ).all()
        
        for message in messages:
            message.is_read = True
            message.read_at = datetime.utcnow()
        
        db.session.commit()
        return len(messages)
    
    @classmethod
    def delete_old_messages(cls, user_id, days=30):
        """删除用户的旧消息"""
        cutoff_date = datetime.utcnow() - datetime.timedelta(days=days)
        
        messages = cls.query.filter(
            cls.user_id == user_id,
            cls.created_at < cutoff_date
        ).all()
        
        count = len(messages)
        for message in messages:
            db.session.delete(message)
        
        db.session.commit()
        return count
    
    @classmethod
    def get_message_types(cls, user_id):
        """获取用户的消息类型列表"""
        result = db.session.query(cls.message_type).filter_by(
            user_id=user_id
        ).distinct().all()
        
        return [row[0] for row in result]
    
    @classmethod
    def count_by_type(cls, user_id):
        """按类型统计用户的消息数量"""
        result = db.session.query(
            cls.message_type,
            db.func.count(cls.id)
        ).filter_by(
            user_id=user_id
        ).group_by(cls.message_type).all()
        
        return {row[0]: row[1] for row in result}


# 常用的消息类型常量
MESSAGE_TYPE_SYSTEM = 'system'        # 系统消息
MESSAGE_TYPE_ORDER = 'order'          # 订单消息
MESSAGE_TYPE_PAYMENT = 'payment'      # 支付消息
MESSAGE_TYPE_COMMENT = 'comment'      # 评论消息
MESSAGE_TYPE_FOLLOW = 'follow'        # 关注消息
MESSAGE_TYPE_ACTIVITY = 'activity'    # 活动消息
MESSAGE_TYPE_COUPON = 'coupon'        # 优惠券消息
MESSAGE_TYPE_REMINDER = 'reminder'    # 提醒消息
MESSAGE_TYPE_COMPLAINT = 'complaint'  # 投诉消息
MESSAGE_TYPE_REPORT = 'report'        # 报告消息
MESSAGE_TYPE_OTHER = 'other'          # 其他消息


class MessageSetting(db.Model):
    """用户消息设置模型"""
    __tablename__ = 'message_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    email_notification = db.Column(db.Boolean, default=True)
    sms_notification = db.Column(db.Boolean, default=False)
    app_notification = db.Column(db.Boolean, default=True)
    push_notification = db.Column(db.Boolean, default=True)
    email_frequency = db.Column(db.String(20), default='immediate')  # immediate, daily, weekly
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref=db.backref('message_setting', uselist=False))
    
    def __repr__(self):
        return f'<MessageSetting {self.user_id}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'user_id': self.user_id,
            'email_notification': self.email_notification,
            'sms_notification': self.sms_notification,
            'app_notification': self.app_notification,
            'push_notification': self.push_notification,
            'email_frequency': self.email_frequency,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_or_create(cls, user_id):
        """获取或创建用户的消息设置"""
        setting = cls.query.filter_by(user_id=user_id).first()
        if not setting:
            setting = cls(user_id=user_id)
            db.session.add(setting)
            db.session.commit()
        return setting
    
    def update(self, **kwargs):
        """更新消息设置"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self


class NotificationChannel(db.Model):
    """通知渠道设置模型"""
    __tablename__ = 'notification_channels'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_type = db.Column(db.String(50), nullable=False)
    email_enabled = db.Column(db.Boolean, default=True)
    sms_enabled = db.Column(db.Boolean, default=False)
    app_enabled = db.Column(db.Boolean, default=True)
    push_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 复合唯一索引
    __table_args__ = (db.UniqueConstraint('user_id', 'message_type'),)
    
    # 关系
    user = db.relationship('User', backref=db.backref('notification_channels', lazy=True))
    
    def __repr__(self):
        return f'<NotificationChannel {self.user_id}: {self.message_type}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message_type': self.message_type,
            'email_enabled': self.email_enabled,
            'sms_enabled': self.sms_enabled,
            'app_enabled': self.app_enabled,
            'push_enabled': self.push_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_by_user_and_type(cls, user_id, message_type):
        """获取用户特定类型的通知渠道设置"""
        return cls.query.filter_by(
            user_id=user_id,
            message_type=message_type
        ).first()
    
    @classmethod
    def get_all_by_user(cls, user_id):
        """获取用户的所有通知渠道设置"""
        channels = cls.query.filter_by(user_id=user_id).all()
        return {channel.message_type: channel.to_dict() for channel in channels}
    
    @classmethod
    def set_channel(cls, user_id, message_type, **kwargs):
        """设置用户的通知渠道"""
        channel = cls.get_by_user_and_type(user_id, message_type)
        if not channel:
            channel = cls(user_id=user_id, message_type=message_type)
            db.session.add(channel)
        
        for key, value in kwargs.items():
            if hasattr(channel, key):
                setattr(channel, key, value)
        
        db.session.commit()
        return channel