import request from './request';

// 商品相关API接口
export const itemAPI = {
  // 获取商品列表
  getItems: (params?: {
    page?: number;
    pageSize?: number;
    category?: string;
    keyword?: string;
    priceMin?: number;
    priceMax?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    status?: string;
    transaction_type?: 'sale' | 'rent';
  }) => {
    return request.get('/items', { params });
  },

  // 获取商品详情
  getItemDetail: (id: string) => {
    return request.get(`/items/${id}`);
  },

  // 创建商品
  createItem: (itemData: {
    title: string;
    description: string;
    price?: number;
    originalPrice?: number;
    categoryId: string;
    tags?: string[];
    images: string[];
    location?: string;
    status?: string;
    // 租赁相关字段
    transaction_type?: 'sale' | 'rent';
    rental_price_day?: number;
    rental_price_week?: number;
    rental_price_month?: number;
    deposit?: number;
    max_rental_days?: number;
  }) => {
    return request.post('/items', itemData);
  },

  // 更新商品
  updateItem: (id: string, itemData: {
    title?: string;
    description?: string;
    price?: number;
    originalPrice?: number;
    categoryId?: string;
    tags?: string[];
    images?: string[];
    location?: string;
    status?: string;
    // 租赁相关字段
    transaction_type?: 'sale' | 'rent';
    rental_price_day?: number;
    rental_price_week?: number;
    rental_price_month?: number;
    deposit?: number;
    max_rental_days?: number;
  }) => {
    return request.put(`/items/${id}`, itemData);
  },

  // 删除商品
  deleteItem: (id: string) => {
    return request.delete(`/items/${id}`);
  },

  // 获取我的商品
  getMyItems: (params?: {
    page?: number;
    pageSize?: number;
    status?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    return request.get('/items/my', { params });
  },

  // 收藏商品
  favoriteItem: (id: string) => {
    return request.post(`/items/${id}/favorite`);
  },

  // 取消收藏商品
  unfavoriteItem: (id: string) => {
    return request.delete(`/items/${id}/favorite`);
  },

  // 获取收藏商品列表
  getFavoriteItems: (params?: {
    page?: number;
    pageSize?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    return request.get('/items/favorites', { params });
  },

  // 浏览商品
  viewItem: (id: string) => {
    return request.post(`/items/${id}/view`);
  },

  // 获取商品分类
  getCategories: () => {
    return request.get('/items/categories');
  },

  // 搜索商品
  searchItems: (params: {
    keyword: string;
    page?: number;
    pageSize?: number;
    category?: string;
    priceMin?: number;
    priceMax?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    transaction_type?: 'sale' | 'rent';
  }) => {
    return request.get('/items/search', { params });
  },

  // 上传商品图片
  uploadItemImages: (formData: FormData) => {
    return request.post('/items/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 获取热门商品
  getHotItems: (params?: { limit?: number }) => {
    return request.get('/items/hot', { params });
  },

  // 获取最新求购
  getLatestRequests: (params?: { limit?: number }) => {
    return request.get('/requests/latest', { params });
  },

  // 获取热门比价任务
  getHotCompareTasks: (params?: { limit?: number }) => {
    // 强制使用直接URL拼接，避免任何axios参数处理问题
    return request.get('/compare/tasks/hot?limit=4');
  },

  // 获取平台统计数据
  getPlatformStats: () => {
    return request.get('/items/platform/stats');
  },

  // 获取新品上架
  getNewItems: (limit?: number) => {
    return request.get('/items/new', { params: { limit } });
  },

  // 获取推荐商品
  getRecommendedItems: (limit?: number) => {
    return request.get('/items/recommended', { params: { limit } });
  },

  // 获取商品评论
  getItemComments: (id: string, params?: {
    page?: number;
    pageSize?: number;
  }) => {
    return request.get(`/items/${id}/comments`, { params });
  },

  // 添加商品评论
  addItemComment: (id: string, commentData: {
    content: string;
    rating: number;
  }) => {
    return request.post(`/items/${id}/comments`, commentData);
  },

  // 举报商品
  reportItem: (id: string, reportData: {
    reason: string;
    description?: string;
  }) => {
    return request.post(`/items/${id}/report`, reportData);
  },

  // 分享商品
  shareItem: (id: string) => {
    return request.post(`/items/${id}/share`);
  }
};

export default itemAPI;

// 导出单独的函数以便直接使用
export const getItems = itemAPI.getItems;
export const getItemDetail = itemAPI.getItemDetail;
export const createItem = itemAPI.createItem;
export const updateItem = itemAPI.updateItem;
export const deleteItem = itemAPI.deleteItem;
export const getMyItems = itemAPI.getMyItems;
export const favoriteItem = itemAPI.favoriteItem;
export const unfavoriteItem = itemAPI.unfavoriteItem;
export const getFavoriteItems = itemAPI.getFavoriteItems;
export const viewItem = itemAPI.viewItem;
export const getCategories = itemAPI.getCategories;
export const getItemComments = itemAPI.getItemComments;
export const addItemComment = itemAPI.addItemComment;
export const reportItem = itemAPI.reportItem;
export const shareItem = itemAPI.shareItem;
export const searchItems = itemAPI.searchItems;
export const getRecommendedItems = itemAPI.getRecommendedItems;
export const getHotItems = itemAPI.getHotItems;
export const getLatestRequests = itemAPI.getLatestRequests;
export const getHotCompareTasks = itemAPI.getHotCompareTasks;
export const getPlatformStats = itemAPI.getPlatformStats;