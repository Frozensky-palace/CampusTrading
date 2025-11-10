from sqlalchemy import func, desc, asc
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from app import db
import json
from datetime import datetime, timedelta


def db_commit():
    """提交数据库更改"""
    try:
        db.session.commit()
        return True, None
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"数据库提交失败: {str(e)}")
        return False, str(e)


def db_add(instance):
    """添加数据库实例"""
    try:
        db.session.add(instance)
        return True, None
    except SQLAlchemyError as e:
        current_app.logger.error(f"添加数据库实例失败: {str(e)}")
        return False, str(e)


def db_delete(instance):
    """删除数据库实例"""
    try:
        db.session.delete(instance)
        return True, None
    except SQLAlchemyError as e:
        current_app.logger.error(f"删除数据库实例失败: {str(e)}")
        return False, str(e)


def db_bulk_insert(model, data_list):
    """批量插入数据"""
    try:
        db.session.bulk_insert_mappings(model, data_list)
        return True, None
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"批量插入数据失败: {str(e)}")
        return False, str(e)


def get_pagination(query, page=1, per_page=10, order_by=None):
    """获取分页数据"""
    try:
        if order_by:
            query = query.order_by(order_by)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        items = pagination.items
        
        return {
            'items': items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'prev_num': pagination.prev_num,
            'next_num': pagination.next_num
        }, None
    except SQLAlchemyError as e:
        current_app.logger.error(f"获取分页数据失败: {str(e)}")
        return None, str(e)


def execute_query(query, params=None):
    """执行自定义SQL查询"""
    try:
        result = db.session.execute(query, params or {})
        return result, None
    except SQLAlchemyError as e:
        current_app.logger.error(f"执行SQL查询失败: {str(e)}")
        return None, str(e)


def get_record_by_id(model, record_id):
    """根据ID获取记录"""
    try:
        return model.query.get(record_id)
    except SQLAlchemyError as e:
        current_app.logger.error(f"根据ID获取记录失败: {str(e)}")
        return None


def get_records_by_ids(model, record_ids):
    """根据ID列表获取记录"""
    try:
        return model.query.filter(model.id.in_(record_ids)).all()
    except SQLAlchemyError as e:
        current_app.logger.error(f"根据ID列表获取记录失败: {str(e)}")
        return []


def get_first_record(model, **filters):
    """获取符合条件的第一条记录"""
    try:
        return model.query.filter_by(**filters).first()
    except SQLAlchemyError as e:
        current_app.logger.error(f"获取第一条记录失败: {str(e)}")
        return None


def get_all_records(model, **filters):
    """获取符合条件的所有记录"""
    try:
        return model.query.filter_by(**filters).all()
    except SQLAlchemyError as e:
        current_app.logger.error(f"获取所有记录失败: {str(e)}")
        return []


def count_records(model, **filters):
    """统计符合条件的记录数量"""
    try:
        return model.query.filter_by(**filters).count()
    except SQLAlchemyError as e:
        current_app.logger.error(f"统计记录数量失败: {str(e)}")
        return 0


def get_records_with_pagination(model, page=1, per_page=10, order_by=None, **filters):
    """获取符合条件的分页记录"""
    try:
        query = model.query.filter_by(**filters)
        
        if order_by:
            query = query.order_by(order_by)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': pagination.items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }, None
    except SQLAlchemyError as e:
        current_app.logger.error(f"获取分页记录失败: {str(e)}")
        return None, str(e)


def update_record(instance, **kwargs):
    """更新记录属性"""
    try:
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        return True, None
    except SQLAlchemyError as e:
        current_app.logger.error(f"更新记录失败: {str(e)}")
        return False, str(e)


def bulk_update(model, filters, update_data):
    """批量更新记录"""
    try:
        query = model.query.filter_by(**filters)
        result = query.update(update_data, synchronize_session=False)
        db.session.commit()
        return result, None  # 返回受影响的行数
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"批量更新记录失败: {str(e)}")
        return 0, str(e)


