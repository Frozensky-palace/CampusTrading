// HTTP请求相关工具函数
import axios, { type AxiosRequestConfig, type AxiosResponse, type AxiosError } from 'axios';

// 重试配置接口
export interface RetryConfig {
  maxRetries?: number;
  retryDelay?: number;
  retryableStatuses?: number[];
  retryableMethods?: string[];
}

// 默认重试配置
const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 3,
  retryDelay: 1000,
  retryableStatuses: [408, 429, 500, 502, 503, 504],
  retryableMethods: ['GET', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'PATCH']
};

// 延迟函数
function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// 请求重试中间件
export function retryMiddleware(config: RetryConfig = {}) {
  const { maxRetries = DEFAULT_RETRY_CONFIG.maxRetries!, 
         retryDelay = DEFAULT_RETRY_CONFIG.retryDelay!, 
         retryableStatuses = DEFAULT_RETRY_CONFIG.retryableStatuses!, 
         retryableMethods = DEFAULT_RETRY_CONFIG.retryableMethods! } = config;

  return async <T = any>(
    request: () => Promise<AxiosResponse<T>>,
    reqConfig: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> => {
    let lastError: AxiosError | null = null;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        if (attempt > 0) {
          // 计算指数退避延迟时间
          const currentDelay = retryDelay * Math.pow(2, attempt - 1);
          // 添加随机抖动，避免多个请求同时重试
          const jitter = Math.random() * retryDelay * 0.5;
          await delay(currentDelay + jitter);
          console.log(`Retry attempt ${attempt} for ${reqConfig.method?.toUpperCase()} ${reqConfig.url}`);
        }
        
        return await request();
      } catch (error) {
        lastError = error as AxiosError;
        
        // 判断是否应该重试
        const shouldRetry = 
          lastError.response &&
          retryableStatuses.includes(lastError.response.status) &&
          retryableMethods.includes(reqConfig.method?.toUpperCase() || '');
        
        if (!shouldRetry || attempt >= maxRetries) {
          break;
        }
      }
    }
    
    throw lastError;
  };
}

// 带重试的请求函数
export async function requestWithRetry<T = any>(
  config: AxiosRequestConfig,
  retryConfig: RetryConfig = {}
): Promise<AxiosResponse<T>> {
  const retry = retryMiddleware(retryConfig);
  
  return retry(() => axios(config), config);
}

// 错误处理函数
export function handleHttpError(error: any): string {
  if (error.response) {
    // 服务器返回错误状态码
    switch (error.response.status) {
      case 400:
        return error.response.data?.message || '请求参数错误';
      case 401:
        return error.response.data?.message || '未授权，请登录';
      case 403:
        return error.response.data?.message || '拒绝访问';
      case 404:
        return error.response.data?.message || '请求的资源不存在';
      case 405:
        return error.response.data?.message || '请求方法不允许';
      case 406:
        return error.response.data?.message || '请求的格式不支持';
      case 408:
        return error.response.data?.message || '请求超时';
      case 409:
        return error.response.data?.message || '请求冲突';
      case 429:
        return error.response.data?.message || '请求过于频繁';
      case 500:
        return error.response.data?.message || '服务器内部错误';
      case 502:
        return error.response.data?.message || '网关错误';
      case 503:
        return error.response.data?.message || '服务不可用';
      case 504:
        return error.response.data?.message || '网关超时';
      default:
        return error.response.data?.message || `请求失败 (${error.response.status})`;
    }
  } else if (error.request) {
    // 请求发出但没有收到响应
    return '网络错误，请检查网络连接';
  } else {
    // 请求配置错误
    return error.message || '请求错误';
  }
}

// 检查响应是否成功
export function isResponseSuccessful(response: any): boolean {
  return (
    response &&
    response.status >= 200 &&
    response.status < 300
  );
}

// 检查响应是否包含错误
export function hasResponseError(response: any): boolean {
  return !isResponseSuccessful(response);
}

// 格式化请求日志
export function formatRequestLog(config: AxiosRequestConfig): string {
  const method = config.method?.toUpperCase() || 'GET';
  const url = config.url || '';
  const headers = config.headers ? JSON.stringify(config.headers) : '';
  const data = config.data ? JSON.stringify(config.data) : '';
  
  return `[${new Date().toISOString()}] ${method} ${url}\nHeaders: ${headers}\nData: ${data}`;
}

