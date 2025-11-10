from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class School(db.Model):
    """学校模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    province = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    campuses = db.relationship('Campus', backref='school', lazy=True)


class Campus(db.Model):
    """校区模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    users = db.relationship('User', backref='campus', lazy=True)
    majors = db.relationship('Major', backref='campus', lazy=True)


class Major(db.Model):
    """专业模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    users = db.relationship('User', backref='major', lazy=True)


class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)  # 是否实名认证
    id_card_photo = db.Column(db.String(255))  # 学生证照片路径
    
    # 校园信息
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'))
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))
    
    # 虚拟币
    coins = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # 关系
    items = db.relationship('Item', backref='user', lazy=True)
    purchases = db.relationship('Transaction', foreign_keys='Transaction.buyer_id', backref='buyer', lazy=True)
    sales = db.relationship('Transaction', foreign_keys='Transaction.seller_id', backref='seller', lazy=True)
    requests = db.relationship('ItemRequest', backref='user', lazy=True)
    offers_made = db.relationship('Offer', backref='buyer', lazy=True)
    collections = db.relationship('Collection', backref='user', lazy=True)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """将用户对象转换为字典"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'email': self.email,
            'username': self.username,
            'is_admin': self.is_admin,
            'is_verified': self.is_verified,
            'coins': self.coins,
            'campus': self.campus.name if self.campus else None,
            'major': self.major.name if self.major else None,
            'created_at': self.created_at.isoformat()
        }


class CoinLog(db.Model):
    """校园币变动记录"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)  # 变动数量，正数为增加，负数为减少
    type = db.Column(db.String(50), nullable=False)  # 类型：注册奖励、交易、评价奖励等
    related_id = db.Column(db.Integer)  # 关联的交易ID或其他ID
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='coin_logs')


class Collection(db.Model):
    """用户收藏模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    item = db.relationship('Item', backref='collections')
    
    # 联合唯一约束
    __table_args__ = (db.UniqueConstraint('user_id', 'item_id', name='_user_item_uc'),)