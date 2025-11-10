from datetime import datetime
from app import db


class PriceCompare(db.Model):
    """比价记录模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    original_link = db.Column(db.String(500), nullable=False)
    
    # 比价结果
    online_price = db.Column(db.Integer)  # 线上价格（虚拟币换算后的价格）
    platform_name = db.Column(db.String(100))  # 平台名称
    product_title = db.Column(db.String(255))  # 商品标题
    product_image = db.Column(db.String(500))  # 商品图片
    compare_status = db.Column(db.String(20), nullable=False, default='pending')  # pending(待比价), completed(已完成), failed(失败)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    compared_at = db.Column(db.DateTime)  # 比价完成时间
    
    # 关系
    user = db.relationship('User', backref='price_compares')
    item = db.relationship('Item', backref='price_compares')
    
    def to_dict(self):
        """将比价记录对象转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'original_link': self.original_link,
            'online_price': self.online_price,
            'platform_name': self.platform_name,
            'product_title': self.product_title,
            'product_image': self.product_image,
            'compare_status': self.compare_status,
            'created_at': self.created_at.isoformat(),
            'compared_at': self.compared_at.isoformat() if self.compared_at else None
        }


class CompareTask(db.Model):
    """比价任务模型"""
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending(待处理), processing(处理中), completed(已完成), failed(失败)
    priority = db.Column(db.Integer, default=0)  # 优先级，数字越小优先级越高
    
    # 任务结果
    result = db.Column(db.JSON)  # 存储比价结果的JSON数据
    error_message = db.Column(db.Text)  # 错误信息
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)  # 开始处理时间
    completed_at = db.Column(db.DateTime)  # 完成处理时间
    
    def to_dict(self):
        """将比价任务对象转换为字典"""
        return {
            'id': self.id,
            'link': self.link,
            'status': self.status,
            'priority': self.priority,
            'result': self.result,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }