from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.modules.compare.models import PriceCompare, CompareTask
from app.modules.item.models import Item
from app.modules.user.models import User
import threading
import time
import requests
from bs4 import BeautifulSoup
import re

# 创建蓝图
compare_bp = Blueprint('compare', __name__)


@compare_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_compare_task():
    """创建比价任务"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 获取商品信息
    item_id = data.get('item_id')
    product_url = data.get('product_url')
    
    if not item_id and not product_url:
        return jsonify({'message': '商品ID或商品链接至少提供一个'}), 400
    
    # 如果提供了商品ID，获取商品链接
    if item_id:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'message': '商品不存在'}), 404
        if not item.original_url:
            return jsonify({'message': '该商品没有提供原始链接，无法比价'}), 400
        product_url = item.original_url
    
    # 创建比价任务
    compare_task = CompareTask(
        user_id=user_id,
        product_url=product_url,
        status='pending',
        created_at=datetime.utcnow()
    )
    
    db.session.add(compare_task)
    db.session.commit()
    
    # 启动异步比价任务
    threading.Thread(target=perform_price_comparison, args=(compare_task.id,)).start()
    
    return jsonify({
        'message': '比价任务已创建，正在进行比价',
        'task_id': compare_task.id
    }), 201


@compare_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_compare_task(task_id):
    """获取比价任务状态和结果"""
    user_id = get_jwt_identity()
    
    # 获取比价任务
    compare_task = CompareTask.query.get(task_id)
    if not compare_task:
        return jsonify({'message': '比价任务不存在'}), 404
    
    # 检查权限
    if compare_task.user_id != user_id:
        return jsonify({'message': '没有权限查看此比价任务'}), 403
    
    # 获取比价结果
    price_comparisons = PriceCompare.query.filter_by(task_id=task_id).all()
    
    # 格式化结果
    comparisons = []
    for comparison in price_comparisons:
        comparisons.append(comparison.to_dict())
    
    return jsonify({
        'task': compare_task.to_dict(),
        'comparisons': comparisons
    }), 200


@compare_bp.route('/my/tasks', methods=['GET'])
@jwt_required()
def get_my_compare_tasks():
    """获取我创建的比价任务列表"""
    user_id = get_jwt_identity()
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = CompareTask.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    # 分页
    pagination = query.order_by(CompareTask.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    tasks = pagination.items
    
    # 格式化结果
    result = []
    for task in tasks:
        task_dict = task.to_dict()
        # 获取最近的比价结果
        latest_comparison = PriceCompare.query.filter_by(task_id=task.id).order_by(PriceCompare.created_at.desc()).first()
        if latest_comparison:
            task_dict['latest_price'] = latest_comparison.price
            task_dict['latest_platform'] = latest_comparison.platform
        result.append(task_dict)
    
    return jsonify({
        'tasks': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


def perform_price_comparison(task_id):
    """执行比价任务（异步函数）"""
    # 获取比价任务
    compare_task = CompareTask.query.get(task_id)
    if not compare_task:
        return
    
    # 更新任务状态为进行中
    compare_task.status = 'processing'
    db.session.commit()
    
    try:
        # 执行比价
        results = crawl_product_prices(compare_task.product_url)
        
        # 保存比价结果
        for result in results:
            price_compare = PriceCompare(
                task_id=task_id,
                platform=result['platform'],
                price=result['price'],
                url=result['url'],
                created_at=datetime.utcnow()
            )
            db.session.add(price_compare)
        
        # 更新任务状态为完成
        compare_task.status = 'completed'
        compare_task.completed_at = datetime.utcnow()
        
    except Exception as e:
        # 更新任务状态为失败
        compare_task.status = 'failed'
        compare_task.error_message = str(e)
        
    finally:
        db.session.commit()


@compare_bp.route('/hot', methods=['GET'])
def get_hot_compare_tasks():
    """获取热门比价任务"""
    limit = request.args.get('limit', 4, type=int)
    
    # 获取已完成的比价任务，按创建时间排序
    tasks = CompareTask.query.filter_by(status='completed').order_by(CompareTask.created_at.desc()).limit(limit).all()
    
    result = []
    for task in tasks:
        # 获取任务相关的比价结果
        comparisons = PriceCompare.query.filter_by(task_id=task.id).all()
        
        # 构建商品列表
        products = []
        for comparison in comparisons:
            products.append({
                'name': comparison.platform + '商品',
                'price': comparison.price,
                'image': '/assets/images/product_placeholder.jpg'  # 使用占位图片
            })
        
        # 获取创建者信息
        creator = User.query.get(task.user_id)
        creator_name = creator.username if creator else '匿名用户'
        
        task_dict = {
            'id': task.id,
            'title': f'商品比价任务 #{task.id}',
            'products': products,
            'creator': creator_name,
            'likes': task.likes if hasattr(task, 'likes') else 0  # 假设任务有likes字段
        }
        result.append(task_dict)
    
    return jsonify({'data': result}), 200


def crawl_product_prices(url):
    """爬取商品价格（示例函数，实际需要根据不同电商平台进行定制）"""
    results = []
    
    try:
        # 模拟不同平台的比价结果
        # 这里只是示例，实际需要实现针对不同电商平台的爬虫逻辑
        # 并且要遵守robots协议，避免过度爬取
        
        # 京东示例
        if 'jd.com' in url:
            price = extract_jd_price(url)
            if price:
                results.append({
                    'platform': '京东',
                    'price': price,
                    'url': url
                })
        # 淘宝示例
        elif 'taobao.com' in url or 'tmall.com' in url:
            price = extract_taobao_price(url)
            if price:
                results.append({
                    'platform': '淘宝/天猫',
                    'price': price,
                    'url': url
                })
        # 拼多多示例
        elif 'pinduoduo.com' in url:
            price = extract_pdd_price(url)
            if price:
                results.append({
                    'platform': '拼多多',
                    'price': price,
                    'url': url
                })
        
        # 其他平台或通用方法
        else:
            price = extract_generic_price(url)
            if price:
                results.append({
                    'platform': '其他平台',
                    'price': price,
                    'url': url
                })
        
    except Exception as e:
        print(f"比价失败: {str(e)}")
        
    return results


def extract_jd_price(url):
    """示例：提取京东商品价格"""
    # 这里是示例实现，实际需要发送请求并解析页面
    # 注意：实际爬虫需要遵守网站robots协议
    # 为了避免实际网络请求，这里返回一个模拟价格
    return 100  # 示例价格


def extract_taobao_price(url):
    """示例：提取淘宝/天猫商品价格"""
    # 这里是示例实现，实际需要发送请求并解析页面
    return 105  # 示例价格


def extract_pdd_price(url):
    """示例：提取拼多多商品价格"""
    # 这里是示例实现，实际需要发送请求并解析页面
    return 95  # 示例价格


def extract_generic_price(url):
    """示例：通用价格提取方法"""
    # 这里是示例实现，实际需要发送请求并解析页面
    # 以下是一个简化版的实现
    try:
        # 设置请求头，模拟浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 发送请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 解析页面
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尝试从页面中提取价格信息（这是一个通用的方法，可能不适用所有网站）
        # 查找包含价格的元素
        price_text = None
        
        # 尝试常见的价格元素选择器
        price_selectors = [
            '.price', '.current-price', '.original-price', '#price',
            'span[class*="price"]', 'div[class*="price"]'
        ]
        
        for selector in price_selectors:
            price_element = soup.select_one(selector)
            if price_element:
                price_text = price_element.get_text().strip()
                break
        
        # 如果找到了价格文本，尝试提取数字
        if price_text:
            # 使用正则表达式提取数字
            price_match = re.search(r'\d+\.?\d*', price_text)
            if price_match:
                return int(float(price_match.group()) * 100)  # 转换为分
        
    except Exception:
        pass
    
    return None