// 格式化响应日志
export function formatResponseLog(response: AxiosResponse): string {
  const method = response.config.method?.toUpperCase() || 'GET';
  const url = response.config.url || '';
  const status = response.status;
  const data = response.data ? JSON.stringify(response.data) : '';
  
  return `[${new Date().toISOString()}] ${method} ${url} ${status}\nData: ${data}`;
}

// 格式化错误日志
export function formatErrorLog(error: AxiosError): string {
  const method = error.config?.method?.toUpperCase() || 'GET';
  const url = error.config?.url || '';
  const status = error.response?.status || 'N/A';
  const message = error.message || 'Unknown error';
  const responseData = error.response?.data ? JSON.stringify(error.response.data) : '';
  
  return `[${new Date().toISOString()}] ${method} ${url} ${status}\nError: ${message}\nResponse Data: ${responseData}`;
}

// 创建axios实例
export function createAxiosInstance(baseURL?: string, timeout: number = 10000) {
  const instance = axios.create({
    baseURL,
    timeout,
    headers: {
      'Content-Type': 'application/json'
    }
  });

  // 请求拦截器
  instance.interceptors.request.use(
    (config) => {
      // 可以在这里添加token、loading等
      console.log('Request:', formatRequestLog(config));
      return config;
    },
    (error) => {
      console.error('Request error:', formatErrorLog(error));
      return Promise.reject(error);
    }
  );

  // 响应拦截器
  instance.interceptors.response.use(
    (response) => {
      console.log('Response:', formatResponseLog(response));
      return response;
    },
    (error) => {
      console.error('Response error:', formatErrorLog(error));
      return Promise.reject(error);
    }
  );

  return instance;
}

// 批量请求函数
export async function batchRequests<T = any>(
  requests: Array<() => Promise<AxiosResponse<T>>>,
  concurrency: number = 5
): Promise<AxiosResponse<T>[]> {
  const results: AxiosResponse<T>[] = [];
  const executing: Promise<void>[] = [];
  const queue = [...requests];

  while (queue.length > 0 || executing.length > 0) {
    // 当执行中的请求数小于并发数且队列中有请求时，执行请求
    while (executing.length < concurrency && queue.length > 0) {
      const request = queue.shift();
      if (request) {
        const promise = request()
          .then((response) => {
            results.push(response);
          })
          .catch((error) => {
            // 这里可以选择抛出错误或继续执行
            console.error('Batch request error:', error);
            throw error;
          })
          .finally(() => {
            // 从执行队列中移除已完成的请求
            const index = executing.indexOf(promise);
            if (index > -1) {
              executing.splice(index, 1);
            }
          });
        
        executing.push(promise as Promise<void>);
      }
    }
    
    // 如果还有执行中的请求，等待其中一个完成
    if (executing.length > 0) {
      await Promise.race(executing);
    }
  }
  
  return results;
}

// 取消请求的工厂函数
export function createCancelToken() {
  const CancelToken = axios.CancelToken;
  return new CancelToken((cancel) => cancel);
}

// 检查网络连接
export async function checkNetworkConnection(): Promise<boolean> {
  try {
    await fetch('https://www.google.com', {
      method: 'HEAD',
      mode: 'no-cors',
      cache: 'no-cache'
    });
    return true;
  } catch (error) {
    return false;
  }
}

// 获取IP地址（通过第三方服务）
export async function getIpAddress(): Promise<string | null> {
  try {
    const response = await axios.get('https://api.ipify.org?format=json');
    return response.data.ip || null;
  } catch (error) {
    console.error('Failed to get IP address:', error);
    return null;
  }
}

// 上传文件进度监控
export function uploadProgressMonitor(onProgress: (progress: number) => void) {
  return {
    onUploadProgress: (event: ProgressEvent) => {
      if (event.lengthComputable) {
        const percentCompleted = Math.round((event.loaded * 100) / event.total);
        onProgress(percentCompleted);
      }
    }
  };
}

// 下载文件进度监控
export function downloadProgressMonitor(onProgress: (progress: number) => void) {
  return {
    onDownloadProgress: (event: ProgressEvent) => {
      if (event.lengthComputable) {
        const percentCompleted = Math.round((event.loaded * 100) / event.total);
        onProgress(percentCompleted);
      }
    }
  };
}