import axios from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';
import { useUserStore } from '../store';

// 扩展axios配置接口
interface RequestConfig extends InternalAxiosRequestConfig {
  loading?: boolean;
}

// 创建axios实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
request.interceptors.request.use(
  (config: RequestConfig) => {
    const userStore = useUserStore();
    
    // 如果有token，添加到请求头
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`;
    }
    
    // 添加loading状态
    if (config.loading !== false) {
      // 这里可以添加全局loading状态
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 关闭loading状态
    
    return response.data;
  },
  (error) => {
    // 关闭loading状态
    
    const userStore = useUserStore();
    
    // 处理错误
    if (error.response) {
      // 服务器返回错误状态码
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          userStore.clearToken();
          if (window.location.pathname !== '/login') {
            window.location.href = `/login?redirect=${encodeURIComponent(window.location.pathname)}`;
          }
          break;
        case 403:
          // 禁止访问
          console.error('禁止访问:', error.response.data?.message || '您没有权限执行此操作');
          break;
        case 404:
          // 资源不存在
          console.error('资源不存在:', error.response.data?.message || '请求的资源不存在');
          break;
        case 500:
          // 服务器错误
          console.error('服务器错误:', error.response.data?.message || '服务器内部错误，请稍后再试');
          break;
        default:
          console.error('请求失败:', error.response.data?.message || '请求失败，请稍后再试');
      }
    } else if (error.request) {
      // 请求发出但没有收到响应
      console.error('网络错误:', '无法连接到服务器，请检查网络连接');
    } else {
      // 请求配置错误
      console.error('请求错误:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default request;