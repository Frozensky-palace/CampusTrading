// 通用工具函数

// 日期格式化函数
export function formatDate(date: Date | string | number, format: string = 'YYYY-MM-DD HH:mm:ss'): string {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');

  return format
    .replace('YYYY', year.toString())
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
}

// 相对时间格式化
export const formatTime = (time: Date | string | number, format?: string) => {
  const now = new Date();
  const targetTime = new Date(time);
  const diff = now.getTime() - targetTime.getTime();
  const minutes = Math.floor(diff / 1000 / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  
  if (format === 'relative' || !format) {
    if (minutes < 60) {
      return `${minutes}分钟前`;
    } else if (hours < 24) {
      return `${hours}小时前`;
    } else if (days < 30) {
      return `${days}天前`;
    } else {
      return formatDate(targetTime, 'YYYY-MM-DD');
    }
  } else {
    return formatDate(targetTime, format);
  }
};

// 年份格式化
export const formatYear = (time: Date | string | number) => {
  const d = new Date(time);
  return d.getFullYear().toString();
};

// 价格格式化函数
export function formatPrice(price: number | string): string {
  const num = typeof price === 'string' ? parseFloat(price) : price;
  if (isNaN(num)) return '¥0.00';
  return `¥${num.toFixed(2)}`;
}

// 数字格式化函数
export function formatNumber(num: number | string, digits: number = 0): string {
  const n = typeof num === 'string' ? parseFloat(num) : num;
  if (isNaN(n)) return '0';
  
  if (n >= 10000) {
    return (n / 10000).toFixed(digits) + '万';
  }
  if (n >= 1000) {
    return (n / 1000).toFixed(digits) + 'k';
  }
  return n.toString();
}

// 防抖函数
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null;
  
  return function (this: any, ...args: Parameters<T>) {
    const context = this;
    
    if (timeout) {
      clearTimeout(timeout);
    }
    
    timeout = setTimeout(() => {
      func.apply(context, args);
    }, wait);
  };
}

// 节流函数
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null;
  let previous = 0;
  
  return function (this: any, ...args: Parameters<T>) {
    const now = Date.now();
    const remaining = wait - (now - previous);
    const context = this;
    
    if (remaining <= 0) {
      if (timeout) {
        clearTimeout(timeout);
        timeout = null;
      }
      previous = now;
      func.apply(context, args);
    } else if (!timeout) {
      timeout = setTimeout(() => {
        previous = Date.now();
        timeout = null;
        func.apply(context, args);
      }, remaining);
    }
  };
}

// 深拷贝函数
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  
  if (obj instanceof Date) {
    return new Date(obj.getTime()) as unknown as T;
  }
  
  if (obj instanceof Array) {
    return obj.map((item) => deepClone(item)) as unknown as T;
  }
  
  if (typeof obj === 'object') {
    const clonedObj: { [key: string]: any } = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key]);
      }
    }
    return clonedObj as T;
  }
  
  return obj;
}

// 获取URL参数函数
export function getUrlParams(url?: string): { [key: string]: string } {
  const queryString = url ? url.split('?')[1] : window.location.search.slice(1);
  const params: { [key: string]: string } = {};
  
  if (queryString) {
    const pairs = queryString.split('&');
    pairs.forEach((pair) => {
      const [key, value] = pair.split('=');
      params[decodeURIComponent(key)] = decodeURIComponent(value || '');
    });
  }
  
  return params;
}

// 生成唯一ID函数
export function generateId(prefix: string = ''): string {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substr(2, 9);
  return `${prefix}${timestamp}_${random}`;
}

// 验证邮箱函数
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
}

// 验证手机号函数
export function isValidPhone(phone: string): boolean {
  const phoneRegex = /^1[3-9]\d{9}$/;
  return phoneRegex.test(phone);
}

// 验证密码强度函数
export function checkPasswordStrength(password: string): 'weak' | 'medium' | 'strong' {
  if (password.length < 6) return 'weak';
  
  let score = 0;
  if (password.length >= 8) score++;
  if (password.match(/[a-z]/)) score++;
  if (password.match(/[A-Z]/)) score++;
  if (password.match(/\d/)) score++;
  if (password.match(/[^a-zA-Z0-9]/)) score++;
  
  if (score <= 2) return 'weak';
  if (score <= 4) return 'medium';
  return 'strong';
}

// 计算两个日期之间的天数
export function daysBetween(date1: Date | string | number, date2: Date | string | number): number {
  const d1 = new Date(date1);
  const d2 = new Date(date2);
  const diffTime = Math.abs(d2.getTime() - d1.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

// 格式化文件大小
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 截断文本函数
export function truncateText(text: string, maxLength: number, suffix: string = '...'): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + suffix;
}

// 数组去重函数
export function uniqueArray<T>(arr: T[]): T[] {
  return Array.from(new Set(arr));
}

// 对象合并函数
export function mergeObjects<T extends object, U extends object>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}

