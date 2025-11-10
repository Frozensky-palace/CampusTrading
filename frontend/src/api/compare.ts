import request from './request';

// 比价相关API接口
export const compareAPI = {
  // 获取比价任务列表
  getCompareTasks: (params?: {
    page?: number;
    pageSize?: number;
    keyword?: string;
    status?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    return request.get('/compare/tasks', { params });
  },

  // 获取比价任务详情
  getCompareTaskDetail: (id: string) => {
    return request.get(`/compare/tasks/${id}`);
  },

  // 创建比价任务
  createCompareTask: (taskData: {
    title: string;
    description?: string;
    items: Array<{
      name: string;
      price: number;
      originalPrice?: number;
      source: string;
      url?: string;
      image?: string;
      description?: string;
    }>;
    status?: string;
    public?: boolean;
  }) => {
    return request.post('/compare/tasks', taskData);
  },

  // 更新比价任务
  updateCompareTask: (id: string, taskData: {
    title?: string;
    description?: string;
    items?: Array<{
      name: string;
      price: number;
      originalPrice?: number;
      source: string;
      url?: string;
      image?: string;
      description?: string;
    }>;
    status?: string;
    public?: boolean;
  }) => {
    return request.put(`/compare/tasks/${id}`, taskData);
  },

  // 删除比价任务
  deleteCompareTask: (id: string) => {
    return request.delete(`/compare/tasks/${id}`);
  },

  // 获取我的比价任务
  getMyCompareTasks: (params?: {
    page?: number;
    pageSize?: number;
    status?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    return request.get('/compare/tasks/my', { params });
  },

  // 获取公开比价任务
  getPublicCompareTasks: (params?: {
    page?: number;
    pageSize?: number;
    keyword?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    return request.get('/compare/tasks/public', { params });
  },

  // 收藏比价任务
  favoriteCompareTask: (id: string) => {
    return request.post(`/compare/tasks/${id}/favorite`);
  },

  // 取消收藏比价任务
  unfavoriteCompareTask: (id: string) => {
    return request.delete(`/compare/tasks/${id}/favorite`);
  },

  // 获取收藏的比价任务
  getFavoriteCompareTasks: (params?: {
    page?: number;
    pageSize?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    return request.get('/compare/tasks/favorites', { params });
  },

  // 搜索比价任务
  searchCompareTasks: (params: {
    keyword: string;
    page?: number;
    pageSize?: number;
    status?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    return request.get('/compare/tasks/search', { params });
  },

  // 获取热门比价任务
  getHotCompareTasks: (limit?: number) => {
    return request.get('/compare/tasks/hot', { params: { limit } });
  },

  // 获取最新比价任务
  getNewCompareTasks: (limit?: number) => {
    return request.get('/compare/tasks/new', { params: { limit } });
  },

  // 添加比价商品
  addCompareItem: (taskId: string, itemData: {
    name: string;
    price: number;
    originalPrice?: number;
    source: string;
    url?: string;
    image?: string;
    description?: string;
  }) => {
    return request.post(`/compare/tasks/${taskId}/items`, itemData);
  },

  // 更新比价商品
  updateCompareItem: (taskId: string, itemId: string, itemData: {
    name?: string;
    price?: number;
    originalPrice?: number;
    source?: string;
    url?: string;
    image?: string;
    description?: string;
  }) => {
    return request.put(`/compare/tasks/${taskId}/items/${itemId}`, itemData);
  },

  // 删除比价商品
  deleteCompareItem: (taskId: string, itemId: string) => {
    return request.delete(`/compare/tasks/${taskId}/items/${itemId}`);
  },

  // 获取比价结果分析
  getCompareAnalysis: (taskId: string) => {
    return request.get(`/compare/tasks/${taskId}/analysis`);
  },

  // 对比两个商品
  compareTwoItems: (item1Id: string, item2Id: string) => {
    return request.get('/compare/items', { params: { item1Id, item2Id } });
  },

  // 分享比价任务
  shareCompareTask: (id: string) => {
    return request.post(`/compare/tasks/${id}/share`);
  },

  // 点赞比价任务
  likeCompareTask: (id: string) => {
    return request.post(`/compare/tasks/${id}/like`);
  },

  // 取消点赞比价任务
  unlikeCompareTask: (id: string) => {
    return request.delete(`/compare/tasks/${id}/like`);
  },

  // 获取比价任务评论
  getCompareTaskComments: (id: string, params?: {
    page?: number;
    pageSize?: number;
  }) => {
    return request.get(`/compare/tasks/${id}/comments`, { params });
  },

  // 添加比价任务评论
  addCompareTaskComment: (id: string, commentData: {
    content: string;
  }) => {
    return request.post(`/compare/tasks/${id}/comments`, commentData);
   },

  // 获取比价报价
  getCompareQuotes: (id: string, params?: {
    page?: number;
    pageSize?: number;
  }) => {
    return request.get(`/compare/tasks/${id}/quotes`, { params });
  },

  // 提交比价报价
  submitCompareQuote: (id: string, quoteData: {
    itemId: string;
    price: number;
    source: string;
    url?: string;
    description?: string;
  }) => {
    return request.post(`/compare/tasks/${id}/quotes`, quoteData);
  },

  // 点赞比价评论
  likeCompareComment: (commentId: string) => {
    return request.post(`/compare/comments/${commentId}/like`);
  }
};

export default compareAPI;

// 导出单独的函数以便直接使用
export const getCompareTaskList = compareAPI.getCompareTasks;
export const getCompareTaskDetail = compareAPI.getCompareTaskDetail;
export const getCompareComments = compareAPI.getCompareTaskComments;
export const submitCompareComment = compareAPI.addCompareTaskComment;
export const likeCompareTask = compareAPI.likeCompareTask;
export const unlikeCompareTask = compareAPI.unlikeCompareTask;
export const getCompareQuotes = compareAPI.getCompareQuotes;
export const submitCompareQuote = compareAPI.submitCompareQuote;
export const likeCompareComment = compareAPI.likeCompareComment;