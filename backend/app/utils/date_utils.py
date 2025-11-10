import datetime
import time
from dateutil import parser
from dateutil.relativedelta import relativedelta
import pytz


class DateUtils:
    """日期时间工具类"""
    
    @staticmethod
    def now(tz=None):
        """获取当前时间"""
        if tz:
            if isinstance(tz, str):
                tz = pytz.timezone(tz)
            return datetime.datetime.now(tz)
        return datetime.datetime.now()
    
    @staticmethod
    def today(tz=None):
        """获取今天日期"""
        return DateUtils.now(tz).date()
    
    @staticmethod
    def tomorrow(tz=None):
        """获取明天日期"""
        return DateUtils.today(tz) + datetime.timedelta(days=1)
    
    @staticmethod
    def yesterday(tz=None):
        """获取昨天日期"""
        return DateUtils.today(tz) - datetime.timedelta(days=1)
    
    @staticmethod
    def parse_date(date_str, format=None):
        """解析日期字符串"""
        if not date_str:
            return None
        
        try:
            if format:
                return datetime.datetime.strptime(date_str, format)
            else:
                return parser.parse(date_str)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def format_date(date_obj, format='%Y-%m-%d'):
        """格式化日期对象"""
        if not date_obj:
            return ''
        
        try:
            return date_obj.strftime(format)
        except (ValueError, TypeError):
            return ''
    
    @staticmethod
    def format_time(time_obj, format='%H:%M:%S'):
        """格式化时间对象"""
        if not time_obj:
            return ''
        
        try:
            return time_obj.strftime(format)
        except (ValueError, TypeError):
            return ''
    
    @staticmethod
    def format_datetime(datetime_obj, format='%Y-%m-%d %H:%M:%S'):
        """格式化日期时间对象"""
        if not datetime_obj:
            return ''
        
        try:
            return datetime_obj.strftime(format)
        except (ValueError, TypeError):
            return ''
    
    @staticmethod
    def to_utc(date_obj):
        """转换为UTC时间"""
        if not date_obj:
            return None
        
        if date_obj.tzinfo:
            return date_obj.astimezone(pytz.UTC)
        else:
            # 假设是本地时间
            local_tz = pytz.timezone('Asia/Shanghai')  # 默认使用北京时间
            local_dt = local_tz.localize(date_obj)
            return local_dt.astimezone(pytz.UTC)
    
    @staticmethod
    def from_utc(utc_dt, target_tz='Asia/Shanghai'):
        """从UTC时间转换到目标时区"""
        if not utc_dt:
            return None
        
        if not utc_dt.tzinfo:
            # 假设是UTC时间
            utc_dt = pytz.UTC.localize(utc_dt)
        
        if isinstance(target_tz, str):
            target_tz = pytz.timezone(target_tz)
        
        return utc_dt.astimezone(target_tz)
    
    @staticmethod
    def is_valid_date(date_str, format=None):
        """验证日期字符串是否有效"""
        return DateUtils.parse_date(date_str, format) is not None
    
    @staticmethod
    def get_time_diff(start_time, end_time, unit='seconds'):
        """计算时间差"""
        if not start_time or not end_time:
            return 0
        
        diff = end_time - start_time
        
        if unit == 'seconds':
            return diff.total_seconds()
        elif unit == 'minutes':
            return diff.total_seconds() / 60
        elif unit == 'hours':
            return diff.total_seconds() / 3600
        elif unit == 'days':
            return diff.days
        elif unit == 'weeks':
            return diff.days / 7
        else:
            return diff.total_seconds()
    
    @staticmethod
    def add_days(date_obj, days):
        """添加天数"""
        if not date_obj:
            return None
        
        return date_obj + datetime.timedelta(days=days)
    
    @staticmethod
    def add_hours(date_obj, hours):
        """添加小时数"""
        if not date_obj:
            return None
        
        return date_obj + datetime.timedelta(hours=hours)
    
    @staticmethod
    def add_minutes(date_obj, minutes):
        """添加分钟数"""
        if not date_obj:
            return None
        
        return date_obj + datetime.timedelta(minutes=minutes)
    
    @staticmethod
    def subtract_days(date_obj, days):
        """减去天数"""
        return DateUtils.add_days(date_obj, -days)
    
    @staticmethod
    def get_month_start(date_obj=None):
        """获取月初日期"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        return date_obj.replace(day=1)
    
    @staticmethod
    def get_month_end(date_obj=None):
        """获取月末日期"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        next_month = date_obj.replace(day=28) + datetime.timedelta(days=4)
        return next_month - datetime.timedelta(days=next_month.day)
    
    @staticmethod
    def get_week_start(date_obj=None, week_start=0):
        """获取周初日期"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        days_since_week_start = (date_obj.weekday() - week_start) % 7
        return date_obj - datetime.timedelta(days=days_since_week_start)
    
    @staticmethod
    def get_week_end(date_obj=None, week_start=0):
        """获取周末日期"""
        week_start_date = DateUtils.get_week_start(date_obj, week_start)
        return week_start_date + datetime.timedelta(days=6)
    
    @staticmethod
    def is_same_day(date1, date2):
        """判断是否是同一天"""
        if not date1 or not date2:
            return False
        
        if isinstance(date1, datetime.datetime):
            date1 = date1.date()
        if isinstance(date2, datetime.datetime):
            date2 = date2.date()
        
        return date1 == date2
    
    @staticmethod
    def is_before(date1, date2):
        """判断date1是否在date2之前"""
        if not date1 or not date2:
            return False
        
        return date1 < date2
    
    @staticmethod
    def is_after(date1, date2):
        """判断date1是否在date2之后"""
        if not date1 or not date2:
            return False
        
        return date1 > date2
    
    @staticmethod
    def is_between(date, start_date, end_date):
        """判断date是否在start_date和end_date之间"""
        if not date or not start_date or not end_date:
            return False
        
        return start_date <= date <= end_date
    
    @staticmethod
    def get_age(birth_date):
        """计算年龄"""
        if not birth_date:
            return 0
        
        today = DateUtils.today()
        try:
            # 处理闰年2月29日的情况
            birth_date_this_year = birth_date.replace(year=today.year)
        except ValueError:
            # 闰年2月29日，今年不是闰年
            birth_date_this_year = birth_date.replace(year=today.year, month=3, day=1)
        
        if birth_date_this_year > today:
            return today.year - birth_date.year - 1
        else:
            return today.year - birth_date.year
    
    @staticmethod
    def get_timestamp(date_obj=None):
        """获取时间戳"""
        if not date_obj:
            return int(time.time())
        
        if isinstance(date_obj, datetime.datetime):
            # 如果有时区，转换为UTC
            if date_obj.tzinfo:
                date_obj = date_obj.astimezone(pytz.UTC)
                return int(date_obj.timestamp())
            else:
                return int(date_obj.timestamp())
        elif isinstance(date_obj, datetime.date):
            # 转换为日期的开始时间
            dt = datetime.datetime.combine(date_obj, datetime.time.min)
            return int(dt.timestamp())
        else:
            return int(time.time())
    
    @staticmethod
    def from_timestamp(timestamp):
        """从时间戳创建日期时间对象"""
        if not timestamp:
            return None
        
        try:
            if isinstance(timestamp, str):
                timestamp = float(timestamp)
            return datetime.datetime.fromtimestamp(timestamp)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def get_time_ago(date_obj):
        """获取相对时间描述（如：3分钟前，2小时前，5天前）"""
        if not date_obj:
            return ''
        
        now = DateUtils.now()
        if isinstance(date_obj, datetime.date) and not isinstance(date_obj, datetime.datetime):
            date_obj = datetime.datetime.combine(date_obj, datetime.time.min)
        
        diff = now - date_obj
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years}年前"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months}个月前"
        elif diff.days > 0:
            return f"{diff.days}天前"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}小时前"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes}分钟前"
        else:
            return "刚刚"
    
    @staticmethod
    def get_next_weekday(date_obj, weekday):
        """获取下一个指定的星期几"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        days_ahead = weekday - date_obj.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        
        return date_obj + datetime.timedelta(days=days_ahead)
    
    @staticmethod
    def get_prev_weekday(date_obj, weekday):
        """获取上一个指定的星期几"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        days_behind = date_obj.weekday() - weekday
        if days_behind <= 0:
            days_behind += 7
        
        return date_obj - datetime.timedelta(days=days_behind)
    
    @staticmethod
    def get_month_diff(start_date, end_date):
        """计算月份差"""
        if not start_date or not end_date:
            return 0
        
        if isinstance(start_date, datetime.datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.date()
        
        rd = relativedelta(end_date, start_date)
        return rd.years * 12 + rd.months
    
    @staticmethod
    def get_season(date_obj=None):
        """获取季节"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        month = date_obj.month
        if 3 <= month <= 5:
            return 'spring'  # 春季
        elif 6 <= month <= 8:
            return 'summer'  # 夏季
        elif 9 <= month <= 11:
            return 'autumn'  # 秋季
        else:
            return 'winter'  # 冬季
    
    @staticmethod
    def format_iso8601(date_obj):
        """格式化为ISO8601标准"""
        if not date_obj:
            return ''
        
        try:
            if date_obj.tzinfo:
                return date_obj.isoformat()
            else:
                # 添加Z表示UTC时间
                return date_obj.isoformat() + 'Z'
        except (ValueError, TypeError):
            return ''
    
    @staticmethod
    def parse_iso8601(date_str):
        """解析ISO8601格式的日期字符串"""
        if not date_str:
            return None
        
        try:
            return parser.isoparse(date_str)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def get_business_day(date_obj, days, holidays=None):
        """获取指定工作日之后的日期（跳过周末和节假日）"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        if holidays is None:
            holidays = []
        
        current_date = date_obj
        remaining_days = abs(days)
        sign = 1 if days > 0 else -1
        
        while remaining_days > 0:
            current_date += datetime.timedelta(days=sign)
            # 检查是否是周末
            if current_date.weekday() >= 5:
                continue
            # 检查是否是节假日
            if any(DateUtils.is_same_day(current_date, holiday) for holiday in holidays):
                continue
            remaining_days -= 1
        
        return current_date
    
    @staticmethod
    def is_workday(date_obj, holidays=None):
        """判断是否是工作日"""
        if not date_obj:
            return False
        
        if holidays is None:
            holidays = []
        
        # 检查是否是周末
        if date_obj.weekday() >= 5:
            return False
        # 检查是否是节假日
        if any(DateUtils.is_same_day(date_obj, holiday) for holiday in holidays):
            return False
        
        return True
    
    @staticmethod
    def get_day_of_year(date_obj=None):
        """获取一年中的第几天"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        return date_obj.timetuple().tm_yday
    
    @staticmethod
    def get_quarter(date_obj=None):
        """获取季度"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        month = date_obj.month
        if 1 <= month <= 3:
            return 1
        elif 4 <= month <= 6:
            return 2
        elif 7 <= month <= 9:
            return 3
        else:
            return 4
    
    @staticmethod
    def get_last_day_of_quarter(date_obj=None):
        """获取季度的最后一天"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        quarter = DateUtils.get_quarter(date_obj)
        year = date_obj.year
        
        if quarter == 1:
            return datetime.date(year, 3, 31)
        elif quarter == 2:
            return datetime.date(year, 6, 30)
        elif quarter == 3:
            return datetime.date(year, 9, 30)
        else:
            return datetime.date(year, 12, 31)
    
    @staticmethod
    def get_first_day_of_quarter(date_obj=None):
        """获取季度的第一天"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        quarter = DateUtils.get_quarter(date_obj)
        year = date_obj.year
        
        if quarter == 1:
            return datetime.date(year, 1, 1)
        elif quarter == 2:
            return datetime.date(year, 4, 1)
        elif quarter == 3:
            return datetime.date(year, 7, 1)
        else:
            return datetime.date(year, 10, 1)
    
    @staticmethod
    def get_timezone_abbr(date_obj=None, tz='Asia/Shanghai'):
        """获取时区缩写"""
        if not date_obj:
            date_obj = DateUtils.now()
        
        if isinstance(tz, str):
            tz = pytz.timezone(tz)
        
        if not date_obj.tzinfo:
            date_obj = tz.localize(date_obj)
        else:
            date_obj = date_obj.astimezone(tz)
        
        return date_obj.strftime('%Z')
    
    @staticmethod
    def get_timezone_offset(date_obj=None, tz='Asia/Shanghai'):
        """获取时区偏移量（以分钟为单位）"""
        if not date_obj:
            date_obj = DateUtils.now()
        
        if isinstance(tz, str):
            tz = pytz.timezone(tz)
        
        if not date_obj.tzinfo:
            date_obj = tz.localize(date_obj)
        else:
            date_obj = date_obj.astimezone(tz)
        
        offset_seconds = date_obj.utcoffset().total_seconds()
        return int(offset_seconds / 60)
    
    @staticmethod
    def get_day_name(date_obj=None, locale=None):
        """获取星期几的名称"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        # 这里可以根据locale返回不同语言的星期名称
        # 简化实现，只返回中文星期名称
        day_names = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        return day_names[date_obj.weekday()]
    
    @staticmethod
    def get_month_name(date_obj=None, locale=None):
        """获取月份的名称"""
        if not date_obj:
            date_obj = DateUtils.today()
        
        # 这里可以根据locale返回不同语言的月份名称
        # 简化实现，只返回中文月份名称
        month_names = ['一月', '二月', '三月', '四月', '五月', '六月',
                      '七月', '八月', '九月', '十月', '十一月', '十二月']
        return month_names[date_obj.month - 1]
    
    @staticmethod
    def convert_to_timezone(date_obj, target_tz):
        """转换日期时间到指定时区"""
        if not date_obj:
            return None
        
        if isinstance(target_tz, str):
            target_tz = pytz.timezone(target_tz)
        
        if not date_obj.tzinfo:
            # 假设当前是UTC时间
            date_obj = pytz.UTC.localize(date_obj)
        
        return date_obj.astimezone(target_tz)
    
    @staticmethod
    def is_leap_year(year):
        """判断是否是闰年"""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    @staticmethod
    def get_days_in_month(year, month):
        """获取指定月份的天数"""
        if month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            return 29 if DateUtils.is_leap_year(year) else 28
        else:
            return 31


