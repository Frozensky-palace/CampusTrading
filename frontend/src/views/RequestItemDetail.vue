<template>
  <div class="request-item-detail-container">
    <!-- 面包屑导航 -->
    <div class="breadcrumb">
      <el-breadcrumb separator="/">{{ breadcrumbItems }}</el-breadcrumb>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 左侧内容 -->
      <div class="left-content">
        <!-- 求购信息卡片 -->
        <el-card class="request-item-card">
          <div class="request-item-header">
            <h1 class="request-item-title">{{ requestItem.title }}</h1>
            <span class="price-tag">{{ $t('request.detail.maxOffer') }}￥{{ formatPrice(requestItem.maxPrice) }}</span>
          </div>

          <!-- 求购基本信息 -->
          <div class="request-item-info">
            <div class="info-row">
              <span class="info-label">{{ $t('request.detail.category') }}</span>
              <span class="info-value">{{ getCategoryName(requestItem.category) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">{{ $t('request.detail.publishTime') }}</span>
              <span class="info-value">{{ formatTime(requestItem.createdAt) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">{{ $t('request.detail.location') }}</span>
              <span class="info-value">{{ requestItem.location }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">{{ $t('request.detail.status') }}</span>
              <span class="info-value status-badge" :class="getStatusClass(requestItem.status)">
                {{ getStatusText(requestItem.status) }}
              </span>
            </div>
            <div class="info-row">
              <span class="info-label">{{ $t('request.detail.viewCount') }}</span>
              <span class="info-value">{{ requestItem.viewCount || 0 }}</span>
            </div>
          </div>

          <!-- 商品标签 -->
          <div class="tags-container" v-if="requestItem.tags && requestItem.tags.length > 0">
            <span class="tags-label">{{ $t('request.detail.relatedTags') }}</span>
            <el-tag
              v-for="tag in requestItem.tags"
              :key="tag"
              type="info"
              effect="plain"
              @click="searchByTag(tag)"
              class="clickable-tag"
            >
              {{ tag }}
            </el-tag>
          </div>

          <!-- 求购描述 -->
          <div class="request-item-description">
            <h3>{{ $t('request.detail.description') }}</h3>
            <div class="description-content" v-html="formatDescription(requestItem.description)"></div>
          </div>

          <!-- 联系方式 -->
          <div v-if="requestItem.status === 'active'" class="contact-section">
            <h3>{{ $t('request.detail.contactInfo') }}</h3>
            <div class="contact-info">
              <p class="contact-hint">{{ $t('request.detail.contactHint') }}</p>
              <el-button type="primary" icon="el-icon-phone" @click="showContactInfo">
                {{ $t('request.detail.viewContact') }}
              </el-button>
            </div>
          </div>

          <!-- 状态提示 -->
          <div v-else-if="requestItem.status === 'completed'" class="status-notice completed">
            <i class="el-icon-success"></i>
            <span>{{ $t('request.detail.completedNotice') }}</span>
          </div>

          <div v-else-if="requestItem.status === 'cancelled'" class="status-notice cancelled">
            <i class="el-icon-error"></i>
            <span>{{ $t('request.detail.cancelledNotice') }}</span>
          </div>

          <!-- 操作按钮 -->
          <div class="action-buttons" v-if="isOwner">
            <el-button type="primary" @click="editRequestItem">{{ $t('request.detail.editRequest') }}</el-button>
            <el-button type="success" v-if="requestItem.status === 'active'" @click="markAsCompleted">{{ $t('request.detail.markComplete') }}</el-button>
            <el-button type="danger" v-if="requestItem.status === 'active'" @click="cancelRequestItem">{{ $t('request.detail.cancelRequest') }}</el-button>
          </div>
        </el-card>

        <!-- 评论区域 -->
        <el-card class="comments-section" v-if="requestItem.status !== 'cancelled'">
          <div class="comments-header">
            <h3>{{ $t('request.detail.commentsSection') }}</h3>
            <span class="comment-count">({{ comments.length }}{{ $t('request.detail.commentsCount') }})</span>
          </div>

          <!-- 评论输入 -->
          <div class="comment-input-section" v-if="!isAnonymous">
            <el-input
              v-model="commentContent"
              type="textarea"
              :placeholder="$t('request.detail.commentPlaceholder')"
              :rows="3"
              maxlength="500"
              show-word-limit
            >
              <template #append>
                <el-button type="primary" @click="submitComment">{{ $t('request.detail.submitComment') }}</el-button>
              </template>
            </el-input>
          </div>

          <!-- 未登录提示 -->
          <div v-else class="login-tip">
            <p>{{ $t('request.detail.loginHint1') }}<a href="/login" class="login-link">{{ $t('request.detail.loginLink') }}</a>{{ $t('request.detail.loginHint2') }}</p>
          </div>

          <!-- 评论列表 -->
          <div class="comments-list" v-if="comments.length > 0">
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <div class="comment-header">
                <img
                  v-if="comment.avatar"
                  :src="comment.avatar"
                  :alt="$t('request.detail.userAvatar')"
                  class="user-avatar"
                />
                <div v-else class="user-avatar placeholder">{{ comment.userName?.substring(0, 2) || $t('request.detail.user') }}</div>
                <div class="comment-info">
                  <div class="user-name">{{ comment.userName || $t('request.detail.anonymousUser') }}</div>
                  <div class="comment-time">{{ formatTime(comment.createdAt) }}</div>
                </div>
                <div v-if="comment.isOwner" class="owner-badge">{{ $t('request.detail.publisher') }}</div>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
              <div class="comment-actions">
                <el-button type="text" size="small" @click="likeComment(comment.id)">
                  <i class="el-icon-like" :class="{ liked: isLiked(comment.id) }"></i>
                  <span>{{ comment.likeCount || 0 }}</span>
                </el-button>
                <el-button type="text" size="small" @click="replyComment(comment.id)">{{ $t('request.detail.reply') }}</el-button>
              </div>
            </div>
          </div>

          <!-- 无评论提示 -->
          <div v-else class="no-comments">
            <p>{{ $t('request.detail.noComments') }}</p>
          </div>

          <!-- 加载更多 -->
          <div v-if="hasMoreComments" class="load-more">
            <el-button type="text" @click="loadMoreComments">{{ $t('request.detail.loadMoreComments') }}</el-button>
          </div>
        </el-card>
      </div>

      <!-- 右侧边栏 -->
      <div class="right-sidebar">
        <!-- 发布者信息 -->
        <el-card class="publisher-info">
          <div class="publisher-header">
            <img
              v-if="requestItem.userAvatar"
              :src="requestItem.userAvatar"
              :alt="$t('request.detail.userAvatar')"
              class="publisher-avatar"
            />
            <div v-else class="publisher-avatar placeholder">{{ requestItem.userName?.substring(0, 2) || $t('request.detail.user') }}</div>
            <div class="publisher-details">
              <div class="publisher-name">{{ requestItem.userName || $t('request.detail.anonymousUser') }}</div>
              <div class="publisher-level">{{ $t('request.detail.reputationLevel') }}{{ getReputationLevel(requestItem.userReputation || 0) }}</div>
            </div>
          </div>
          <div class="publisher-stats">
            <div class="stat-item">
              <span class="stat-label">{{ $t('request.detail.publishedRequests') }}</span>
              <span class="stat-value">{{ requestItem.userRequestCount || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">{{ $t('request.detail.completed') }}</span>
              <span class="stat-value">{{ requestItem.userCompletedCount || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">{{ $t('request.detail.positiveRate') }}</span>
              <span class="stat-value">{{ requestItem.userRating || 100 }}%</span>
            </div>
          </div>
          <div v-if="!isOwner && requestItem.status === 'active'" class="publisher-actions">
            <el-button type="primary" full-width @click="sendMessage">{{ $t('request.detail.sendMessage') }}</el-button>
            <el-button type="default" full-width @click="showContactInfo">{{ $t('request.detail.viewContact') }}</el-button>
          </div>
        </el-card>

        <!-- 相关推荐 -->
        <el-card class="related-requests">
          <h3 class="card-title">{{ $t('request.detail.relatedRequests') }}</h3>
          <div class="related-list">
            <div
              v-for="item in relatedRequests"
              :key="item.id"
              class="related-item"
              @click="viewOtherDetail(item.id)"
            >
              <h4 class="related-title">{{ truncateText(item.title, 30) }}</h4>
              <div class="related-info">
                <span class="related-price">￥{{ formatPrice(item.maxPrice) }}</span>
                <span class="related-time">{{ formatTime(item.createdAt, 'relative') }}</span>
              </div>
            </div>
          </div>
          <div class="view-more">
            <el-button type="text" @click="viewMoreRelated">{{ $t('request.detail.viewMore') }}</el-button>
          </div>
        </el-card>

        <!-- 平台提示 -->
        <el-card class="platform-tips">
          <h3 class="card-title">{{ $t('request.detail.safetyTips') }}</h3>
          <ul class="tips-list">
            <li>{{ $t('request.detail.tip1') }}</li>
            <li>{{ $t('request.detail.tip2') }}</li>
            <li>{{ $t('request.detail.tip3') }}</li>
            <li>{{ $t('request.detail.tip4') }}</li>
          </ul>
        </el-card>
      </div>
    </div>

    <!-- 举报弹窗 -->
    <el-dialog v-model="reportDialogVisible" :title="$t('request.detail.reportDialogTitle')" width="500px">
      <div class="report-form">
        <el-form :model="reportForm" :rules="reportRules" ref="reportFormRef">
          <el-form-item :label="$t('request.detail.reportType')" prop="type">
            <el-select v-model="reportForm.type" :placeholder="$t('request.detail.selectReportType')">
              <el-option :label="$t('request.detail.reportFake')" value="fake"></el-option>
              <el-option :label="$t('request.detail.reportProhibited')" value="prohibited"></el-option>
              <el-option :label="$t('request.detail.reportHarassment')" value="harassment"></el-option>
              <el-option :label="$t('request.detail.reportOther')" value="other"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="$t('request.detail.reportDescription')" prop="description">
            <el-input
              v-model="reportForm.description"
              type="textarea"
              :placeholder="$t('request.detail.reportDescPlaceholder')"
              :rows="4"
              maxlength="500"
              show-word-limit
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="reportDialogVisible = false">{{ $t('common.cancel') }}</el-button>
        <el-button type="primary" @click="submitReport">{{ $t('request.detail.submitReport') }}</el-button>
      </template>
    </el-dialog>

    <!-- 联系方式弹窗 -->
    <el-dialog v-model="contactDialogVisible" :title="$t('request.detail.contactDialogTitle')" width="400px" :show-close="false">
      <div class="contact-dialog-content" v-if="contactInfo">
        <div class="contact-item">
          <span class="contact-label">{{ $t('request.detail.phoneNumber') }}</span>
          <span class="contact-value">{{ contactInfo.phoneNumber || $t('request.detail.notSet') }}</span>
        </div>
        <div class="contact-item">
          <span class="contact-label">{{ $t('request.detail.wechat') }}</span>
          <span class="contact-value">{{ contactInfo.wechat || $t('request.detail.notSet') }}</span>
        </div>
        <div class="contact-item">
          <span class="contact-label">{{ $t('request.detail.qq') }}</span>
          <span class="contact-value">{{ contactInfo.qq || $t('request.detail.notSet') }}</span>
        </div>
        <div class="contact-tip">
          <i class="el-icon-warning"></i>
          <span>{{ $t('request.detail.contactSafetyTip') }}</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="contactDialogVisible = false">{{ $t('common.close') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useI18n } from 'vue-i18n';
import {
  getRequestItemDetail,
  getRequestItemComments,
  submitRequestItemComment,
  likeRequestItemComment,
  getRelatedRequestItems,
  reportRequestItem,
  getContactInfo
} from '@/api/requestItem';
import {
  formatPrice,
  formatTime,
  truncateText,
  formatDescription,
  getStatusClass,
  getReputationLevel
} from '@/utils/common';
import { useUserStore } from '@/store/user';

const { t } = useI18n();

// 路由和状态管理
const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

// 请求参数
const requestItemId = route.params.id as string;

// 求购信息
const requestItem = ref<any>({});

// 评论数据
const comments = ref<any[]>([]);
const commentContent = ref('');
const hasMoreComments = ref(true);
const currentCommentPage = ref(1);

// 相关推荐
const relatedRequests = ref<any[]>([]);

// 模态框状态
const reportDialogVisible = ref(false);
const contactDialogVisible = ref(false);

// 表单引用
const reportFormRef = ref<any>();

// 举报表单数据
const reportForm = reactive({
  type: '',
  description: ''
});

// 举报表单验证规则
const reportRules = computed(() => ({
  type: [
    { required: true, message: t('request.detail.reportTypeRequired'), trigger: 'change' }
  ],
  description: [
    { required: true, message: t('request.detail.reportDescRequired'), trigger: 'blur' },
    { min: 10, max: 500, message: t('request.detail.reportDescLength'), trigger: 'blur' }
  ]
}));

// 联系方式信息
const contactInfo = ref<any>(null);

// 已点赞的评论ID列表
const likedComments = ref<Set<string>>(new Set());

// 面包屑导航
const breadcrumbItems = computed(() => [
  { path: '/', title: t('common.home') },
  { path: '/request-items', title: t('request.detail.breadcrumbRequests') },
  { title: requestItem.value.title || t('request.detail.breadcrumbDetail') }
]);

// 获取分类名称
const getCategoryName = (category: string) => {
  const categoryMap: Record<string, string> = {
    digital: t('item.categories.digital'),
    textbook: t('item.categories.textbook'),
    home: t('item.categories.home'),
    sports: t('item.categories.sports'),
    clothing: t('item.categories.clothing'),
    others: t('item.categories.others')
  };
  return categoryMap[category] || t('request.list.unknownCategory');
};

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    active: t('request.list.statusActive'),
    completed: t('request.list.statusCompleted'),
    cancelled: t('request.list.statusCancelled')
  };
  return statusMap[status] || t('request.list.unknownStatus');
};

// 判断是否为求购者本人
  const isOwner = computed(() => {
    return userStore.isLoggedIn && userStore.getUserInfo?.id === requestItem.value.userId;
  });

// 是否匿名用户
const isAnonymous = computed(() => {
  return !userStore.isLoggedIn;
});

// 加载求购详情
const loadRequestItemDetail = async () => {
  try {
    const response = await getRequestItemDetail(requestItemId);
    requestItem.value = response.data || {};
  } catch (error) {
    console.error('Failed to load request item detail:', error);
    ElMessage.error(t('request.detail.loadFailed'));
  }
};

// 加载评论
const loadComments = async (page: number = 1) => {
  try {
    const response = await getRequestItemComments(requestItemId, { page, pageSize: 10 });
    const newComments = response.data.comments || [];
    
    if (page === 1) {
      comments.value = newComments;
    } else {
      comments.value = [...comments.value, ...newComments];
    }
    
    hasMoreComments.value = newComments.length === 10;
    currentCommentPage.value = page;
  } catch (error) {
    console.error('Failed to load comments:', error);
    ElMessage.error(t('request.detail.loadCommentsFailed'));
  }
};

// 加载相关推荐
const loadRelatedRequests = async () => {
  try {
    const response = await getRelatedRequestItems(requestItemId, { page: 1, pageSize: 5 });
    relatedRequests.value = response.data.items || [];
  } catch (error) {
    console.error('Failed to load related requests:', error);
    // 错误处理可以省略，因为相关推荐不是核心功能
  }
};

// 提交评论
const submitComment = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning(t('request.detail.commentEmpty'));
    return;
  }
  
  if (!userStore.isLoggedIn) {
    ElMessage.warning(t('request.detail.loginToComment'));
    return;
  }
  
  try {
    await submitRequestItemComment(requestItemId, { content: commentContent.value.trim() });
    ElMessage.success(t('request.detail.commentSuccess'));
    commentContent.value = '';
    loadComments(1); // 重新加载评论列表
  } catch (error) {
    console.error('Failed to submit comment:', error);
    ElMessage.error(t('request.detail.commentFailed'));
  }
};

// 点赞评论
const likeComment = async (commentId: string) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning(t('request.detail.loginToLike'));
    return;
  }
  
  try {
    await likeRequestItemComment(commentId);
    
    // 更新本地点赞状态
    if (likedComments.value.has(commentId)) {
      likedComments.value.delete(commentId);
      // 减少点赞数
      const comment = comments.value.find(c => c.id === commentId);
      if (comment && comment.likeCount > 0) {
        comment.likeCount--;
      }
    } else {
      likedComments.value.add(commentId);
      // 增加点赞数
      const comment = comments.value.find(c => c.id === commentId);
      if (comment) {
        comment.likeCount = (comment.likeCount || 0) + 1;
      }
    }
  } catch (error) {
    console.error('Failed to like comment:', error);
    ElMessage.error(t('request.detail.likeFailed'));
  }
};

// 检查评论是否已点赞
const isLiked = (commentId: string) => {
  return likedComments.value.has(commentId);
};

// 回复评论
const replyComment = (commentId: string) => {
  const comment = comments.value.find(c => c.id === commentId);
  if (comment) {
    commentContent.value = `${t('request.detail.replyTo')} @${comment.userName || t('request.detail.user')}${t('request.detail.colon')}`;
    // 滚动到评论输入框
    setTimeout(() => {
      const inputElement = document.querySelector('.comment-input-section textarea');
      if (inputElement) {
        inputElement.focus();
      }
    }, 100);
  }
};

// 加载更多评论
const loadMoreComments = () => {
  if (hasMoreComments.value) {
    loadComments(currentCommentPage.value + 1);
  }
};

// 提交举报
const submitReport = async () => {
  if (!reportFormRef.value) return;
  
  try {
    await reportFormRef.value.validate();
    await reportRequestItem(requestItemId, reportForm);
    ElMessage.success(t('request.detail.reportSuccess'));
    reportDialogVisible.value = false;
    // 重置表单
    reportForm.type = '';
    reportForm.description = '';
  } catch (error: any) {
    console.error('Failed to submit report:', error);
    if (error.name !== 'validate') {
      ElMessage.error(t('request.detail.reportFailed'));
    }
  }
};

// 显示联系方式
const showContactInfo = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning(t('request.detail.loginToViewContact'));
    return;
  }
  
  try {
    const response = await getContactInfo(requestItem.value.userId);
    contactInfo.value = response.data || {};
    contactDialogVisible.value = true;
  } catch (error) {
    console.error('Failed to get contact info:', error);
    ElMessage.error(t('request.detail.getContactFailed'));
  }
};

// 发送消息
const sendMessage = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning(t('request.detail.loginToSendMessage'));
    return;
  }
  
  // 这里可以跳转到消息页面或打开消息对话框
  ElMessage.info(t('request.detail.messageFunctionDev'));
};

