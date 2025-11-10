from datetime import datetime
from app import db


class ItemCategory(db.Model):
    """商品分类模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('item_category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 自引用关系
    children = db.relationship('ItemCategory', backref=db.backref('parent', remote_side=[id]))
    items = db.relationship('Item', backref='category', lazy=True)


class Item(db.Model):
    """商品模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)  # 虚拟币价格
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending(待审核), active(上架中), sold(已售出), rented(已出租), removed(已下架)
    
    # 校园属性
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('item_category.id'), nullable=False)
    
    # 商品信息
    condition = db.Column(db.String(20))  # 成色：全新、九成新、八成新等
    usage_years = db.Column(db.Float)  # 使用年限
    is_bargainable = db.Column(db.Boolean, default=False)  # 是否支持砍价
    original_link = db.Column(db.String(500))  # 原商品链接
    
    # 交易类型
    transaction_type = db.Column(db.String(20), nullable=False)  # sale(出售), rent(出租)
    rental_price_day = db.Column(db.Integer)  # 日租金
    rental_price_week = db.Column(db.Integer)  # 周租金
    rental_price_month = db.Column(db.Integer)  # 月租金
    deposit = db.Column(db.Integer)  # 押金
    max_rental_days = db.Column(db.Integer)  # 最长租赁天数
    
    # 定位信息
    location_enabled = db.Column(db.Boolean, default=False)  # 是否允许定位
    location_description = db.Column(db.String(255))  # 位置描述：如XX校区附近
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)  # 审核时间
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # 审核人
    
    # 关系
    item_images = db.relationship('ItemImage', backref='item', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='item', lazy=True)
    offers = db.relationship('Offer', backref='item', lazy=True)
    
    def to_dict(self):
        """将商品对象转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'status': self.status,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'condition': self.condition,
            'usage_years': self.usage_years,
            'is_bargainable': self.is_bargainable,
            'original_link': self.original_link,
            'transaction_type': self.transaction_type,
            'rental_price_day': self.rental_price_day,
            'rental_price_week': self.rental_price_week,
            'rental_price_month': self.rental_price_month,
            'deposit': self.deposit,
            'max_rental_days': self.max_rental_days,
            'location_enabled': self.location_enabled,
            'location_description': self.location_description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'images': [img.url for img in self.item_images]
        }


class ItemImage(db.Model):
    """商品图片模型"""
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """将图片对象转换为字典"""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'url': self.url,
            'created_at': self.created_at.isoformat()
        }