from datetime import datetime
from app import db


class Transaction(db.Model):
    """交易模型"""
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)  # 交易金额（虚拟币）
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending(待付款), paid(已付款), completed(已完成), canceled(已取消), disputed(纠纷中)
    transaction_type = db.Column(db.String(20), nullable=False)  # sale(出售), rent(出租)
    
    # 租赁相关字段
    rental_days = db.Column(db.Integer)  # 租赁天数
    start_date = db.Column(db.DateTime)  # 租赁开始日期
    end_date = db.Column(db.DateTime)  # 租赁结束日期
    deposit_paid = db.Column(db.Integer)  # 已付押金
    
    # 交易流程时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)  # 付款时间
    completed_at = db.Column(db.DateTime)  # 完成时间
    canceled_at = db.Column(db.DateTime)  # 取消时间
    
    # 资金托管信息
    is_escrowed = db.Column(db.Boolean, default=False)  # 是否已托管
    escrow_released_at = db.Column(db.DateTime)  # 托管资金释放时间
    
    # 交易地点信息
    meeting_location = db.Column(db.String(255))  # 见面交易地点
    
    # 评价信息
    buyer_rating = db.Column(db.Integer)  # 买家评分
    buyer_comment = db.Column(db.Text)  # 买家评价
    seller_rating = db.Column(db.Integer)  # 卖家评分
    seller_comment = db.Column(db.Text)  # 卖家评价
    
    # 关系
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='purchases')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='sales')
    
    def to_dict(self):
        """将交易对象转换为字典"""
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'item_id': self.item_id,
            'amount': self.amount,
            'status': self.status,
            'transaction_type': self.transaction_type,
            'rental_days': self.rental_days,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'deposit_paid': self.deposit_paid,
            'created_at': self.created_at.isoformat(),
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'canceled_at': self.canceled_at.isoformat() if self.canceled_at else None,
            'meeting_location': self.meeting_location,
            'buyer_rating': self.buyer_rating,
            'seller_rating': self.seller_rating
        }


class Offer(db.Model):
    """还价模型"""
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    offer_amount = db.Column(db.Integer, nullable=False)  # 还价金额
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending(待回应), accepted(已接受), rejected(已拒绝)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)  # 回应时间
    
    # 关系
    buyer = db.relationship('User', backref='offers_made')
    
    def to_dict(self):
        """将还价对象转换为字典"""
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'item_id': self.item_id,
            'offer_amount': self.offer_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'responded_at': self.responded_at.isoformat() if self.responded_at else None
        }


class Complaint(db.Model):
    """投诉模型"""
    id = db.Column(db.Integer, primary_key=True)
    complainant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    defendant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)  # 投诉原因
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending(待处理), processed(已处理), resolved(已解决)
    admin_comment = db.Column(db.Text)  # 管理员处理意见
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)  # 处理时间
    
    # 关系
    complainant = db.relationship('User', foreign_keys=[complainant_id])
    defendant = db.relationship('User', foreign_keys=[defendant_id])
    transaction = db.relationship('Transaction', backref='complaints')