import request from './request';

// 求购相关API接口
export const requestItemAPI = {
  // 获取求购列表
  getRequests: (params?: {
    page?: number;
    pageSize?: number;
    category?: string;
    keyword?: string;
    priceMin?: number;
    priceMax?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    status?: string;
  }) => {
    return request.get('/requests', { params });
  },

  // 获取求购详情
  getRequestDetail: (id: string) => {
    return request.get(`/requests/${id}`);
  },

  // 点赞求购评论
  likeComment: (commentId: string) => {
    return request.post(`/request-comments/${commentId}/like`);
  },

  // 获取相关求购
  getRelatedRequests: (id: string, params?: {
    page?: number;
    pageSize?: number;
  }) => {
    return request.get(`/requests/${id}/related`, { params });
  },

  // 举报求购
  reportRequest: (id: string, reportData: {
    type: string;
    description: string;
  }) => {
    return request.post(`/requests/${id}/report`, reportData);
  },

  // 获取联系方式
  getContactInfo: (id: string) => {
    return request.get(`/requests/${id}/contact`);
  },

  // 获取求购评论
  getComments: (id: string, params?: {
    page?: number;
    pageSize?: number;
  }) => {
    return request.get(`/requests/${id}/comments`, { params });
  },

  // 提交求购评论
  submitComment: (id: string, commentData: {
    content: string;
  }) => {
    return request.post(`/requests/${id}/comments`, commentData);
  },

  // 创建求购
  createRequest: (requestData: {
    title: string;
    description: string;
    priceRange?: {
      min: number;
      max: number;
    };
    categoryId: string;
    tags?: string[];
    images?: string[];
    location?: string;
    status?: string;
  }) => {
    return request.post('/requests', requestData);
  },

  // 更新求购
  updateRequest: (id: string, requestData: {
    title?: string;
    description?: string;
    priceRange?: {
      min: number;
      max: number;
    };
    categoryId?: string;
    tags?: string[];
    images?: string[];
    location?: string;
    status?: string;
  }) => {
    return request.put(`/requests/${id}`, requestData);
  },

  // 删除求购
  deleteRequest: (id: string) => {
    return request.delete(`/requests/${id}`);
  },

  // 获取我的求购
  getMyRequests: (params?: {
    page?: number;
    pageSize?: number;
    status?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    return request.get('/requests/my', { params });
  },

  // 收藏求购
  favoriteRequest: (id: string) => {
    return request.post(`/requests/${id}/favorite`);
  },

  // 取消收藏求购
  unfavoriteRequest: (id: string) => {
    return request.delete(`/requests/${id}/favorite`);
  },

  // 获取收藏求购列表
  getFavoriteRequests: (params?: {
    page?: number;
    pageSize?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }) => {
    return request.get('/requests/favorites', { params });
  },

  // 浏览求购
  viewRequest: (id: string) => {
    return request.post(`/requests/${id}/view`);
  },

  // 搜索求购
  searchRequests: (keyword: string, params?: {
    page?: number;
    pageSize?: number;
    category?: string;
    priceMin?: number;
    priceMax?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    status?: string;
  }) => {
    return request.get(`/requests/search?q=${keyword}`, { params });
  }
};

export default requestItemAPI;
// 导出单独的函数以便直接使用
export const getRequestItemList = requestItemAPI.getRequests;
export const getRequestItemDetail = requestItemAPI.getRequestDetail;
export const createRequestItem = requestItemAPI.createRequest;
export const updateRequestItem = requestItemAPI.updateRequest;
export const deleteRequestItem = requestItemAPI.deleteRequest;
export const getMyRequestItems = requestItemAPI.getMyRequests;
export const toggleFavoriteRequest = requestItemAPI.favoriteRequest;
export const searchRequestItems = requestItemAPI.searchRequests;
export const likeRequestItemComment = requestItemAPI.likeComment;
export const getRelatedRequestItems = requestItemAPI.getRelatedRequests;
export const reportRequestItem = requestItemAPI.reportRequest;
export const getContactInfo = requestItemAPI.getContactInfo;
export const getRequestItemComments = requestItemAPI.getComments;
export const submitRequestItemComment = requestItemAPI.submitComment;