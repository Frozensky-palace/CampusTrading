import { ElMessage, ElNotification, ElLoading } from 'element-plus';

// 显示消息提示
export function showMessage(message: string, type: 'success' | 'warning' | 'error' | 'info' = 'info') {
  ElMessage[type](message);
}

// 显示通知
export function showNotification(title: string, message: string, type: 'success' | 'warning' | 'error' | 'info' = 'info') {
  ElNotification[type]({
    title,
    message,
    duration: 3000
  });
}

// 显示加载状态
export function showLoading(message: string = '加载中...'): any {
  return ElLoading.service({
    lock: true,
    text: message,
    background: 'rgba(0, 0, 0, 0.7)'
  });
}

// 隐藏加载状态
export function hideLoading(loadingInstance: any) {
  if (loadingInstance && typeof loadingInstance.close === 'function') {
    loadingInstance.close();
  }
}