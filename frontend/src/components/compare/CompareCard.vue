<template>
  <div class="compare-card">
    <!-- 比价任务头部 -->
    <div class="compare-header">
      <div class="compare-category" v-if="task.category">
        {{ task.category }}
      </div>
      <!-- 任务状态标签 -->
      <div class="compare-status" v-if="task.status">
        {{ getStatusText(task.status) }}
      </div>
    </div>
    
    <!-- 比价任务内容 -->
    <div class="compare-content">
      <h3 class="compare-title">
        <router-link :to="`/compare/${task.id}`" :title="task.title" class="compare-title-link">
          {{ task.title }}
        </router-link>
      </h3>
      
      <!-- 任务描述 -->
      <p class="compare-description" v-if="task.description">
        {{ task.description }}
      </p>
      
      <!-- 比价条件 -->
      <div class="compare-conditions" v-if="hasConditions">
        <div class="condition-item" v-if="task.budget">
          <i class="el-icon-money"></i>
          <span>{{ $t('compare.card.budget') }}{{ task.budget }}</span>
        </div>
        <div class="condition-item" v-if="task.expectedCondition">
          <i class="el-icon-goods"></i>
          <span>{{ $t('compare.card.expectedCondition') }}{{ getConditionText(task.expectedCondition) }}</span>
        </div>
        <div class="condition-item" v-if="task.expectedTime">
          <i class="el-icon-time"></i>
          <span>{{ $t('compare.card.expectedTime') }}{{ task.expectedTime }}</span>
        </div>
      </div>
      
      <!-- 比价任务标签 -->
      <div class="compare-tags" v-if="task.tags && task.tags.length > 0">
        <span v-for="(tag, index) in task.tags.slice(0, 3)" :key="index" class="compare-tag">
          {{ tag }}
        </span>
      </div>
    </div>
    
    <!-- 比价任务底部 -->
    <div class="compare-footer">
      <!-- 发布者信息 -->
      <div class="compare-publisher">
        <img :src="task.publisher?.avatar || defaultAvatar" :alt="task.publisher?.nickname" class="publisher-avatar" />
        <span class="publisher-name">{{ task.publisher?.nickname || $t('compare.card.anonymousUser') }}</span>
      </div>

      <!-- 统计信息 -->
      <div class="compare-stats">
        <span class="stat-item">
          <i class="el-icon-eye"></i> {{ task.views || 0 }}
        </span>
        <span class="stat-item">
          <i class="el-icon-comment"></i> {{ task.quotes || 0 }} {{ $t('compare.card.quotes') }}
        </span>
        <span class="stat-item">
          <i class="el-icon-time"></i> {{ formatTime(task.createdAt) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

// i18n
const { t } = useI18n();

// 比价任务类型定义
interface CompareTask {
  id: string;
  title: string;
  description?: string;
  category?: string;
  budget?: number;
  expectedCondition?: 'new' | 'like_new' | 'excellent' | 'good' | 'used';
  expectedTime?: string;
  status?: 'pending' | 'processing' | 'completed' | 'closed';
  tags?: string[];
  views?: number;
  quotes?: number;
  createdAt: string;
  publisher?: {
    id: string;
    nickname: string;
    avatar?: string;
  };
}

// 组件属性
interface Props {
  task: CompareTask;
}

// 定义组件属性
const props = defineProps<Props>();

// 默认头像
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';

// 计算属性：是否有比价条件
const hasConditions = computed(() => {
  const { budget, expectedCondition, expectedTime } = props.task;
  return budget !== undefined || expectedCondition !== undefined || expectedTime !== undefined;
});

// 获取状态文本
const getStatusText = (status: string): string => {
  const statusMap: Record<string, string> = {
    'pending': t('compare.card.statusPending'),
    'processing': t('compare.card.statusProcessing'),
    'completed': t('compare.card.statusCompleted'),
    'closed': t('compare.card.statusClosed')
  };
  return statusMap[status] || status;
};

// 获取成色文本
const getConditionText = (condition: string): string => {
  const conditionMap: Record<string, string> = {
    'new': t('compare.card.conditionNew'),
    'like_new': t('compare.card.conditionLikeNew'),
    'excellent': t('compare.card.conditionExcellent'),
    'good': t('compare.card.conditionGood'),
    'used': t('compare.card.conditionUsed')
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
    return t('compare.card.minutesAgo', { minutes });
  } else if (hours < 24) {
    return t('compare.card.hoursAgo', { hours });
  } else if (days < 30) {
    return t('compare.card.daysAgo', { days });
  } else {
    return time.toLocaleDateString();
  }
};
</script>

<style lang="scss" scoped>
.compare-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.compare-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* 比价任务头部 */
.compare-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.compare-category {
  background-color: #f0f9ff;
  color: #409eff;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.compare-status {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.compare-status:contains('待处理') {
  background-color: #f0f9ff;
  color: #409eff;
}

.compare-status:contains('处理中') {
  background-color: #f6ffed;
  color: #67c23a;
}

.compare-status:contains('已完成') {
  background-color: #f5f5f5;
  color: #909399;
}

.compare-status:contains('已关闭') {
  background-color: #fef0f0;
  color: #f56c6c;
}

/* 比价任务内容 */
.compare-content {
  margin-bottom: 15px;
}

/* 比价任务标题 */
.compare-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 500;
  line-height: 1.4;
  color: #333;
}

.compare-title-link {
  color: #333;
  text-decoration: none;
  transition: color 0.3s ease;
}

.compare-title-link:hover {
  color: #409eff;
}

/* 比价任务描述 */
.compare-description {
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

/* 比价条件 */
.compare-conditions {
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
  color: #67c23a;
  width: 16px;
  text-align: center;
}

/* 比价任务标签 */
.compare-tags {
  margin-bottom: 10px;
}

.compare-tag {
  display: inline-block;
  margin-right: 8px;
  margin-bottom: 4px;
  padding: 2px 8px;
  background-color: #f0f9ff;
  color: #409eff;
  border-radius: 12px;
  font-size: 12px;
}

/* 比价任务底部 */
.compare-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

/* 发布者信息 */
.compare-publisher {
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
.compare-stats {
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
  .compare-card {
    padding: 16px;
  }
  
  .compare-title {
    font-size: 16px;
  }
  
  .condition-item {
    font-size: 13px;
  }
  
  .compare-footer {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .compare-stats {
    margin-top: 10px;
  }
  
  .stat-item {
    margin-left: 0;
    margin-right: 12px;
  }
}

@media (max-width: 480px) {
  .compare-card {
    padding: 12px;
  }
  
  .compare-title {
    font-size: 15px;
  }
  
  .compare-description {
    font-size: 13px;
  }
  
  .condition-item {
    font-size: 12px;
  }
  
  .compare-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .compare-status {
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

.compare-card {
  animation: fadeIn 0.3s ease-out;
}
</style>