// 编辑求购
const editRequestItem = () => {
  router.push(`/request-items/edit/${requestItemId}`);
};

// 标记完成
const markAsCompleted = async () => {
  ElMessage.info(t('request.detail.markCompleteFunctionDev'));
  // 实际实现中需要调用API更新求购状态
};

// 取消求购
const cancelRequestItem = async () => {
  ElMessage.info(t('request.detail.cancelFunctionDev'));
  // 实际实现中需要调用API更新求购状态
};

// 查看其他求购详情
const viewOtherDetail = (id: string) => {
  router.push(`/request-items/${id}`);
};

// 查看更多相关求购
const viewMoreRelated = () => {
  router.push('/request-items');
};

// 按标签搜索
const searchByTag = (tag: string) => {
  router.push({ path: '/request-items', query: { keyword: tag } });
};

// 组件挂载时
onMounted(() => {
  loadRequestItemDetail();
  loadComments();
  loadRelatedRequests();
});
</script>

<style lang="scss" scoped>
.request-item-detail-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 面包屑导航 */
.breadcrumb {
  margin-bottom: 20px;
}

/* 主内容区域 */
.main-content {
  display: grid;
  grid-template-columns: 3fr 1fr;
  gap: 20px;
}

/* 左侧内容 */
.left-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 求购信息卡片 */
.request-item-card {
  padding: 25px;
}