def bulk_delete(model, **filters):
    """批量删除记录"""
    try:
        query = model.query.filter_by(**filters)
        result = query.delete(synchronize_session=False)
        db.session.commit()
        return result, None  # 返回受影响的行数
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"批量删除记录失败: {str(e)}")
        return 0, str(e)


def get_date_range_query(field, start_date=None, end_date=None):
    """获取日期范围查询条件"""
    query = True
    
    if start_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d') if isinstance(start_date, str) else start_date
        query = query & (field >= start_datetime)
    
    if end_date:
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d') if isinstance(end_date, str) else end_date
        end_datetime = end_datetime + timedelta(days=1) - timedelta(seconds=1)  # 设置为当天的最后一秒
        query = query & (field <= end_datetime)
    
    return query


def get_field_stats(model, field, **filters):
    """获取字段的统计信息"""
    try:
        query = model.query.filter_by(**filters)
        
        stats = {
            'count': query.count(),
            'min': query.with_entities(func.min(field)).scalar(),
            'max': query.with_entities(func.max(field)).scalar(),
            'avg': query.with_entities(func.avg(field)).scalar(),
            'sum': query.with_entities(func.sum(field)).scalar()
        }
        
        return stats, None
    except SQLAlchemyError as e:
        current_app.logger.error(f"获取字段统计信息失败: {str(e)}")
        return None, str(e)


def get_distinct_values(model, field, **filters):
    """获取字段的唯一值列表"""
    try:
        query = model.query.filter_by(**filters)
        distinct_values = query.with_entities(field).distinct().all()
        
        # 提取元组中的值
        return [value[0] for value in distinct_values], None
    except SQLAlchemyError as e:
        current_app.logger.error(f"获取唯一值失败: {str(e)}")
        return [], str(e)


def json_serial(obj):
    """JSON序列化函数，用于处理日期时间等特殊类型"""
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def model_to_dict(instance, include_relationships=False, exclude_fields=None):
    """将模型实例转换为字典"""
    if instance is None:
        return None
    
    result = {}
    exclude_fields = exclude_fields or []
    
    # 获取所有列字段
    columns = instance.__table__.columns.keys()
    
    for column in columns:
        if column in exclude_fields:
            continue
        
        value = getattr(instance, column)
        
        # 处理日期时间类型
        if isinstance(value, datetime):
            result[column] = value.isoformat()
        else:
            result[column] = value
    
    # 包含关联关系
    if include_relationships:
        for relationship in instance.__mapper__.relationships:
            if relationship.key in exclude_fields:
                continue
            
            related_instance = getattr(instance, relationship.key)
            
            if related_instance is None:
                result[relationship.key] = None
            elif isinstance(related_instance, list):
                # 一对多或多对多关系
                result[relationship.key] = [
                    model_to_dict(item, include_relationships=False, exclude_fields=exclude_fields)
                    for item in related_instance
                ]
            else:
                # 一对一或多对一关系
                result[relationship.key] = model_to_dict(
                    related_instance, include_relationships=False, exclude_fields=exclude_fields
                )
    
    return result


def dict_to_model(model, data, instance=None):
    """将字典转换为模型实例"""
    if instance is None:
        instance = model()
    
    for key, value in data.items():
        if hasattr(instance, key):
            # 获取字段类型
            field_type = None
            for column in instance.__table__.columns:
                if column.name == key:
                    field_type = column.type.__class__.__name__
                    break
            
            # 处理日期时间类型
            if field_type in ['DateTime', 'Date'] and isinstance(value, str):
                try:
                    setattr(instance, key, datetime.fromisoformat(value))
                except ValueError:
                    # 如果格式不正确，忽略该字段
                    pass
            else:
                setattr(instance, key, value)
    
    return instance


def create_backup():"""创建数据库备份"""
    # 实际项目中需要实现数据库备份逻辑
    # 这里只是一个示例
    current_app.logger.info("创建数据库备份")
    return True, "数据库备份创建成功"