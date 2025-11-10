import { defineStore } from 'pinia';
import request from '../api/request';

// 用户类型定义
interface User {
  id: string;
  username: string;
  nickname: string;
  avatar: string;
  email: string;
  phone: string;
  role: 'user' | 'admin';
  created_at: string;
  updated_at: string;
  // 其他用户信息字段
}

// 用户状态类型
interface UserState {
  user: User | null;
  token: string | null;
  isLoggedIn: boolean;
  isAdmin: boolean;
  loading: boolean;
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isLoggedIn: !!localStorage.getItem('token'),
    isAdmin: false,
    loading: false,
    error: null
  }),

  getters: {
    // 获取用户信息
    getUserInfo: (state) => state.user,
    // 检查是否登录
    checkLogin: (state) => state.isLoggedIn,
    // 检查是否为管理员
    checkAdmin: (state) => state.isAdmin,
    // 获取加载状态
    getLoading: (state) => state.loading,
    // 获取错误信息
    getError: (state) => state.error
  },

  actions: {
    // 设置token
    setToken(token: string) {
      this.token = token;
      localStorage.setItem('token', token);
      this.isLoggedIn = true;
    },

    // 清除token
    clearToken() {
      this.token = null;
      this.user = null;
      this.isLoggedIn = false;
      this.isAdmin = false;
      localStorage.removeItem('token');
    },

    // 设置用户信息
    setUserInfo(user: User) {
      this.user = user;
      this.isAdmin = user.role === 'admin';
    },

    // 设置错误信息
    setError(error: string) {
      this.error = error;
      // 3秒后清除错误信息
      setTimeout(() => {
        this.error = null;
      }, 3000);
    },

    // 登录
    async login(credentials: { username: string; password: string }) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await request.post('/auth/login', credentials);
        const { token, user } = response.data;
        
        this.setToken(token);
        this.setUserInfo(user);
        
        return { success: true, user };
      } catch (error: any) {
        this.error = error.response?.data?.message || '登录失败，请检查用户名和密码';
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    // 注册
    async register(userData: {
      username: string;
      password: string;
      nickname: string;
      email: string;
      phone: string;
    }) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await request.post('/auth/register', userData);
        
        return { success: true, message: response.data.message };
      } catch (error: any) {
        this.error = error.response?.data?.message || '注册失败，请稍后再试';
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    // 登出
    async logout() {
      try {
        await request.post('/auth/logout');
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        this.clearToken();
      }
    },

    // 获取用户信息
    async fetchUserInfo() {
      try {
        if (!this.token) return;
        
        this.loading = true;
        const response = await request.get('/users/me');
        
        this.setUserInfo(response.data);
        
        return { success: true, user: response.data };
      } catch (error: any) {
        // 如果token过期或无效，清除token
        if (error.response?.status === 401) {
          this.clearToken();
        }
        
        this.error = error.response?.data?.message || '获取用户信息失败';
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    // 更新用户信息
    async updateUserInfo(userData: Partial<User>) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await request.put('/users/me', userData);
        
        this.setUserInfo(response.data);
        
        return { success: true, user: response.data };
      } catch (error: any) {
        this.error = error.response?.data?.message || '更新用户信息失败';
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    // 更改密码
    async changePassword(passwordData: {
      currentPassword: string;
      newPassword: string;
      confirmPassword: string;
    }) {
      try {
        this.loading = true;
        this.error = null;
        
        await request.put('/users/me/password', passwordData);
        
        return { success: true, message: '密码更改成功' };
      } catch (error: any) {
        this.error = error.response?.data?.message || '更改密码失败';
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    // 发送重置密码邮件
    async forgotPassword(email: string) {
      try {
        this.loading = true;
        this.error = null;
        
        await request.post('/auth/forgot-password', { email });
        
        return { success: true, message: '重置密码邮件已发送' };
      } catch (error: any) {
        this.error = error.response?.data?.message || '发送邮件失败';
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    // 重置密码
    async resetPassword(resetData: {
      token: string;
      newPassword: string;
      confirmPassword: string;
    }) {
      try {
        this.loading = true;
        this.error = null;
        
        await request.post('/auth/reset-password', resetData);
        
        return { success: true, message: '密码重置成功' };
      } catch (error: any) {
        this.error = error.response?.data?.message || '重置密码失败';
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    // 初始化用户状态
    async initializeUser() {
      if (this.token && !this.user) {
        await this.fetchUserInfo();
      }
    }
  }
});