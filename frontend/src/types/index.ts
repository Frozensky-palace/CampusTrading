// 基础类型定义

// 用户类型
export interface User {
  id: string;
  username: string;
  nickname: string;
  avatar: string;
  email: string;
  phone: string;
  role: 'user' | 'admin';
  created_at: string;
  updated_at: string;
}

// 商品类型
export interface Item {
  id: string;
  title: string;
  description: string;
  price: number;
  originalPrice?: number;
  categoryId: string;
  categoryName?: string;
  tags: string[];
  images: string[];
  location?: string;
  status: 'active' | 'sold' | 'draft' | 'deleted';
  viewCount: number;
  favoriteCount: number;
  commentCount: number;
  createdAt: string;
  updatedAt: string;
  userId: string;
  user?: User;
}

// 求购类型
export interface RequestItem {
  id: string;
  title: string;
  description: string;
  priceRange?: {
    min: number;
    max: number;
  };
  categoryId: string;
  categoryName?: string;
  tags: string[];
  images: string[];
  location?: string;
  status: 'active' | 'completed' | 'cancelled' | 'deleted';
  viewCount: number;
  favoriteCount: number;
  participantCount: number;
  createdAt: string;
  updatedAt: string;
  userId: string;
  user?: User;
}

// 比价任务类型
export interface CompareTask {
  id: string;
  title: string;
  description?: string;
  items: CompareItem[];
  status: 'active' | 'completed' | 'draft' | 'deleted';
  isPublic: boolean;
  viewCount: number;
  favoriteCount: number;
  likeCount: number;
  commentCount: number;
  createdAt: string;
  updatedAt: string;
  userId: string;
  user?: User;
}

// 比价商品类型
export interface CompareItem {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  source: string;
  url?: string;
  image?: string;
  description?: string;
  taskId: string;
  createdAt: string;
  updatedAt: string;
}

// 分类类型
export interface Category {
  id: string;
  name: string;
  icon?: string;
  parentId?: string;
  children?: Category[];
  level: number;
}

// 评论类型
export interface Comment {
  id: string;
  content: string;
  rating?: number;
  targetId: string;
  targetType: 'item' | 'request' | 'compare' | 'user';
  userId: string;
  user?: User;
  parentId?: string;
  children?: Comment[];
  createdAt: string;
  updatedAt: string;
}

// 交易类型
export interface Transaction {
  id: string;
  type: 'buy' | 'sell' | 'request' | 'compare';
  itemId?: string;
  requestId?: string;
  compareTaskId?: string;
  buyerId: string;
  sellerId: string;
  amount: number;
  status: 'pending' | 'paid' | 'shipped' | 'completed' | 'cancelled' | 'refunded';
  paymentMethod?: string;
  shippingAddress?: ShippingAddress;
  paymentTime?: string;
  shippingTime?: string;
  completionTime?: string;
  createdAt: string;
  updatedAt: string;
  buyer?: User;
  seller?: User;
  item?: Item;
  request?: RequestItem;
}

// 收货地址类型
export interface ShippingAddress {
  id: string;
  userId: string;
  recipientName: string;
  phone: string;
  province: string;
  city: string;
  district: string;
  detailAddress: string;
  isDefault: boolean;
  createdAt: string;
  updatedAt: string;
}

// 消息类型
export interface Message {
  id: string;
  senderId: string;
  receiverId: string;
  content: string;
  type: 'text' | 'image' | 'system' | 'notification';
  isRead: boolean;
  relatedId?: string;
  relatedType?: 'item' | 'request' | 'transaction' | 'compare';
  createdAt: string;
  sender?: User;
  receiver?: User;
}

// 通知类型
export interface Notification {
  id: string;
  userId: string;
  title: string;
  content: string;
  type: 'system' | 'transaction' | 'message' | 'activity' | 'other';
  isRead: boolean;
  relatedId?: string;
  relatedType?: 'item' | 'request' | 'transaction' | 'compare' | 'user';
  createdAt: string;
  updatedAt: string;
}

// 举报类型
export interface Report {
  id: string;
  reporterId: string;
  targetId: string;
  targetType: 'item' | 'request' | 'user' | 'comment' | 'compare';
  reason: string;
  description?: string;
  status: 'pending' | 'processing' | 'resolved' | 'rejected';
  handledBy?: string;
  handleTime?: string;
  createdAt: string;
  updatedAt: string;
  reporter?: User;
}

// 分页结果类型
export interface PaginationResult<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// API响应类型
export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
  success: boolean;
}

// 登录凭证类型
export interface LoginCredentials {
  username: string;
  password: string;
}

// 注册信息类型
export interface RegisterInfo {
  username: string;
  password: string;
  nickname: string;
  email: string;
  phone: string;
}

// 搜索参数类型
export interface SearchParams {
  keyword?: string;
  page?: number;
  pageSize?: number;
  category?: string;
  priceMin?: number;
  priceMax?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  status?: string;
}

// 通用ID类型
export interface IdResult {
  id: string;
}

// 文件上传结果类型
export interface UploadResult {
  url: string;
  filename: string;
  size: number;
  mimeType: string;
  fileId: string;
}