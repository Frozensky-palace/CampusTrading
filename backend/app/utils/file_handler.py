import os
import uuid
import datetime
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """检查文件是否允许上传"""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_unique_filename(filename):
    """生成唯一的文件名"""
    filename = secure_filename(filename)
    name, ext = os.path.splitext(filename)
    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{name}_{timestamp}_{unique_id}{ext}"


def save_file(file, upload_folder):
    """保存文件到指定目录"""
    if not file or file.filename == '':
        return None, "未提供文件"
    
    if not allowed_file(file.filename):
        return None, "不允许的文件类型"
    
    # 确保上传目录存在
    os.makedirs(upload_folder, exist_ok=True)
    
    # 生成唯一文件名
    filename = generate_unique_filename(file.filename)
    
    # 保存文件
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    
    return filename, None


def get_file_path(filename, upload_folder):
    """获取文件的完整路径"""
    return os.path.join(upload_folder, filename)


def delete_file(filename, upload_folder):
    """删除文件"""
    file_path = os.path.join(upload_folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False


def get_file_size(filename, upload_folder):
    """获取文件大小（字节）"""
    file_path = os.path.join(upload_folder, filename)
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0


def get_file_url(filename, base_url):
    """获取文件的URL"""
    return f"{base_url}/{filename}"


def compress_image(file_path, output_path=None, quality=85):
    """压缩图片"""
    try:
        from PIL import Image
        
        if not output_path:
            output_path = file_path
        
        with Image.open(file_path) as img:
            # 转换为RGB模式（如果不是）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存图片并设置质量
            img.save(output_path, optimize=True, quality=quality)
        
        return True, None
    except Exception as e:
        return False, str(e)


def resize_image(file_path, width=None, height=None, output_path=None):
    """调整图片尺寸"""
    try:
        from PIL import Image
        
        if not output_path:
            output_path = file_path
        
        with Image.open(file_path) as img:
            # 计算调整后的尺寸（保持比例）
            img_width, img_height = img.size
            
            if width and height:
                # 按给定的宽高调整（可能会变形）
                new_size = (width, height)
            elif width:
                # 按给定的宽度调整，高度等比例缩放
                ratio = width / img_width
                new_size = (width, int(img_height * ratio))
            elif height:
                # 按给定的高度调整，宽度等比例缩放
                ratio = height / img_height
                new_size = (int(img_width * ratio), height)
            else:
                return False, "未提供宽高参数"
            
            # 调整图片尺寸
            resized_img = img.resize(new_size)
            
            # 保存调整后的图片
            resized_img.save(output_path)
        
        return True, None
    except Exception as e:
        return False, str(e)


def extract_text_from_file(file_path):
    """从文件中提取文本（支持常见文档格式）"""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            # 从PDF文件中提取文本
            import PyPDF2
            text = ''
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() + '\n'
            return text
        
        elif ext in ['.doc', '.docx']:
            # 从Word文档中提取文本
            import docx
            if ext == '.docx':
                doc = docx.Document(file_path)
                text = '\n'.join([para.text for para in doc.paragraphs])
            else:
                # 处理.doc文件（需要python-docx2txt库）
                import docx2txt
                text = docx2txt.process(file_path)
            return text
        
        elif ext in ['.xls', '.xlsx']:
            # 从Excel文件中提取文本
            import pandas as pd
            df = pd.read_excel(file_path)
            return df.to_string()
        
        elif ext in ['.txt', '.md', '.csv']:
            # 从文本文件中读取
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        else:
            return f"不支持的文件格式: {ext}"
    
    except Exception as e:
        return f"提取文本时出错: {str(e)}"


def create_thumbnail(file_path, thumbnail_path=None, size=(128, 128)):
    """创建缩略图"""
    try:
        from PIL import Image
        
        if not thumbnail_path:
            name, ext = os.path.splitext(file_path)
            thumbnail_path = f"{name}_thumbnail{ext}"
        
        with Image.open(file_path) as img:
            img.thumbnail(size)
            img.save(thumbnail_path)
        
        return thumbnail_path, None
    except Exception as e:
        return None, str(e)


def batch_process_files(directory, process_func):
    """批量处理目录中的文件"""
    results = []
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            result = process_func(file_path)
            results.append({
                'filename': filename,
                'result': result
            })
    
    return results


def scan_directory_for_files(directory, extensions=None):
    """扫描目录中的文件，支持按扩展名筛选"""
    files = []
    
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if extensions:
                ext = os.path.splitext(filename)[1].lower()
                if ext in extensions:
                    files.append(os.path.join(root, filename))
            else:
                files.append(os.path.join(root, filename))
    
    return files


def calculate_directory_size(directory):
    """计算目录的总大小（字节）"""
    total_size = 0
    
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    
    return total_size


def clear_directory(directory, keep_subdirs=True):
    """清空目录中的文件"""
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            os.remove(file_path)
        
        if not keep_subdirs:
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
    
    return True