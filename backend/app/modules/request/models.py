from datetime import datetime
from app import db


class ItemRequest(db.Model):
    """求购信息模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    expected_price = db.Column(db.Integer, nullable=False)  # 期望价格（虚拟币）
    category_id = db.Column(db.Integer, db.ForeignKey('item_category.id'), nullable=False)
    
    # 专业和校区范围
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))  # 所需专业
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'))  # 校区范围
    
    # 状态
    status = db.Column(db.String(20), nullable=False, default='active')  # active(有效), matched(已匹配), canceled(已取消)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    request_responses = db.relationship('RequestResponse', backref='item_request', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """将求购信息对象转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'expected_price': self.expected_price,
            'category_id': self.category_id,
            'major_id': self.major_id,
            'campus_id': self.campus_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'major_name': self.major.name if self.major else None,
            'campus_name': self.campus.name if self.campus else None
        }


class RequestResponse(db.Model):
    """求购响应模型"""
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('item_request.id'), nullable=False)
    responder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offer_amount = db.Column(db.Integer, nullable=False)  # 报价金额
    message = db.Column(db.Text)  # 附加消息
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending(待买家确认), accepted(已接受), rejected(已拒绝)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)  # 回应时间
    
    # 关系
    responder = db.relationship('User', backref='request_responses')
    
    def to_dict(self):
        """将求购响应对象转换为字典"""
        return {
            'id': self.id,
            'request_id': self.request_id,
            'responder_id': self.responder_id,
            'offer_amount': self.offer_amount,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'responded_at': self.responded_at.isoformat() if self.responded_at else None
        }