<template>
  <div class="item-card">
    <!-- 商品图片 -->
    <div class="item-image-container">
      <router-link :to="`/items/${item.id}`" class="item-image-link">
        <img :src="item.images?.[0] || defaultImage" :alt="item.title" class="item-image" />
      </router-link>
      <!-- 商品状态标签 -->
      <div class="item-status" v-if="item.status">
        {{ getStatusText(item.status) }}
      </div>
      <!-- 收藏按钮 -->
      <button class="favorite-btn" @click.stop="toggleFavorite" :class="{ active: item.isFavorite }">
        <i class="el-icon-star-off"></i>
      </button>
    </div>
    
    <!-- 商品信息 -->
    <div class="item-info">
      <h3 class="item-title">
        <router-link :to="`/items/${item.id}`" :title="item.title" class="item-title-link">
          {{ item.title }}
        </router-link>
      </h3>
      
      <!-- 商品标签 -->
      <div class="item-tags" v-if="item.tags && item.tags.length > 0">
        <span v-for="(tag, index) in item.tags.slice(0, 3)" :key="index" class="item-tag">
          {{ tag }}
        </span>
      </div>
      
      <!-- 价格和卖家信息 -->
      <div class="item-meta">
        <div class="item-price">¥{{ item.price }}</div>
        <div class="item-seller">
          <img :src="item.seller?.avatar || defaultAvatar" :alt="item.seller?.nickname" class="seller-avatar" />
          <span class="seller-name">{{ item.seller?.nickname || '匿名用户' }}</span>
        </div>
      </div>
      
      <!-- 商品统计信息 -->
      <div class="item-stats">
        <span class="stat-item">
          <i class="el-icon-eye"></i> {{ item.views || 0 }}
        </span>
        <span class="stat-item">
          <i class="el-icon-chat-dot-square"></i> {{ item.comments || 0 }}
        </span>
        <span class="stat-item">
          <i class="el-icon-time"></i> {{ formatTime(item.createdAt) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

// 商品数据类型定义
interface Item {
  id: string;
  title: string;
  price: number;
  images?: string[];
  status: 'new' | 'used' | 'like_new' | 'excellent' | 'good';
  tags?: string[];
  views?: number;
  comments?: number;
  createdAt: string;
  isFavorite?: boolean;
  seller?: {
    id: string;
    nickname: string;
    avatar?: string;
  };
}

// 组件属性
interface Props {
  item: Item;
}

// 定义组件属性
const props = defineProps<Props>();

// 路由实例
const router = useRouter();

// 默认图片
const defaultImage = 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg';
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';

// 获取状态文本
const getStatusText = (status: string): string => {
  const statusMap: Record<string, string> = {
    'new': '全新',
    'used': '使用过',
    'like_new': '九成新',
    'excellent': '八成新',
    'good': '七成新'
  };
  return statusMap[status] || status;
};

// 格式化时间
const formatTime = (timeString: string): string => {
  const now = new Date();
  const time = new Date(timeString);
  const diff = now.getTime() - time.getTime();
  const minutes = Math.floor(diff / 1000 / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  
  if (minutes < 60) {
    return `${minutes}分钟前`;
  } else if (hours < 24) {
    return `${hours}小时前`;
  } else if (days < 30) {
    return `${days}天前`;
  } else {
    return time.toLocaleDateString();
  }
};

// 切换收藏状态
const toggleFavorite = () => {
  // 这里应该调用API切换收藏状态
  // 模拟收藏功能
  const isLoggedIn = true; // 实际应该从用户状态管理中获取
  
  if (!isLoggedIn) {
    ElMessage.warning('请先登录');
    router.push('/login');
    return;
  }
  
  // 在实际应用中，这里应该调用API
  // 这里仅做前端模拟
  const newFavoriteState = !props.item.isFavorite;
  ElMessage.success(newFavoriteState ? '收藏成功' : '取消收藏');
};
</script>

<style lang="scss" scoped>
.item-card {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.item-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* 商品图片容器 */
.item-image-container {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.item-card:hover .item-image {
  transform: scale(1.05);
}

/* 商品状态标签 */
.item-status {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: #409eff;
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  z-index: 10;
}

/* 收藏按钮 */
.favorite-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 32px;
  height: 32px;
  border: none;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #999;
  transition: all 0.3s ease;
  z-index: 10;
}

.favorite-btn:hover {
  background-color: #fff;
  color: #f56c6c;
}

.favorite-btn.active {
  background-color: #fef0f0;
  color: #f56c6c;
}

/* 商品信息 */
.item-info {
  padding: 16px;
}

/* 商品标题 */
.item-title {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 500;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.item-title-link {
  color: #333;
  text-decoration: none;
  transition: color 0.3s ease;
}

.item-title-link:hover {
  color: #409eff;
}

/* 商品标签 */
.item-tags {
  margin-bottom: 12px;
}

.item-tag {
  display: inline-block;
  margin-right: 8px;
  margin-bottom: 4px;
  padding: 2px 8px;
  background-color: #f0f9ff;
  color: #409eff;
  border-radius: 12px;
  font-size: 12px;
}

/* 商品元信息 */
.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.item-price {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}

.item-seller {
  display: flex;
  align-items: center;
}

.seller-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 6px;
}

.seller-name {
  font-size: 12px;
  color: #999;
  max-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 商品统计信息 */
.item-stats {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-item i {
  margin-right: 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .item-image-container {
    height: 180px;
  }
  
  .item-title {
    font-size: 15px;
  }
  
  .item-price {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .item-image-container {
    height: 160px;
  }
  
  .item-info {
    padding: 12px;
  }
  
  .item-title {
    font-size: 14px;
  }
  
  .item-price {
    font-size: 15px;
  }
  
  .item-stats {
    font-size: 11px;
  }
}
</style>