.request-item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.request-item-title {
  font-size: 24px;
  font-weight: 500;
  color: #333;
  margin: 0;
  flex: 1;
  margin-right: 20px;
}

.price-tag {
  font-size: 22px;
  font-weight: bold;
  color: #ff6700;
  white-space: nowrap;
}

/* 基本信息 */
.request-item-info {
  margin-bottom: 25px;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px;
}

.info-label {
  width: 100px;
  color: #999;
}

.info-value {
  color: #333;
}

.status-badge {
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-active {
  background-color: #f0f9ff;
  color: #0369a1;
}

.status-completed {
  background-color: #f0fdf4;
  color: #15803d;
}

.status-cancelled {
  background-color: #fef2f2;
  color: #b91c1c;
}

/* 标签容器 */
.tags-container {
  margin-bottom: 25px;
  padding: 15px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.tags-label {
  font-weight: 500;
  margin-right: 10px;
  color: #666;
}

.clickable-tag {
  cursor: pointer;
}

.clickable-tag:hover {
  background-color: #409eff;
  color: white;
}

/* 求购描述 */
.request-item-description {
  margin-bottom: 25px;
}

.request-item-description h3 {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 15px;
  color: #333;
}

.description-content {
  line-height: 1.8;
  color: #666;
  white-space: pre-wrap;
}

/* 联系方式 */
.contact-section {
  margin-bottom: 25px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.contact-section h3 {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 15px;
  color: #333;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.contact-hint {
  color: #666;
  font-size: 14px;
}

/* 状态提示 */
.status-notice {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 25px;
}

.status-notice.completed {
  background-color: #f0fdf4;
  color: #15803d;
}

.status-notice.cancelled {
  background-color: #fef2f2;
  color: #b91c1c;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 15px;
}

/* 评论区域 */
.comments-section {
  padding: 25px;
}

.comments-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.comments-header h3 {
  font-size: 18px;
  font-weight: 500;
  margin: 0;
  color: #333;
}

.comment-count {
  color: #999;
  font-size: 14px;
}

/* 评论输入 */
.comment-input-section {
  margin-bottom: 30px;
}

.login-tip {
  text-align: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 30px;
}

.login-link {
  color: #409eff;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
}

/* 评论列表 */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-avatar.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #409eff;
  color: white;
  font-weight: bold;
}

.comment-info {
  flex: 1;
}

.user-name {
  font-weight: 500;
  color: #333;
  margin-bottom: 5px;
}

.comment-time {
  font-size: 12px;
  color: #999;
}

.owner-badge {
  background-color: #ff6700;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.comment-content {
  line-height: 1.6;
  color: #333;
  margin-bottom: 15px;
}

.comment-actions {
  display: flex;
  gap: 20px;
}

.comment-actions .el-button {
  padding: 0;
  font-size: 12px;
}

.liked {
  color: #ff4d4f;
}

/* 无评论提示 */
.no-comments {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

/* 加载更多 */
.load-more {
  text-align: center;
  margin-top: 20px;
}

/* 右侧边栏 */
.right-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 发布者信息 */
.publisher-info {
  padding: 20px;
}

.publisher-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.publisher-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.publisher-avatar.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #409eff;
  color: white;
  font-size: 20px;
  font-weight: bold;
}

.publisher-details {
  flex: 1;
}

.publisher-name {
  font-weight: 500;
  color: #333;
  margin-bottom: 5px;
}

.publisher-level {
  font-size: 12px;
  color: #999;
}

.publisher-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}

.publisher-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* 相关推荐 */
.related-requests {
  padding: 20px;
}

.card-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 15px;
  color: #333;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.related-item {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.related-item:hover {
  background-color: #e6f7ff;
  transform: translateX(5px);
}

.related-title {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.4;
}

.related-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.related-price {
  font-size: 14px;
  font-weight: bold;
  color: #ff6700;
}

.related-time {
  font-size: 12px;
  color: #999;
}

.view-more {
  text-align: center;
  margin-top: 15px;
}

/* 平台提示 */
.platform-tips {
  padding: 20px;
  background-color: #fff7e6;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tips-list li {
  position: relative;
  padding-left: 20px;
  margin-bottom: 10px;
  font-size: 12px;
  color: #666;
  line-height: 1.5;
}

.tips-list li:before {
  content: "•";
  position: absolute;
  left: 8px;
  color: #ff9800;
}

/* 举报弹窗 */
.report-form {
  padding: 10px 0;
}

/* 联系方式弹窗 */
.contact-dialog-content {
  padding: 20px 0;
}

.contact-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.contact-label {
  width: 100px;
  color: #666;
  font-weight: 500;
}

.contact-value {
  color: #333;
  font-weight: 500;
}

.contact-tip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background-color: #fff3cd;
  color: #856404;
  border-radius: 4px;
  margin-top: 20px;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .request-item-detail-container {
    max-width: 100%;
  }
}

@media (max-width: 992px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .right-sidebar {
    order: -1;
  }
}

@media (max-width: 768px) {
  .request-item-detail-container {
    padding: 15px;
  }
  
  .request-item-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .request-item-title {
    font-size: 20px;
  }
  
  .price-tag {
    font-size: 18px;
  }
  
  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .info-label {
    width: auto;
  }
  
  .tags-container {
    flex-direction: column;
    gap: 10px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  .comment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .publisher-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .publisher-stats {
    flex-direction: column;
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .request-item-detail-container {
    padding: 10px;
  }
  
  .request-item-card,
  .comments-section,
  .publisher-info,
  .related-requests,
  .platform-tips {
    padding: 15px;
  }
  
  .request-item-title {
    font-size: 18px;
  }
  
  .price-tag {
    font-size: 16px;
  }
  
  .request-item-description h3,
  .comments-header h3,
  .contact-section h3 {
    font-size: 16px;
  }
  
  .comment-item {
    padding: 15px;
  }
  
  .contact-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .contact-label {
    width: auto;
  }
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.request-item-card,
.comments-section,
.publisher-info,
.related-requests,
.platform-tips {
  animation: fadeInUp 0.5s ease-out;
}

.comments-section {
  animation-delay: 0.2s;
}

.publisher-info {
  animation-delay: 0.3s;
}

.related-requests {
  animation-delay: 0.4s;
}

.platform-tips {
  animation-delay: 0.5s;
}
</style>