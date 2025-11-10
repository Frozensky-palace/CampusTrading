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
            <span class="price-tag">最高出价：￥{{ formatPrice(requestItem.maxPrice) }}</span>
          </div>

          <!-- 求购基本信息 -->
          <div class="request-item-info">
            <div class="info-row">
              <span class="info-label">求购分类：</span>
              <span class="info-value">{{ getCategoryName(requestItem.category) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">发布时间：</span>
              <span class="info-value">{{ formatTime(requestItem.createdAt) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">交易地点：</span>
              <span class="info-value">{{ requestItem.location }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">求购状态：</span>
              <span class="info-value status-badge" :class="getStatusClass(requestItem.status)">
                {{ getStatusText(requestItem.status) }}
              </span>
            </div>
            <div class="info-row">
              <span class="info-label">浏览量：</span>
              <span class="info-value">{{ requestItem.viewCount || 0 }}</span>
            </div>
          </div>

          <!-- 商品标签 -->
          <div class="tags-container" v-if="requestItem.tags && requestItem.tags.length > 0">
            <span class="tags-label">相关标签：</span>
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
            <h3>详细描述</h3>
            <div class="description-content" v-html="formatDescription(requestItem.description)"></div>
          </div>

          <!-- 联系方式 -->
          <div v-if="requestItem.status === 'active'" class="contact-section">
            <h3>联系方式</h3>
            <div class="contact-info">
              <p class="contact-hint">为了保护您的隐私，点击下方按钮查看卖家联系方式</p>
              <el-button type="primary" icon="el-icon-phone" @click="showContactInfo">
                查看联系方式
              </el-button>
            </div>
          </div>

          <!-- 状态提示 -->
          <div v-else-if="requestItem.status === 'completed'" class="status-notice completed">
            <i class="el-icon-success"></i>
            <span>此求购信息已完成，感谢您的关注</span>
          </div>
          
          <div v-else-if="requestItem.status === 'cancelled'" class="status-notice cancelled">
            <i class="el-icon-error"></i>
            <span>此求购信息已取消</span>
          </div>

          <!-- 操作按钮 -->
          <div class="action-buttons" v-if="isOwner">
            <el-button type="primary" @click="editRequestItem">编辑求购</el-button>
            <el-button type="success" v-if="requestItem.status === 'active'" @click="markAsCompleted">标记完成</el-button>
            <el-button type="danger" v-if="requestItem.status === 'active'" @click="cancelRequestItem">取消求购</el-button>
          </div>
        </el-card>

        <!-- 评论区域 -->
        <el-card class="comments-section" v-if="requestItem.status !== 'cancelled'">
          <div class="comments-header">
            <h3>评论区</h3>
            <span class="comment-count">({{ comments.length }}条评论)</span>
          </div>

          <!-- 评论输入 -->
          <div class="comment-input-section" v-if="!isAnonymous">
            <el-input
              v-model="commentContent"
              type="textarea"
              placeholder="写下您的评论或提供相关信息..."
              :rows="3"
              maxlength="500"
              show-word-limit
            >
              <template #append>
                <el-button type="primary" @click="submitComment">发表评论</el-button>
              </template>
            </el-input>
          </div>

          <!-- 未登录提示 -->
          <div v-else class="login-tip">
            <p>请先<a href="/login" class="login-link">登录</a>后发表评论</p>
          </div>

          <!-- 评论列表 -->
          <div class="comments-list" v-if="comments.length > 0">
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <div class="comment-header">
                <img
                  v-if="comment.avatar"
                  :src="comment.avatar"
                  alt="用户头像"
                  class="user-avatar"
                />
                <div v-else class="user-avatar placeholder">{{ comment.userName?.substring(0, 2) || '用户' }}</div>
                <div class="comment-info">
                  <div class="user-name">{{ comment.userName || '匿名用户' }}</div>
                  <div class="comment-time">{{ formatTime(comment.createdAt) }}</div>
                </div>
                <div v-if="comment.isOwner" class="owner-badge">发布者</div>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
              <div class="comment-actions">
                <el-button type="text" size="small" @click="likeComment(comment.id)">
                  <i class="el-icon-like" :class="{ liked: isLiked(comment.id) }"></i>
                  <span>{{ comment.likeCount || 0 }}</span>
                </el-button>
                <el-button type="text" size="small" @click="replyComment(comment.id)">回复</el-button>
              </div>
            </div>
          </div>

          <!-- 无评论提示 -->
          <div v-else class="no-comments">
            <p>暂无评论，来发表第一条评论吧</p>
          </div>

          <!-- 加载更多 -->
          <div v-if="hasMoreComments" class="load-more">
            <el-button type="text" @click="loadMoreComments">加载更多评论</el-button>
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
              alt="用户头像"
              class="publisher-avatar"
            />
            <div v-else class="publisher-avatar placeholder">{{ requestItem.userName?.substring(0, 2) || '用户' }}</div>
            <div class="publisher-details">
              <div class="publisher-name">{{ requestItem.userName || '匿名用户' }}</div>
              <div class="publisher-level">信誉等级：{{ getReputationLevel(requestItem.userReputation || 0) }}</div>
            </div>
          </div>
          <div class="publisher-stats">
            <div class="stat-item">
              <span class="stat-label">发布求购</span>
              <span class="stat-value">{{ requestItem.userRequestCount || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">已完成</span>
              <span class="stat-value">{{ requestItem.userCompletedCount || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">好评率</span>
              <span class="stat-value">{{ requestItem.userRating || 100 }}%</span>
            </div>
          </div>
          <div v-if="!isOwner && requestItem.status === 'active'" class="publisher-actions">
            <el-button type="primary" full-width @click="sendMessage">发送消息</el-button>
            <el-button type="default" full-width @click="showContactInfo">查看联系方式</el-button>
          </div>
        </el-card>

        <!-- 相关推荐 -->
        <el-card class="related-requests">
          <h3 class="card-title">相关求购</h3>
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
            <el-button type="text" @click="viewMoreRelated">查看更多</el-button>
          </div>
        </el-card>

        <!-- 平台提示 -->
        <el-card class="platform-tips">
          <h3 class="card-title">交易安全提示</h3>
          <ul class="tips-list">
            <li>建议选择校园内公开场所进行交易</li>
            <li>请勿提前支付定金或全款</li>
            <li>仔细检查商品质量后再完成交易</li>
            <li>如遇可疑情况，请及时联系客服</li>
          </ul>
        </el-card>
      </div>
    </div>

    <!-- 举报弹窗 -->
    <el-dialog v-model="reportDialogVisible" title="举报该求购信息" width="500px">
      <div class="report-form">
        <el-form :model="reportForm" :rules="reportRules" ref="reportFormRef">
          <el-form-item label="举报类型" prop="type">
            <el-select v-model="reportForm.type" placeholder="请选择举报类型">
              <el-option label="虚假信息" value="fake"></el-option>
              <el-option label="违禁内容" value="prohibited"></el-option>
              <el-option label="骚扰信息" value="harassment"></el-option>
              <el-option label="其他问题" value="other"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="详细说明" prop="description">
            <el-input
              v-model="reportForm.description"
              type="textarea"
              placeholder="请详细描述您遇到的问题"
              :rows="4"
              maxlength="500"
              show-word-limit
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="reportDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReport">提交举报</el-button>
      </template>
    </el-dialog>

    <!-- 联系方式弹窗 -->
    <el-dialog v-model="contactDialogVisible" title="联系方式" width="400px" :show-close="false">
      <div class="contact-dialog-content" v-if="contactInfo">
        <div class="contact-item">
          <span class="contact-label">手机号码：</span>
          <span class="contact-value">{{ contactInfo.phoneNumber || '未设置' }}</span>
        </div>
        <div class="contact-item">
          <span class="contact-label">微信：</span>
          <span class="contact-value">{{ contactInfo.wechat || '未设置' }}</span>
        </div>
        <div class="contact-item">
          <span class="contact-label">QQ：</span>
          <span class="contact-value">{{ contactInfo.qq || '未设置' }}</span>
        </div>
        <div class="contact-tip">
          <i class="el-icon-warning"></i>
          <span>请保护个人信息安全，谨防诈骗</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="contactDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
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
  getCategoryName,
  getStatusText,
  getStatusClass,
  getReputationLevel
} from '@/utils/common';
import { useUserStore } from '@/store/user';

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
const reportRules = reactive({
  type: [
    { required: true, message: '请选择举报类型', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请详细说明问题', trigger: 'blur' },
    { min: 10, max: 500, message: '详细说明长度在 10 到 500 个字符', trigger: 'blur' }
  ]
});

// 联系方式信息
const contactInfo = ref<any>(null);

// 已点赞的评论ID列表
const likedComments = ref<Set<string>>(new Set());

// 面包屑导航
const breadcrumbItems = computed(() => [
  { path: '/', title: '首页' },
  { path: '/request-items', title: '求购信息' },
  { title: requestItem.value.title || '求购详情' }
]);

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
    ElMessage.error('加载求购信息失败，请稍后重试');
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
    ElMessage.error('加载评论失败，请稍后重试');
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
    ElMessage.warning('评论内容不能为空');
    return;
  }
  
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后发表评论');
    return;
  }
  
  try {
    await submitRequestItemComment(requestItemId, { content: commentContent.value.trim() });
    ElMessage.success('评论发表成功');
    commentContent.value = '';
    loadComments(1); // 重新加载评论列表
  } catch (error) {
    console.error('Failed to submit comment:', error);
    ElMessage.error('评论发表失败，请稍后重试');
  }
};

// 点赞评论
const likeComment = async (commentId: string) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后点赞');
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
    ElMessage.error('点赞失败，请稍后重试');
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
    commentContent.value = `回复 @${comment.userName || '用户'}：`;
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
    ElMessage.success('举报已提交，感谢您的反馈');
    reportDialogVisible.value = false;
    // 重置表单
    reportForm.type = '';
    reportForm.description = '';
  } catch (error: any) {
    console.error('Failed to submit report:', error);
    if (error.name !== 'validate') {
      ElMessage.error('举报提交失败，请稍后重试');
    }
  }
};

// 显示联系方式
const showContactInfo = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后查看联系方式');
    return;
  }
  
  try {
    const response = await getContactInfo(requestItem.value.userId);
    contactInfo.value = response.data || {};
    contactDialogVisible.value = true;
  } catch (error) {
    console.error('Failed to get contact info:', error);
    ElMessage.error('获取联系方式失败，请稍后重试');
  }
};

// 发送消息
const sendMessage = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后发送消息');
    return;
  }
  
  // 这里可以跳转到消息页面或打开消息对话框
  ElMessage.info('消息功能开发中');
};

// 编辑求购
const editRequestItem = () => {
  router.push(`/request-items/edit/${requestItemId}`);
};

// 标记完成
const markAsCompleted = async () => {
  ElMessage.info('标记完成功能开发中');
  // 实际实现中需要调用API更新求购状态
};

// 取消求购
const cancelRequestItem = async () => {
  ElMessage.info('取消求购功能开发中');
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