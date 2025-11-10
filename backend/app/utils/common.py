import os
import sys
import json
import random
import string
import hashlib
import base64
import re
import uuid
from functools import wraps
from flask import request, jsonify, current_app


class CommonUtils:
    """通用工具类"""
    
    @staticmethod
    def generate_random_string(length=10, include_digits=True, include_special=False):
        """生成随机字符串"""
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        if include_special:
            chars += string.punctuation
        
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def generate_token(length=32):
        """生成令牌"""
        return CommonUtils.generate_random_string(length, include_digits=True, include_special=False)
    
    @staticmethod
    def generate_uuid():
        """生成UUID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def hash_string(text, algorithm='sha256'):
        """哈希字符串"""
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(text.encode('utf-8'))
        return hash_obj.hexdigest()
    
    @staticmethod
    def md5(text):
        """计算MD5哈希值"""
        return CommonUtils.hash_string(text, 'md5')
    
    @staticmethod
    def sha1(text):
        """计算SHA1哈希值"""
        return CommonUtils.hash_string(text, 'sha1')
    
    @staticmethod
    def sha256(text):
        """计算SHA256哈希值"""
        return CommonUtils.hash_string(text, 'sha256')
    
    @staticmethod
    def base64_encode(data):
        """Base64编码"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')
    
    @staticmethod
    def base64_decode(encoded_data):
        """Base64解码"""
        try:
            return base64.b64decode(encoded_data).decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def is_valid_uuid(uuid_str):
        """验证UUID格式"""
        try:
            uuid.UUID(uuid_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def merge_dicts(*dicts):
        """合并多个字典"""
        result = {}
        for d in dicts:
            if d:
                result.update(d)
        return result
    
    @staticmethod
    def remove_none_values(d):
        """移除字典中的None值"""
        if not isinstance(d, dict):
            return d
        return {k: v for k, v in d.items() if v is not None}
    
    @staticmethod
    def safe_get(data, keys, default=None):
        """安全地从嵌套字典中获取值"""
        if not isinstance(keys, list):
            keys = [keys]
        
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    @staticmethod
    def format_number(number, decimals=2):
        """格式化数字"""
        try:
            return round(float(number), decimals)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def format_price(price):
        """格式化价格"""
        try:
            return f"{float(price):.2f}"
        except (ValueError, TypeError):
            return "0.00"
    
    @staticmethod
    def format_percentage(value, decimals=2):
        """格式化百分比"""
        try:
            return f"{float(value) * 100:.{decimals}f}%"
        except (ValueError, TypeError):
            return "0.00%"
    
    @staticmethod
    def to_camel_case(snake_str):
        """蛇形命名转驼峰命名"""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def to_snake_case(camel_str):
        """驼峰命名转蛇形命名"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def convert_case(obj, case_func):
        """转换对象的键名大小写"""
        if isinstance(obj, dict):
            return {case_func(k): CommonUtils.convert_case(v, case_func) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [CommonUtils.convert_case(item, case_func) for item in obj]
        else:
            return obj
    
    @staticmethod
    def to_camel_case_dict(obj):
        """将字典的键名转换为驼峰命名"""
        return CommonUtils.convert_case(obj, CommonUtils.to_camel_case)
    
    @staticmethod
    def to_snake_case_dict(obj):
        """将字典的键名转换为蛇形命名"""
        return CommonUtils.convert_case(obj, CommonUtils.to_snake_case)
    
    @staticmethod
    def truncate_string(s, max_length, suffix='...'):
        """截断字符串"""
        if len(s) <= max_length:
            return s
        return s[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def wrap_text(s, width=80):
        """换行文本"""
        words = s.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + (1 if current_line else 0) > width:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                current_line.append(word)
                current_length += len(word) + (1 if current_line else 0)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    @staticmethod
    def get_file_extension(filename):
        """获取文件扩展名"""
        _, ext = os.path.splitext(filename)
        return ext.lower()
    
    @staticmethod
    def get_filename_without_extension(filename):
        """获取没有扩展名的文件名"""
        name, _ = os.path.splitext(filename)
        return name
    
    @staticmethod
    def ensure_directory(directory):
        """确保目录存在"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
    
    @staticmethod
    def is_file_path_safe(file_path, base_directory):
        """检查文件路径是否安全（防止路径遍历攻击）"""
        # 获取规范化的绝对路径
        try:
            abs_file_path = os.path.abspath(file_path)
            abs_base_dir = os.path.abspath(base_directory)
            # 检查文件路径是否在基础目录内
            return os.path.commonpath([abs_file_path, abs_base_dir]) == abs_base_dir
        except Exception:
            return False
    
    @staticmethod
    def read_json_file(file_path):
        """读取JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    @staticmethod
    def write_json_file(file_path, data, indent=2):
        """写入JSON文件"""
        try:
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory:
                CommonUtils.ensure_directory(directory)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            return True
        except Exception:
            return False
    
    @staticmethod
    def deep_merge(dict1, dict2):
        """深度合并字典"""
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = CommonUtils.deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    @staticmethod
    def chunk_list(lst, chunk_size):
        """将列表分块"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    @staticmethod
    def flatten_list(lst):
        """扁平化列表"""
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(CommonUtils.flatten_list(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def remove_duplicates(lst):
        """移除列表中的重复项"""
        if isinstance(lst[0], dict):
            # 对于字典列表，使用JSON序列化来去重
            seen = set()
            unique_list = []
            for item in lst:
                item_str = json.dumps(item, sort_keys=True)
                if item_str not in seen:
                    seen.add(item_str)
                    unique_list.append(item)
            return unique_list
        else:
            # 对于简单类型列表，直接转换为集合再转回列表
            return list(dict.fromkeys(lst))
    
    @staticmethod
    def find_in_list(lst, key, value):
        """在字典列表中查找指定键值的项"""
        for item in lst:
            if isinstance(item, dict) and item.get(key) == value:
                return item
        return None
    
    @staticmethod
    def group_by(lst, key_func):
        """根据指定的键函数对列表进行分组"""
        groups = {}
        for item in lst:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups
    
    @staticmethod
    def sort_by(lst, key_func, reverse=False):
        """根据指定的键函数对列表进行排序"""
        return sorted(lst, key=key_func, reverse=reverse)
    
    @staticmethod
    def unique_by(lst, key_func):
        """根据指定的键函数对列表去重"""
        seen = set()
        unique_list = []
        for item in lst:
            key = key_func(item)
            if key not in seen:
                seen.add(key)
                unique_list.append(item)
        return unique_list
    
    @staticmethod
    def safe_divide(a, b, default=0):
        """安全除法"""
        try:
            if b == 0:
                return default
            return a / b
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_int(value, default=0):
        """安全转换为整数"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_float(value, default=0.0):
        """安全转换为浮点数"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_bool(value, default=False):
        """安全转换为布尔值"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            value = value.lower()
            if value in ('true', 'yes', '1', 'y', 't'):
                return True
            if value in ('false', 'no', '0', 'n', 'f'):
                return False
        try:
            return bool(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def get_env_variable(name, default=None, required=False):
        """获取环境变量"""
        value = os.environ.get(name, default)
        if required and value is None:
            raise ValueError(f"环境变量 {name} 未设置")
        return value
    
    @staticmethod
    def set_env_variable(name, value):
        """设置环境变量"""
        os.environ[name] = str(value)
    
    @staticmethod
    def clean_dict(d, allowed_keys=None, remove_none=True):
        """清理字典"""
        if not isinstance(d, dict):
            return d
        
        result = {}
        for key, value in d.items():
            # 检查是否在允许的键列表中
            if allowed_keys and key not in allowed_keys:
                continue
            # 检查是否为None
            if remove_none and value is None:
                continue
            # 如果是嵌套字典，递归清理
            if isinstance(value, dict):
                result[key] = CommonUtils.clean_dict(value, allowed_keys, remove_none)
            # 如果是列表，递归清理每个元素
            elif isinstance(value, list):
                result[key] = [CommonUtils.clean_dict(item, allowed_keys, remove_none) for item in value]
            else:
                result[key] = value
        
        return result
    
    @staticmethod
    def sanitize_filename(filename):
        """清理文件名（移除不安全字符）"""
        # 只保留字母、数字、下划线、点、横线
        return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    
    @staticmethod
    def normalize_string(s):
        """规范化字符串"""
        if not s:
            return ''
        # 去除首尾空白字符
        s = s.strip()
        # 替换多个空格为单个空格
        s = re.sub(r'\s+', ' ', s)
        return s
    
    @staticmethod
    def distance(s1, s2):
        """计算编辑距离（Levenshtein距离）"""
        if len(s1) < len(s2):
            return CommonUtils.distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def similarity(s1, s2):
        """计算字符串相似度"""
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        return 1.0 - CommonUtils.distance(s1, s2) / max_len
    
    @staticmethod
    def retry(func, max_retries=3, delay=1, exceptions=(Exception,)):
        """重试函数执行"""
        for i in range(max_retries):
            try:
                return func()
            except exceptions as e:
                if i == max_retries - 1:
                    raise
                import time
                time.sleep(delay)
        return None


# 快捷函数
def random_string(length=10):
    """生成随机字符串"""
    return CommonUtils.generate_random_string(length)

def generate_token(length=32):
    """生成令牌"""
    return CommonUtils.generate_token(length)

def md5_hash(text):
    """计算MD5哈希值"""
    return CommonUtils.md5(text)

def sha256_hash(text):
    """计算SHA256哈希值"""
    return CommonUtils.sha256(text)

def safe_get(data, keys, default=None):
    """安全地从嵌套字典中获取值"""
    return CommonUtils.safe_get(data, keys, default)

def clean_dict(d, allowed_keys=None):
    """清理字典"""
    return CommonUtils.clean_dict(d, allowed_keys)

def to_camel_case(snake_str):
    """蛇形命名转驼峰命名"""
    return CommonUtils.to_camel_case(snake_str)

def to_snake_case(camel_str):
    """驼峰命名转蛇形命名"""
    return CommonUtils.to_snake_case(camel_str)

def ensure_dir(directory):
    """确保目录存在"""
    return CommonUtils.ensure_directory(directory)

def chunk_list(lst, chunk_size):
    """将列表分块"""
    return CommonUtils.chunk_list(lst, chunk_size)

def safe_int(value, default=0):
    """安全转换为整数"""
    return CommonUtils.safe_int(value, default)

def safe_float(value, default=0.0):
    """安全转换为浮点数"""
    return CommonUtils.safe_float(value, default)

def get_env(name, default=None, required=False):
    """获取环境变量"""
    return CommonUtils.get_env_variable(name, default, required)