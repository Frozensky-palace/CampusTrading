from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class AdminUser(db.Model, UserMixin):
    """管理员用户模型"""
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(40), default='admin')  # admin, super_admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # 验证密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ItemReview(db.Model):
    """商品审核模型"""
    __tablename__ = 'item_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    
    # 关系
    item = db.relationship('Item', backref=db.backref('review', uselist=False))
    admin = db.relationship('AdminUser', backref='reviews')
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'admin_id': self.admin_id,
            'status': self.status,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'item': {
                'id': self.item.id,
                'title': self.item.title,
                'user_id': self.item.user_id
            } if self.item else None
        }


class Complaint(db.Model):
    """投诉模型"""
    __tablename__ = 'complaints'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_type = db.Column(db.String(20), nullable=False)  # user, item, transaction
    target_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, processing, resolved, rejected
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    admin_comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='complaints')
    admin = db.relationship('AdminUser', backref='handled_complaints')
    
    def to_dict(self):
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'content': self.content,
            'status': self.status,
            'admin_id': self.admin_id,
            'admin_comment': self.admin_comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # 根据目标类型获取相关信息（仅用于展示）
        from app.modules.user.models import User as UserModel
        from app.modules.item.models import Item
        from app.modules.transaction.models import Transaction
        
        if self.target_type == 'user':
            target = UserModel.query.get(self.target_id)
            if target:
                result['target_info'] = {
                    'id': target.id,
                    'username': target.username
                }
        elif self.target_type == 'item':
            target = Item.query.get(self.target_id)
            if target:
                result['target_info'] = {
                    'id': target.id,
                    'title': target.title
                }
        elif self.target_type == 'transaction':
            target = Transaction.query.get(self.target_id)
            if target:
                result['target_info'] = {
                    'id': target.id,
                    'item_id': target.item_id,
                    'buyer_id': target.buyer_id,
                    'seller_id': target.seller_id
                }
        
        return result


class School(db.Model):
    """学校模型"""
    __tablename__ = 'schools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    campuses = db.relationship('Campus', backref='school', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'province': self.province,
            'city': self.city,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Campus(db.Model):
    """校区模型"""
    __tablename__ = 'campuses'
    
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'school_id': self.school_id,
            'school_name': self.school.name if self.school else None,
            'name': self.name,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Major(db.Model):
    """专业模型"""
    __tablename__ = 'majors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    school = db.relationship('School', backref='majors')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'school_id': self.school_id,
            'school_name': self.school.name if self.school else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ItemCategory(db.Model):
    """商品分类模型"""
    __tablename__ = 'item_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('item_categories.id'))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    parent = db.relationship('ItemCategory', remote_side=[id], backref='children')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'parent_name': self.parent.name if self.parent else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class SystemLog(db.Model):
    """系统日志模型"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    log_type = db.Column(db.String(50), nullable=False)  # admin_action, user_action, system_event, error
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='logs')
    admin = db.relationship('AdminUser', backref='logs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'log_type': self.log_type,
            'user_id': self.user_id,
            'admin_id': self.admin_id,
            'action': self.action,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SystemConfig(db.Model):
    """系统配置模型"""
    __tablename__ = 'system_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }