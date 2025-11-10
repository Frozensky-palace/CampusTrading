<template>
  <div class="compare-detail-container">
    <!-- 面包屑导航 -->
    <div class="breadcrumb-section">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/compare-tasks' }">比价任务</el-breadcrumb-item>
        <el-breadcrumb-item>{{ compareTask?.title }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 比价任务详情卡片 -->
    <div class="compare-detail-card" v-if="compareTask">
      <!-- 任务基本信息 -->
      <div class="task-header">
        <h1 class="task-title">{{ compareTask.title }}</h1>
        <div class="task-badges">
          <span class="category-badge">{{ getCategoryName(compareTask.category) }}</span>
          <span class="status-badge" :class="getStatusClass(compareTask.status)">{{ getStatusText(compareTask.status) }}</span>
        </div>
      </div>

      <!-- 任务主要内容 -->
      <div class="task-content">
        <div class="content-left">
          <!-- 任务描述 -->
          <div class="task-description">
            <h3>任务描述</h3>
            <div class="description-content">
              {{ compareTask.description }}
            </div>
          </div>

          <!-- 任务要求 -->
          <div class="task-requirements" v-if="compareTask.requirements && compareTask.requirements.length > 0">
            <h3>具体要求</h3>
            <ul class="requirements-list">
              <li v-for="(req, index) in compareTask.requirements" :key="index">
                <i class="el-icon-check"></i> {{ req }}
              </li>
            </ul>
          </div>

          <!-- 标签 -->
          <div class="task-tags" v-if="compareTask.tags && compareTask.tags.length > 0">
            <el-tag
              v-for="tag in compareTask.tags"
              :key="tag"
              size="medium"
              type="info"
              effect="plain"
            >
              {{ tag }}
            </el-tag>
          </div>
        </div>

        <div class="content-right">
          <!-- 任务信息卡片 -->
          <div class="info-card">
            <div class="info-item">
              <span class="info-label">预算价格</span>
              <span class="info-value price">{{ formatPrice(compareTask.budget) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">期望新旧</span>
              <span class="info-value">{{ getConditionText(compareTask.condition) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">交易地点</span>
              <span class="info-value">{{ compareTask.location }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">交易方式</span>
              <span class="info-value">{{ getTradeMethodText(compareTask.tradeMethod) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">发布时间</span>
              <span class="info-value">{{ formatTime(compareTask.createdAt) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">截止时间</span>
              <span class="info-value deadline" :class="{ 'expired': isDeadlineExpired }">
                {{ formatTime(compareTask.deadline) }}
                <span v-if="isDeadlineExpired" class="expired-tag">（已过期）</span>
              </span>
            </div>
            <div class="info-item">
              <span class="info-label">查看次数</span>
              <span class="info-value">{{ compareTask.viewCount || 0 }}</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="action-buttons" v-if="isLoggedIn">
            <el-button
              v-if="compareTask.status === 'active' && !isTaskCreator"
              type="primary"
              size="large"
              class="quote-button"
              @click="showQuoteDialog"
            >
              提交报价
            </el-button>
            <el-button
              v-if="compareTask.status === 'active' && isTaskCreator"
              type="warning"
              size="large"
              @click="closeTask"
            >
              结束比价
            </el-button>
            <el-button
              v-if="compareTask.status === 'active' && isTaskCreator"
              type="danger"
              size="large"
              @click="cancelTask"
            >
              取消任务
            </el-button>
          </div>

          <!-- 未登录提示 -->
          <div class="login-prompt" v-else>
            <el-button type="primary" size="large" @click="redirectToLogin">
              登录后操作
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-else class="loading-container">
      <el-loading v-loading="true" element-loading-text="正在加载任务详情...">
        <div style="height: 400px;"></div>
      </el-loading>
    </div>

    <!-- 报价区域 -->
    <div class="quotes-section" v-if="compareTask">
      <div class="section-header">
        <h2>报价列表 <span class="quote-count">({{ quotes.length }} 个)</span></h2>
        <el-button type="text" @click="sortQuotes" class="sort-button">
          <i class="el-icon-sort"></i> 价格排序
        </el-button>
      </div>

      <!-- 报价列表 -->
      <div class="quotes-list">
        <div v-if="quotes.length > 0">
          <el-card
            v-for="quote in sortedQuotes"
            :key="quote.id"
            class="quote-card"
            :class="{ 'selected-quote': quote.selected }"
          >
            <div class="quote-content">
              <div class="quote-header">
                <div class="quote-price">
                  <span class="price-label">报价</span>
                  <span class="price-value">{{ formatPrice(quote.price) }}</span>
                </div>
                <div class="quote-meta">
                  <span class="quote-time">{{ formatTime(quote.createdAt) }}</span>
                  <span v-if="quote.selected" class="selected-badge">已选中</span>
                </div>
              </div>

              <div class="quote-body">
                <p class="quote-description">{{ quote.description }}</p>
              </div>

              <div class="quote-footer">
                <!-- 卖家信息 -->
                <div class="seller-info">
                  <img :src="quote.userAvatar || defaultAvatar" alt="用户头像" class="seller-avatar">
                  <div class="seller-details">
                    <div class="seller-name">{{ quote.userName }}</div>
                    <div class="seller-rating">
                      <span>信誉评分：{{ quote.userRating || 0 }}</span>
                      <el-rate v-model="quote.userRating" :max="5" :disabled="true" show-score />
                    </div>
                  </div>
                </div>

                <!-- 操作按钮 -->
                <div class="quote-actions">
                  <el-button type="text" @click="viewSellerProfile(quote.userId)">
                    <i class="el-icon-user"></i> 查看卖家
                  </el-button>
                  <el-button type="primary" @click="contactSeller(quote.userId, quote.id)">
                    <i class="el-icon-chat-dot-round"></i> 联系卖家
                  </el-button>
                  <el-button
                    v-if="isTaskCreator && !quote.selected && compareTask.status === 'active'"
                    type="success"
                    @click="selectQuote(quote.id)"
                  >
                    选择此报价
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 无报价 -->
        <div v-else class="no-quotes">
          <div class="no-quotes-icon">
            <i class="el-icon-comment"></i>
          </div>
          <p class="no-quotes-text">暂无报价</p>
          <p class="no-quotes-hint" v-if="!isTaskCreator">快来提交第一个报价吧！</p>
          <p class="no-quotes-hint" v-else>等待其他用户的报价...</p>
        </div>
      </div>
    </div>

    <!-- 评论区域 -->
    <div class="comments-section" v-if="compareTask">
      <div class="section-header">
        <h2>评论讨论 <span class="comment-count">({{ comments.length }} 条)</span></h2>
      </div>

      <!-- 评论列表 -->
      <div class="comments-list">
        <div v-if="comments.length > 0">
          <el-card
            v-for="comment in comments"
            :key="comment.id"
            class="comment-card"
          >
            <div class="comment-content">
              <div class="comment-header">
                <img :src="comment.userAvatar || defaultAvatar" alt="用户头像" class="comment-avatar">
                <div class="comment-meta">
                  <div class="comment-user">{{ comment.userName }}</div>
                  <div class="comment-time">{{ formatTime(comment.createdAt) }}</div>
                </div>
              </div>
              <div class="comment-body">
                {{ comment.content }}
              </div>
              <div class="comment-footer">
                <el-button type="text" @click="likeComment(comment.id)">
                  <i class="el-icon-thumb-up"></i>
                  <span>{{ comment.likes || 0 }}</span>
                </el-button>
                <el-button type="text" @click="replyComment">
                  <i class="el-icon-chat-line-round"></i>
                  回复
                </el-button>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 无评论 -->
        <div v-else class="no-comments">
          <p>暂无评论，来发表第一条评论吧！</p>
        </div>

        <!-- 发表评论 -->
        <div class="comment-form" v-if="isLoggedIn">
          <el-input
            v-model="newComment"
            type="textarea"
            placeholder="写下你的评论..."
            :rows="3"
            maxlength="500"
            show-word-limit
          ></el-input>
          <div class="comment-form-actions">
            <el-button @click="cancelComment">取消</el-button>
            <el-button type="primary" @click="submitComment">提交评论</el-button>
          </div>
        </div>

        <!-- 登录提示 -->
        <div class="login-prompt" v-else>
          <el-button type="primary" @click="redirectToLogin">
            登录后评论
          </el-button>
        </div>
      </div>
    </div>

    <!-- 相关推荐 -->
    <div class="related-section" v-if="relatedTasks.length > 0">
      <div class="section-header">
        <h2>相关比价任务</h2>
      </div>
      <div class="related-tasks">
        <el-card
          v-for="task in relatedTasks"
          :key="task.id"
          class="related-task-card"
          hover
          @click="viewTaskDetail(task.id)"
        >
          <div class="related-task-content">
            <h3>{{ task.title }}</h3>
            <div class="related-task-meta">
              <span class="related-price">￥{{ formatPrice(task.budget) }}</span>
              <span class="related-category">{{ getCategoryName(task.category) }}</span>
              <span class="related-quote-count">{{ task.quoteCount || 0 }}个报价</span>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 提交报价对话框 -->
    <el-dialog
      v-model="quoteDialogVisible"
      title="提交报价"
      width="600px"
      :before-close="handleQuoteDialogClose"
    >
      <div class="quote-dialog-content">
        <div class="quote-form">
          <el-form :model="quoteForm" :rules="quoteRules" ref="quoteFormRef" label-width="80px">
            <el-form-item label="报价金额" prop="price">
              <el-input
                v-model.number="quoteForm.price"
                placeholder="请输入您的报价金额"
                prefix-icon="el-icon-money"
              ></el-input>
            </el-form-item>
            <el-form-item label="报价描述" prop="description">
              <el-input
                v-model="quoteForm.description"
                type="textarea"
                placeholder="请详细描述您的报价包含的内容、商品来源、新旧程度等信息"
                :rows="4"
                maxlength="500"
                show-word-limit
              ></el-input>
            </el-form-item>
            <el-form-item label="联系方式">
              <el-radio-group v-model="quoteForm.contactMethod">
                <el-radio-button label="站内信">站内信</el-radio-button>
                <el-radio-button label="手机">手机</el-radio-button>
                <el-radio-button label="微信">微信</el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-form>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleQuoteDialogClose">取消</el-button>
          <el-button type="primary" @click="submitQuote">提交报价</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getCompareTaskDetail, submitCompareQuote, getCompareQuotes, getCompareComments, submitCompareComment, likeCompareComment } from '@/api/compare';
import {
  formatPrice,
  formatTime,
  getCategoryName,
  getStatusText,
  getStatusClass,
  getConditionText,
  getTradeMethodText
} from '@/utils/common';

// 路由和参数
const router = useRouter();
const route = useRoute();
const taskId = route.params.id as string;

// 默认头像
const defaultAvatar = 'https://via.placeholder.com/40/409EFF/FFFFFF?text=U';

// 比价任务详情
const compareTask = ref<any>(null);

// 报价列表
const quotes = ref<any[]>([]);

// 评论列表
const comments = ref<any[]>([]);

// 相关比价任务
const relatedTasks = ref<any[]>([]);

// 加载状态
const loading = ref(false);

// 登录状态
const isLoggedIn = ref(true); // 实际项目中应从状态管理获取

// 任务创建者
const isTaskCreator = ref(false); // 实际项目中应根据用户ID判断

// 报价对话框显示状态
const quoteDialogVisible = ref(false);

// 报价表单
const quoteForm = reactive({
  price: null,
  description: '',
  contactMethod: '站内信'
});

// 报价表单验证规则
const quoteRules = {
  price: [
    { required: true, message: '请输入报价金额', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '报价金额必须大于0', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入报价描述', trigger: 'blur' },
    { min: 10, message: '描述至少10个字符', trigger: 'blur' }
  ]
};

// 报价表单引用
const quoteFormRef = ref<InstanceType<any>>();

// 排序方式
const sortByPrice = ref(false);

// 新评论内容
const newComment = ref('');

// 检查截止日期是否过期
const isDeadlineExpired = computed(() => {
  if (!compareTask.value?.deadline) return false;
  return new Date(compareTask.value.deadline) < new Date();
});

// 排序后的报价
const sortedQuotes = computed(() => {
  const quotesCopy = [...quotes.value];
  if (sortByPrice.value) {
    return quotesCopy.sort((a, b) => a.price - b.price);
  }
  return quotesCopy.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
});

// 加载比价任务详情
const loadCompareTaskDetail = async () => {
  loading.value = true;
  try {
    const response = await getCompareTaskDetail(taskId);
    compareTask.value = response.data;
    
    // 实际项目中应根据用户ID判断是否为任务创建者
    isTaskCreator.value = false;
    
    // 加载报价和评论
    await Promise.all([
      loadQuotes(),
      loadComments(),
      loadRelatedTasks()
    ]);
  } catch (error) {
    console.error('Failed to load compare task detail:', error);
    ElMessage.error('加载任务详情失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

// 加载报价列表
const loadQuotes = async () => {
  try {
    const response = await getCompareQuotes(taskId);
    quotes.value = response.data || [];
  } catch (error) {
    console.error('Failed to load quotes:', error);
    ElMessage.error('加载报价列表失败');
  }
};

// 加载评论列表
const loadComments = async () => {
  try {
    const response = await getCompareComments(taskId);
    comments.value = response.data || [];
  } catch (error) {
    console.error('Failed to load comments:', error);
    ElMessage.error('加载评论列表失败');
  }
};

// 加载相关任务
const loadRelatedTasks = async () => {
  // 模拟数据，实际项目中应调用API
  relatedTasks.value = [
    {
      id: 'rel1',
      title: '求购二手笔记本电脑，预算4000左右',
      budget: 4000,
      category: 'digital',
      quoteCount: 5
    },
    {
      id: 'rel2',
      title: '寻找二手专业相机，佳能或尼康',
      budget: 3500,
      category: 'digital',
      quoteCount: 3
    },
    {
      id: 'rel3',
      title: '求购全套考研复习资料',
      budget: 500,
      category: 'textbook',
      quoteCount: 8
    }
  ];
};

// 提交报价
const submitQuote = async () => {
  if (!quoteFormRef.value) return;
  
  try {
    await quoteFormRef.value.validate();
    
    // 构建报价数据
    const quoteData = {
      itemId: compareTask.value.items[0]?.id || '',
      price: quoteForm.price || 0,
      source: '用户报价',
      description: quoteForm.description,
      url: ''
    };
    
    await submitCompareQuote(compareTask.value.id, quoteData);
    
    ElMessage.success('报价提交成功');
    quoteDialogVisible.value = false;
    
    // 重置表单
    resetQuoteForm();
    
    // 重新加载报价列表
    await loadQuotes();
  } catch (error) {
    console.error('Failed to submit quote:', error);
    ElMessage.error('报价提交失败，请稍后重试');
  }
};

// 提交评论
const submitComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容');
    return;
  }
  
  try {
    const commentData = {
      taskId,
      content: newComment.value.trim()
    };
    
    await submitCompareComment(taskId, commentData);
    
    ElMessage.success('评论提交成功');
    
    // 清空评论框
    newComment.value = '';
    
    // 重新加载评论列表
    await loadComments();
  } catch (error) {
    console.error('Failed to submit comment:', error);
    ElMessage.error('评论提交失败，请稍后重试');
  }
};

// 点赞评论
const likeComment = async (commentId: string) => {
  try {
    await likeCompareComment(commentId);
    
    // 更新评论点赞数
    const comment = comments.value.find(c => c.id === commentId);
    if (comment) {
      comment.likes = (comment.likes || 0) + 1;
    }
    
    ElMessage.success('点赞成功');
  } catch (error) {
    console.error('Failed to like comment:', error);
    ElMessage.error('点赞失败，请稍后重试');
  }
};

// 选择报价
const selectQuote = async (quoteId: string) => {
  try {
    ElMessageBox.confirm(
      '确定要选择此报价吗？选择后比价任务将自动完成',
      '确认选择',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(async () => {
      // 实际项目中应调用API选择报价
      ElMessage.success('报价选择成功');
      
      // 更新报价状态
      quotes.value.forEach(quote => {
        quote.selected = quote.id === quoteId;
      });
      
      // 更新任务状态
      compareTask.value.status = 'completed';
    });
  } catch (error) {
    console.error('Failed to select quote:', error);
  }
};

// 结束比价任务
const closeTask = async () => {
  try {
    ElMessageBox.confirm(
      '确定要结束此比价任务吗？结束后将无法再接收新的报价',
      '确认结束',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(async () => {
      // 实际项目中应调用API结束任务
      ElMessage.success('比价任务已结束');
      compareTask.value.status = 'completed';
    });
  } catch (error) {
    console.error('Failed to close task:', error);
  }
};

// 取消比价任务
const cancelTask = async () => {
  try {
    ElMessageBox.confirm(
      '确定要取消此比价任务吗？取消后将无法恢复',
      '确认取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error'
      }
    ).then(async () => {
      // 实际项目中应调用API取消任务
      ElMessage.success('比价任务已取消');
      compareTask.value.status = 'cancelled';
    });
  } catch (error) {
    console.error('Failed to cancel task:', error);
  }
};

// 查看卖家资料
const viewSellerProfile = (userId: string) => {
  router.push(`/user/${userId}`);
};

// 联系卖家
const contactSeller = (userId: string, quoteId: string) => {
  router.push(`/message/${userId}?quoteId=${quoteId}`);
};

// 回复评论
const replyComment = () => {
  // 实际项目中应实现回复功能
  ElMessage.info('回复功能待实现');
};

// 排序报价
const sortQuotes = () => {
  sortByPrice.value = !sortByPrice.value;
};

// 显示报价对话框
const showQuoteDialog = () => {
  if (!isLoggedIn.value) {
    redirectToLogin();
    return;
  }
  
  if (isDeadlineExpired.value) {
    ElMessage.warning('此任务已过期，无法提交报价');
    return;
  }
  
  quoteDialogVisible.value = true;
};

// 处理报价对话框关闭
const handleQuoteDialogClose = () => {
  resetQuoteForm();
  quoteDialogVisible.value = false;
};

// 重置报价表单
const resetQuoteForm = () => {
  if (quoteFormRef.value) {
    quoteFormRef.value.resetFields();
  }
  quoteForm.price = null;
  quoteForm.description = '';
  quoteForm.contactMethod = '站内信';
};

// 取消评论
const cancelComment = () => {
  newComment.value = '';
};

// 查看任务详情
const viewTaskDetail = (id: string) => {
  router.push(`/compare-tasks/${id}`);
};

// 重定向到登录
const redirectToLogin = () => {
  router.push('/login');
};

// 组件挂载时加载数据
onMounted(() => {
  if (taskId) {
    loadCompareTaskDetail();
  }
});
</script>

<style lang="scss" scoped>
.compare-detail-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 面包屑导航 */
.breadcrumb-section {
  margin-bottom: 20px;
}

/* 比价任务详情卡片 */
.compare-detail-card {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.task-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.task-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.4;
}

.task-badges {
  display: flex;
  gap: 10px;
}

.category-badge {
  background-color: #e6f7ff;
  color: #1890ff;
  padding: 5px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.status-badge {
  padding: 5px 12px;
  border-radius: 4px;
  font-size: 14px;
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

/* 任务内容 */
.task-content {
  display: flex;
  gap: 40px;
}

.content-left {
  flex: 2;
}

.content-right {
  flex: 1;
}

/* 任务描述 */
.task-description {
  margin-bottom: 30px;
}

.task-description h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.description-content {
  color: #666;
  line-height: 1.8;
  font-size: 16px;
  white-space: pre-wrap;
}

/* 任务要求 */
.task-requirements {
  margin-bottom: 30px;
}

.task-requirements h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}

.requirements-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.requirements-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
  color: #666;
}

.requirements-list li i {
  color: #1890ff;
  margin-top: 4px;
}

/* 任务标签 */
.task-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* 信息卡片 */
.info-card {
  background-color: #fafafa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #f0f0f0;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 500;
  color: #666;
  font-size: 14px;
}

.info-value {
  font-size: 16px;
  color: #333;
}

.info-value.price {
  font-size: 24px;
  font-weight: bold;
  color: #ff6700;
}

.deadline.expired {
  color: #f56c6c;
}

.expired-tag {
  font-size: 12px;
  color: #f56c6c;
  margin-left: 5px;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.quote-button {
  width: 100%;
  padding: 15px;
  font-size: 18px;
}

.login-prompt {
  text-align: center;
  padding: 20px;
  background-color: #f0f9ff;
  border-radius: 8px;
}

/* 加载状态 */
.loading-container {
  background-color: white;
  border-radius: 8px;
  padding: 100px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 报价区域 */
.quotes-section {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.section-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.quote-count,
.comment-count {
  font-size: 16px;
  color: #666;
  font-weight: normal;
  margin-left: 10px;
}

.sort-button {
  font-size: 14px;
}

/* 报价列表 */
.quotes-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.quote-card {
  transition: all 0.3s ease;
  position: relative;
}

.quote-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.quote-card.selected-quote {
  border: 2px solid #1890ff;
}

.quote-content {
  padding: 10px;
}

.quote-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.quote-price {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.price-label {
  font-size: 14px;
  color: #666;
}

.price-value {
  font-size: 24px;
  font-weight: bold;
  color: #ff6700;
}

.quote-meta {
  display: flex;
  align-items: center;
  gap: 15px;
}

.quote-time {
  font-size: 12px;
  color: #999;
}

.selected-badge {
  background-color: #f0f9ff;
  color: #1890ff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.quote-body {
  margin-bottom: 20px;
}

.quote-description {
  color: #666;
  line-height: 1.6;
  white-space: pre-wrap;
}

.quote-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.seller-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.seller-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.seller-details {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.seller-name {
  font-weight: 500;
  color: #333;
}

.seller-rating {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #666;
}

.quote-actions {
  display: flex;
  gap: 10px;
}

/* 无报价状态 */
.no-quotes {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.no-quotes-icon {
  font-size: 60px;
  margin-bottom: 20px;
  color: #dcdfe6;
}

.no-quotes-text {
  font-size: 18px;
  margin-bottom: 10px;
  color: #606266;
}

.no-quotes-hint {
  font-size: 14px;
}

/* 评论区域 */
.comments-section {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 评论列表 */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-card {
  transition: all 0.3s ease;
}

.comment-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comment-content {
  padding: 10px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.comment-meta {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.comment-user {
  font-weight: 500;
  color: #333;
}

.comment-time {
  font-size: 12px;
  color: #999;
}

.comment-body {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
  white-space: pre-wrap;
}

.comment-footer {
  display: flex;
  gap: 20px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.comment-footer .el-button {
  padding: 0;
}

/* 无评论状态 */
.no-comments {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-size: 16px;
}

/* 评论表单 */
.comment-form {
  margin-top: 30px;
  padding-top: 30px;
  border-top: 2px solid #f0f0f0;
}

.comment-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

/* 相关推荐 */
.related-section {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.related-tasks {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.related-task-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.related-task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.related-task-content {
  padding: 10px;
}

.related-task-content h3 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.4;
}

.related-task-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.related-price {
  font-size: 18px;
  font-weight: bold;
  color: #ff6700;
}

.related-category {
  font-size: 12px;
  color: #666;
}

.related-quote-count {
  font-size: 12px;
  color: #999;
}

/* 报价对话框 */
.quote-dialog-content {
  max-height: 500px;
  overflow-y: auto;
}

.quote-form {
  padding: 10px 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .compare-detail-container {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .task-content {
    flex-direction: column;
    gap: 30px;
  }
  
  .task-title {
    font-size: 24px;
  }
  
  .section-header h2 {
    font-size: 20px;
  }
  
  .quote-footer {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .related-tasks {
    grid-template-columns: 1fr;
  }
  
  .quote-dialog-content {
    padding: 0 10px;
  }
}

@media (max-width: 480px) {
  .compare-detail-container {
    padding: 10px;
  }
  
  .compare-detail-card,
  .quotes-section,
  .comments-section,
  .related-section {
    padding: 15px;
  }
  
  .task-title {
    font-size: 20px;
  }
  
  .task-badges {
    flex-wrap: wrap;
  }
  
  .description-content {
    font-size: 14px;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .quote-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .comment-footer {
    flex-wrap: wrap;
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

.quote-card,
.comment-card,
.related-task-card {
  animation: fadeIn 0.3s ease-out;
}
</style>