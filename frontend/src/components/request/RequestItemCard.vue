<template>
  <div class="request-card">
    <!-- 求购信息头部 -->
    <div class="request-header">
      <div class="request-category" v-if="request.category">
        {{ request.category }}
      </div>
      <!-- 紧急程度标签 -->
      <div class="request-urgency" v-if="request.urgency">
        {{ getUrgencyText(request.urgency) }}
      </div>
    </div>
    
    <!-- 求购信息内容 -->
    <div class="request-content">
      <h3 class="request-title">
        <router-link :to="`/requests/${request.id}`" :title="request.title" class="request-title-link">
          {{ request.title }}
        </router-link>
      </h3>
      
      <!-- 求购描述 -->
      <p class="request-description" v-if="request.description">
        {{ request.description }}
      </p>
      
      <!-- 求购条件 -->
      <div class="request-conditions" v-if="hasConditions">
        <div class="condition-item" v-if="request.maxPrice">
          <i class="el-icon-money"></i>
          <span>最高出价：¥{{ request.maxPrice }}</span>
        </div>
        <div class="condition-item" v-if="request.expectedCondition">
          <i class="el-icon-goods"></i>
          <span>期望成色：{{ getConditionText(request.expectedCondition) }}</span>
        </div>
        <div class="condition-item" v-if="request.expectedTime">
          <i class="el-icon-time"></i>
          <span>期望时间：{{ request.expectedTime }}</span>
        </div>
      </div>
      
      <!-- 求购标签 -->
      <div class="request-tags" v-if="request.tags && request.tags.length > 0">
        <span v-for="(tag, index) in request.tags.slice(0, 3)" :key="index" class="request-tag">
          {{ tag }}
        </span>
      </div>
    </div>
    
    <!-- 求购信息底部 -->
    <div class="request-footer">
      <!-- 发布者信息 -->
      <div class="request-publisher">
        <img :src="request.publisher?.avatar || defaultAvatar" :alt="request.publisher?.nickname" class="publisher-avatar" />
        <span class="publisher-name">{{ request.publisher?.nickname || '匿名用户' }}</span>
      </div>
      
      <!-- 统计信息 -->
      <div class="request-stats">
        <span class="stat-item">
          <i class="el-icon-eye"></i> {{ request.views || 0 }}
        </span>
        <span class="stat-item">
          <i class="el-icon-comment"></i> {{ request.responses || 0 }}
        </span>
        <span class="stat-item">
          <i class="el-icon-time"></i> {{ formatTime(request.createdAt) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// 求购信息类型定义
interface RequestItem {
  id: string;
  title: string;
  description?: string;
  category?: string;
  maxPrice?: number;
  expectedCondition?: 'new' | 'like_new' | 'excellent' | 'good' | 'used';
  expectedTime?: string;
  urgency?: 'normal' | 'urgent' | 'very_urgent';
  tags?: string[];
  views?: number;
  responses?: number;
  createdAt: string;
  publisher?: {
    id: string;
    nickname: string;
    avatar?: string;
  };
}

// 组件属性
interface Props {
  request: RequestItem;
}

// 定义组件属性
const props = defineProps<Props>();

// 默认头像
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';

// 计算属性：是否有求购条件
const hasConditions = computed(() => {
  const { maxPrice, expectedCondition, expectedTime } = props.request;
  return maxPrice !== undefined || expectedCondition !== undefined || expectedTime !== undefined;
});

// 获取紧急程度文本
const getUrgencyText = (urgency: string): string => {
  const urgencyMap: Record<string, string> = {
    'normal': '普通',
    'urgent': '紧急',
    'very_urgent': '非常紧急'
  };
  return urgencyMap[urgency] || urgency;
};

// 获取成色文本
const getConditionText = (condition: string): string => {
  const conditionMap: Record<string, string> = {
    'new': '全新',
    'like_new': '九成新',
    'excellent': '八成新',
    'good': '七成新',
    'used': '使用过'
  };
  return conditionMap[condition] || condition;
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
</script>

<style lang="scss" scoped>
.request-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.request-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* 求购信息头部 */
.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.request-category {
  background-color: #e6f7ff;
  color: #1890ff;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.request-urgency {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.request-urgency:contains('普通') {
  background-color: #f0f9ff;
  color: #409eff;
}

.request-urgency:contains('紧急') {
  background-color: #fff7e6;
  color: #e6a23c;
}

.request-urgency:contains('非常紧急') {
  background-color: #fef0f0;
  color: #f56c6c;
}

/* 求购信息内容 */
.request-content {
  margin-bottom: 15px;
}

/* 求购标题 */
.request-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 500;
  line-height: 1.4;
  color: #333;
}

.request-title-link {
  color: #333;
  text-decoration: none;
  transition: color 0.3s ease;
}

.request-title-link:hover {
  color: #409eff;
}

/* 求购描述 */
.request-description {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* 求购条件 */
.request-conditions {
  margin-bottom: 12px;
}

.condition-item {
  display: flex;
  align-items: center;
  margin-bottom: 6px;
  font-size: 14px;
  color: #666;
}

.condition-item i {
  margin-right: 8px;
  color: #409eff;
  width: 16px;
  text-align: center;
}

/* 求购标签 */
.request-tags {
  margin-bottom: 10px;
}

.request-tag {
  display: inline-block;
  margin-right: 8px;
  margin-bottom: 4px;
  padding: 2px 8px;
  background-color: #f5f5f5;
  color: #666;
  border-radius: 12px;
  font-size: 12px;
}

/* 求购信息底部 */
.request-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

/* 发布者信息 */
.request-publisher {
  display: flex;
  align-items: center;
}

.publisher-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 8px;
}

.publisher-name {
  font-size: 14px;
  color: #666;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 统计信息 */
.request-stats {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #999;
}

.stat-item {
  display: flex;
  align-items: center;
  margin-left: 12px;
}

.stat-item i {
  margin-right: 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .request-card {
    padding: 16px;
  }
  
  .request-title {
    font-size: 16px;
  }
  
  .condition-item {
    font-size: 13px;
  }
  
  .request-footer {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .request-stats {
    margin-top: 10px;
  }
  
  .stat-item {
    margin-left: 0;
    margin-right: 12px;
  }
}

@media (max-width: 480px) {
  .request-card {
    padding: 12px;
  }
  
  .request-title {
    font-size: 15px;
  }
  
  .request-description {
    font-size: 13px;
  }
  
  .condition-item {
    font-size: 12px;
  }
  
  .request-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .request-urgency {
    margin-top: 6px;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.request-card {
  animation: fadeIn 0.3s ease-out;
}
</style>