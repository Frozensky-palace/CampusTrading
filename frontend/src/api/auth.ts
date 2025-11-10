import request from './request';

// 单独导出登录函数，供Login.vue使用
export const login = (username: string, password: string) => {
  // 后端登录API需要email参数，但前端使用username
  return request.post('/user/login', { email: username, password });
};

// 单独导出注册函数，供Register.vue使用
export const register = (userData: { username: string; password: string; email: string; student_id?: string }) => {
  // 确保有student_id参数
  const data = {
    ...userData,
    student_id: userData.student_id || userData.email.split('@')[0]
  };
  return request.post('/user/register', data);
};

// 认证相关API接口
export const authAPI = {
  // 用户登录
  login: (credentials: {
    username: string;
    password: string;
  }) => {
    return request.post('/auth/login', credentials);
  },

  // 用户注册
  register: (userData: {
    username: string;
    password: string;
    nickname: string;
    email: string;
    phone: string;
  }) => {
    return request.post('/auth/register', userData);
  },

  // 用户登出
  logout: () => {
    return request.post('/auth/logout');
  },

  // 获取当前用户信息
  getCurrentUser: () => {
    return request.get('/users/me');
  },

  // 更新用户信息
  updateUserInfo: (userData: {
    nickname?: string;
    avatar?: string;
    email?: string;
    phone?: string;
  }) => {
    return request.put('/users/me', userData);
  },

  // 修改密码
  changePassword: (passwordData: {
    currentPassword: string;
    newPassword: string;
    confirmPassword: string;
  }) => {
    return request.put('/users/me/password', passwordData);
  },

  // 忘记密码
  forgotPassword: (email: string) => {
    return request.post('/auth/forgot-password', { email });
  },

  // 重置密码
  resetPassword: (resetData: {
    token: string;
    newPassword: string;
    confirmPassword: string;
  }) => {
    return request.post('/auth/reset-password', resetData);
  },

  // 发送验证码
  sendVerificationCode: (email: string) => {
    return request.post('/auth/send-verification-code', { email });
  },

  // 验证邮箱
  verifyEmail: (token: string) => {
    return request.post('/auth/verify-email', { token });
  },

  // 刷新token
  refreshToken: (refreshToken: string) => {
    return request.post('/auth/refresh-token', { refreshToken });
  },

  // 第三方登录 - 微信
  wechatLogin: (code: string) => {
    return request.post('/auth/wechat-login', { code });
  },

  // 第三方登录 - QQ
  qqLogin: (code: string) => {
    return request.post('/auth/qq-login', { code });
  },

  // 第三方登录 - 微博
  weiboLogin: (code: string) => {
    return request.post('/auth/weibo-login', { code });
  }
};

export default authAPI;