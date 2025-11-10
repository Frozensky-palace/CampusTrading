import re
import datetime
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from flask import request


class ValidationError(Exception):
    """验证错误异常"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"字段 '{field}' 验证失败: {message}")


class Validator:
    """数据验证器基类"""
    def __init__(self, field_name):
        self.field_name = field_name
        self.validations = []
        self.error_messages = {}
    
    def required(self, message=None):
        """验证字段是否必填"""
        if not message:
            message = f"{self.field_name} 是必填项"
        
        def validate(value):
            if value is None or (isinstance(value, str) and value.strip() == ''):
                raise ValidationError(self.field_name, message)
            return True
        
        self.validations.append(validate)
        self.error_messages['required'] = message
        return self
    
    def type_(self, expected_type, message=None):
        """验证字段类型"""
        if not message:
            message = f"{self.field_name} 必须是 {expected_type.__name__} 类型"
        
        def validate(value):
            if not isinstance(value, expected_type):
                raise ValidationError(self.field_name, message)
            return True
        
        self.validations.append(validate)
        self.error_messages['type'] = message
        return self
    
    def min_length(self, min_len, message=None):
        """验证字符串最小长度"""
        if not message:
            message = f"{self.field_name} 长度不能少于 {min_len} 个字符"
        
        def validate(value):
            if len(str(value)) < min_len:
                raise ValidationError(self.field_name, message)
            return True
        
        self.validations.append(validate)
        self.error_messages['min_length'] = message
        return self
    
    def max_length(self, max_len, message=None):
        """验证字符串最大长度"""
        if not message:
            message = f"{self.field_name} 长度不能超过 {max_len} 个字符"
        
        def validate(value):
            if len(str(value)) > max_len:
                raise ValidationError(self.field_name, message)
            return True
        
        self.validations.append(validate)
        self.error_messages['max_length'] = message
        return self
    
    def range_(self, min_val, max_val, message=None):
        """验证数值范围"""
        if not message:
            message = f"{self.field_name} 必须在 {min_val} 到 {max_val} 之间"
        
        def validate(value):
            if not (min_val <= value <= max_val):
                raise ValidationError(self.field_name, message)
            return True
        
        self.validations.append(validate)
        self.error_messages['range'] = message
        return self
    
    def pattern(self, regex, message=None):
        """验证正则表达式匹配"""
        if not message:
            message = f"{self.field_name} 格式不正确"
        
        def validate(value):
            if not re.match(regex, str(value)):
                raise ValidationError(self.field_name, message)
            return True
        
        self.validations.append(validate)
        self.error_messages['pattern'] = message
        return self
    
    def custom(self, validation_func, message=None):
        """自定义验证函数"""
        if not message:
            message = f"{self.field_name} 验证失败"
        
        def validate(value):
            if not validation_func(value):
                raise ValidationError(self.field_name, message)
            return True
        
        self.validations.append(validate)
        self.error_messages['custom'] = message
        return self
    
    def validate(self, value):
        """执行所有验证"""
        for validation in self.validations:
            validation(value)
        return True


class FormValidator:
    """表单验证器"""
    def __init__(self, data=None):
        self.data = data or (request.get_json() if request.is_json else request.form.to_dict())
        self.validators = {}
        self.errors = {}
    
    def add_validator(self, field_name, validator):
        """添加字段验证器"""
        self.validators[field_name] = validator
        return self
    
    def validate(self):
        """执行所有字段验证"""
        self.errors = {}
        
        for field_name, validator in self.validators.items():
            value = self.data.get(field_name)
            try:
                validator.validate(value)
            except ValidationError as e:
                self.errors[field_name] = e.message
        
        return len(self.errors) == 0


# 常用验证函数

def is_valid_email(email):
    """验证邮箱格式"""
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def is_valid_phone(phone, region='CN'):
    """验证手机号格式"""
    try:
        parsed_phone = phonenumbers.parse(phone, region)
        return phonenumbers.is_valid_number(parsed_phone)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


def is_valid_password(password):
    """验证密码强度（至少8位，包含字母和数字）"""
    if len(password) < 8:
        return False
    if not re.search(r'[a-zA-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True


def is_valid_username(username):
    """验证用户名格式（2-20位字母、数字、下划线）"""
    pattern = r'^[a-zA-Z0-9_]{2,20}$'
    return bool(re.match(pattern, username))


def is_valid_id_card(id_card):
    """验证身份证号格式（简单验证）"""
    pattern = r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$
    return bool(re.match(pattern, id_card))


def is_valid_date(date_str, format='%Y-%m-%d'):
    """验证日期格式"""
    try:
        datetime.datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def is_valid_url(url):
    """验证URL格式"""
    pattern = r'^(http|https)://[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)*(:[0-9]+)?(/\S*)?$'
    return bool(re.match(pattern, url))


def is_valid_price(price):
    """验证价格格式（正数，最多两位小数）"""
    pattern = r'^\d+(\.\d{1,2})?$'
    return bool(re.match(pattern, str(price))) and float(price) >= 0


def is_valid_decimal(value, max_digits=10, decimal_places=2):
    """验证小数格式"""
    try:
        float_val = float(value)
        # 检查整数部分位数
        integer_part = abs(int(float_val))
        if len(str(integer_part)) > (max_digits - decimal_places):
            return False
        # 检查小数部分位数
        decimal_part = abs(float_val - integer_part)
        if decimal_part != 0:
            decimal_str = str(decimal_part)[2:]
            if len(decimal_str) > decimal_places:
                return False
        return True
    except (ValueError, TypeError):
        return False


def is_valid_chinese(text):
    """验证是否包含中文字符"""
    pattern = r'[\u4e00-\u9fa5]'
    return bool(re.search(pattern, text))


def is_valid_string_length(text, min_len=1, max_len=255):
    """验证字符串长度"""
    if not isinstance(text, str):
        return False
    return min_len <= len(text) <= max_len


def is_valid_image_file(filename):
    """验证是否为图片文件"""
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    _, ext = os.path.splitext(filename.lower())
    return ext in valid_extensions


def is_valid_file_size(file_path, max_size_mb=5):
    """验证文件大小"""
    max_size_bytes = max_size_mb * 1024 * 1024
    try:
        return os.path.getsize(file_path) <= max_size_bytes
    except (OSError, TypeError):
        return False


def is_valid_page_number(page, min_page=1):
    """验证页码格式"""
    try:
        page_num = int(page)
        return page_num >= min_page
    except (ValueError, TypeError):
        return False


def is_valid_page_size(page_size, min_size=1, max_size=100):
    """验证每页数量格式"""
    try:
        size = int(page_size)
        return min_size <= size <= max_size
    except (ValueError, TypeError):
        return False


def is_valid_enum_value(value, enum_class):
    """验证值是否在枚举范围内"""
    try:
        enum_class(value)
        return True
    except ValueError:
        return False


def is_valid_array_length(arr, min_len=0, max_len=100):
    """验证数组长度"""
    if not isinstance(arr, (list, tuple)):
        return False
    return min_len <= len(arr) <= max_len


def is_valid_array_items(arr, item_validator):
    """验证数组中的所有元素"""
    if not isinstance(arr, (list, tuple)):
        return False
    return all(item_validator(item) for item in arr)


def is_valid_dict_keys(d, required_keys=None, optional_keys=None):
    """验证字典的键"""
    if not isinstance(d, dict):
        return False
    
    # 检查必需的键
    if required_keys:
        for key in required_keys:
            if key not in d:
                return False
    
    # 检查可选的键（如果提供了optional_keys，则只允许这些键）
    if optional_keys:
        allowed_keys = set(required_keys or []) | set(optional_keys)
        for key in d:
            if key not in allowed_keys:
                return False
    
    return True


def sanitize_input(input_str, allow_html=False):
    """清理输入字符串"""
    if not input_str:
        return ''
    
    # 转换为字符串
    input_str = str(input_str)
    
    # 去除首尾空白字符
    input_str = input_str.strip()
    
    # 如果不允许HTML，移除HTML标签
    if not allow_html:
        input_str = re.sub(r'<[^>]*>', '', input_str)
    
    return input_str


def sanitize_html(html_str):
    """清理HTML字符串（保留安全标签）"""
    if not html_str:
        return ''
    
    # 允许的安全标签
    allowed_tags = {'b', 'i', 'u', 's', 'strong', 'em', 'br', 'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote'}
    
    # 移除非允许的标签
    def clean_tag(match):
        tag = match.group(1).lower()
        if tag in allowed_tags:
            return match.group(0)
        return ''
    
    # 移除开始标签
    html_str = re.sub(r'<([^>]+)>', clean_tag, html_str)
    # 移除结束标签
    html_str = re.sub(r'</([^>]+)>', lambda m: f'</{m.group(1)}>' if m.group(1).lower() in allowed_tags else '', html_str)
    
    return html_str


def validate_pagination_params(params):
    """验证分页参数"""
    errors = {}
    
    # 验证页码
    page = params.get('page', 1)
    try:
        page = int(page)
        if page < 1:
            errors['page'] = '页码必须大于等于1'
    except ValueError:
        errors['page'] = '页码必须是整数'
    
    # 验证每页数量
    page_size = params.get('page_size', 10)
    try:
        page_size = int(page_size)
        if page_size < 1 or page_size > 100:
            errors['page_size'] = '每页数量必须在1到100之间'
    except ValueError:
        errors['page_size'] = '每页数量必须是整数'
    
    return {
        'page': page if 'page' not in errors else 1,
        'page_size': page_size if 'page_size' not in errors else 10,
        'errors': errors
    }


def validate_sort_params(params, allowed_fields=None):
    """验证排序参数"""
    errors = {}
    sort_field = params.get('sort_field', None)
    sort_order = params.get('sort_order', 'asc').lower()
    
    # 验证排序字段
    if allowed_fields and sort_field and sort_field not in allowed_fields:
        errors['sort_field'] = f'排序字段必须是以下之一: {allowed_fields}'
    
    # 验证排序顺序
    if sort_order not in ('asc', 'desc'):
        errors['sort_order'] = '排序顺序必须是 asc 或 desc'
    
    return {
        'sort_field': sort_field if 'sort_field' not in errors else None,
        'sort_order': sort_order if 'sort_order' not in errors else 'asc',
        'errors': errors
    }


def validate_search_params(params, max_length=255):
    """验证搜索参数"""
    errors = {}
    search = params.get('search', '')
    
    # 验证搜索长度
    if len(search) > max_length:
        errors['search'] = f'搜索内容不能超过 {max_length} 个字符'
    
    return {
        'search': search if 'search' not in errors else '',
        'errors': errors
    }

# 导入必要的模块
import os