# 常用日期时间格式常量
DATE_FORMAT_ISO = '%Y-%m-%d'
DATE_FORMAT_CN = '%Y年%m月%d日'
TIME_FORMAT_ISO = '%H:%M:%S'
TIME_FORMAT_CN = '%H时%M分%S秒'
DATETIME_FORMAT_ISO = '%Y-%m-%d %H:%M:%S'
DATETIME_FORMAT_CN = '%Y年%m月%d日 %H时%M分%S秒'
DATETIME_FORMAT_COMPACT = '%Y%m%d%H%M%S'
DATETIME_FORMAT_SHORT = '%Y-%m-%d %H:%M'


# 快捷函数
def now():
    """获取当前时间"""
    return DateUtils.now()

def today():
    """获取今天日期"""
    return DateUtils.today()

def format_date(date_obj, format=DATE_FORMAT_ISO):
    """格式化日期"""
    return DateUtils.format_date(date_obj, format)

def format_datetime(date_obj, format=DATETIME_FORMAT_ISO):
    """格式化日期时间"""
    return DateUtils.format_datetime(date_obj, format)

def parse_date(date_str, format=None):
    """解析日期字符串"""
    return DateUtils.parse_date(date_str, format)

def get_time_ago(date_obj):
    """获取相对时间描述"""
    return DateUtils.get_time_ago(date_obj)

def get_timestamp(date_obj=None):
    """获取时间戳"""
    return DateUtils.get_timestamp(date_obj)

def from_timestamp(timestamp):
    """从时间戳创建日期时间对象"""
    return DateUtils.from_timestamp(timestamp)