// 防抖节流组合函数
export function debounceAndThrottle<T extends (...args: any[]) => any>(
  func: T,
  debounceWait: number,
  throttleWait: number
): (...args: Parameters<T>) => void {
  let lastCall = 0;
  let lastInvoke = 0;
  let result: any;
  let timeout: ReturnType<typeof setTimeout> | null = null;
  
  const invokeFunc = function (this: any, time: number, ...args: Parameters<T>) {
    lastInvoke = time;
    result = func.apply(this, args);
    return result;
  };
  
  const leadingEdge = function (this: any, time: number, ...args: Parameters<T>) {
    lastInvoke = time;
    timeout = setTimeout(() => trailingEdge.apply(this, args), debounceWait);
    return invokeFunc.apply(this, [time, ...args]);
  };
  
  const remainingWait = function (time: number) {
    const timeSinceLastCall = time - lastCall;
    const timeSinceLastInvoke = time - lastInvoke;
    const timeWaiting = debounceWait - timeSinceLastCall;
    
    return Math.max(0, throttleWait - timeSinceLastInvoke, timeWaiting);
  };
  
  const shouldInvoke = function (time: number) {
    const timeSinceLastCall = time - lastCall;
    const timeSinceLastInvoke = time - lastInvoke;
    
    return (
      lastCall === 0 ||
      timeSinceLastCall >= debounceWait ||
      (timeSinceLastCall < debounceWait && timeSinceLastInvoke >= throttleWait)
    );
  };
  
  const trailingEdge = function (this: any, ...args: Parameters<T>) {
    timeout = null;
    if (lastCall >= lastInvoke) {
      return invokeFunc.apply(this, [lastCall, ...args]);
    }
    return result;
  };
  
  return function (this: any, ...args: Parameters<T>) {
    const time = Date.now();
    const isInvoking = shouldInvoke(time);
    
    lastCall = time;
    
    if (isInvoking) {
      if (timeout === null) {
        return leadingEdge.apply(this, [time, ...args]);
      }
      
      if (timeout !== null) {
        clearTimeout(timeout);
      }
      
      timeout = setTimeout(() => trailingEdge.apply(this, args), remainingWait(time));
    } else if (timeout === null) {
      timeout = setTimeout(() => trailingEdge.apply(this, args), debounceWait);
    }
    
    return result;
  };
}

// 下载文件函数
export function downloadFile(url: string, filename: string): void {
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// 复制文本到剪贴板函数
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      textArea.style.top = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      textArea.remove();
    }
    return true;
  } catch (error) {
    console.error('复制失败:', error);
    return false;
  }
}

// 滚动到页面顶部函数
export function scrollToTop(smooth: boolean = true): void {
  window.scrollTo({
    top: 0,
    behavior: smooth ? 'smooth' : 'auto'
  });
}

// 滚动到元素函数
export function scrollToElement(element: HTMLElement | string, smooth: boolean = true): void {
  let targetElement: HTMLElement | null;
  
  if (typeof element === 'string') {
    targetElement = document.querySelector(element);
  } else {
    targetElement = element;
  }
  
  if (targetElement) {
    targetElement.scrollIntoView({
      behavior: smooth ? 'smooth' : 'auto',
      block: 'start'
    });
  }
}

// 格式化描述文本
export function formatDescription(description: string): string {
  if (!description) return '';
  // 将换行符转换为<br>标签
  return description.replace(/\n/g, '<br>').replace(/\s+/g, ' ');
}

// 根据分类ID获取分类名称
export function getCategoryName(categoryId: string): string {
  const categoryMap: Record<string, string> = {
    'digital': '数码产品',
    'clothing': '服饰鞋包',
    'books': '图书文具',
    'sports': '运动户外',
    'beauty': '美妆个护',
    'furniture': '家居日用',
    'electronics': '电子电器',
    'others': '其他'
  };
  return categoryMap[categoryId] || '未知分类';
}

// 根据状态获取状态文本
export function getStatusText(status: string): string {
  const statusMap: Record<string, string> = {
    'active': '进行中',
    'completed': '已完成',
    'cancelled': '已取消',
    'pending': '待审核'
  };
  return statusMap[status] || '未知状态';
}

// 根据状态获取状态样式类
export function getStatusClass(status: string): string {
  const statusClassMap: Record<string, string> = {
    'active': 'status-active',
    'completed': 'status-completed',
    'cancelled': 'status-cancelled',
    'pending': 'status-pending'
  };
  return statusClassMap[status] || '';
}

// 获取信誉等级
export function getReputationLevel(reputationScore: number): string {
  if (reputationScore >= 500) return '钻石用户';
  if (reputationScore >= 300) return '铂金用户';
  if (reputationScore >= 200) return '黄金用户';
  if (reputationScore >= 100) return '白银用户';
  return '普通用户';
}

// 根据商品状态获取状态文本
export function getConditionText(condition: string): string {
  const conditionMap: Record<string, string> = {
    'new': '全新',
    'like-new': '九成新',
    'good': '良好',
    'fair': '一般'
  };
  return conditionMap[condition] || '未知状态';
}

// 根据交易方式获取文本
export function getTradeMethodText(method: string): string {
  const methodMap: Record<string, string> = {
    'meetup': '面交',
    'delivery': '快递',
    'both': '两者均可'
  };
  return methodMap[method] || '未知方式';
}