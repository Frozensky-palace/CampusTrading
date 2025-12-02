<template>
  <div class="compare-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1>{{ $t('compare.list.title') }}</h1>
        <p>{{ $t('compare.list.subtitle') }}</p>
      </div>
      <div class="action-buttons">
        <el-button type="primary" icon="el-icon-plus" @click="createCompareTask">{{ $t('compare.list.publishCompare') }}</el-button>
      </div>
    </div>

    <!-- 筛选和搜索区域 -->
    <div class="filter-section">
      <div class="filter-container">
        <!-- 分类筛选 -->
        <div class="filter-item">
          <el-select v-model="filters.category" :placeholder="$t('compare.list.categoryPlaceholder')" clearable>
            <el-option :label="$t('compare.list.allCategories')" value=""></el-option>
            <el-option :label="$t('item.categories.digital')" value="digital"></el-option>
            <el-option :label="$t('item.categories.textbook')" value="textbook"></el-option>
            <el-option :label="$t('item.categories.home')" value="home"></el-option>
            <el-option :label="$t('item.categories.sports')" value="sports"></el-option>
            <el-option :label="$t('item.categories.clothing')" value="clothing"></el-option>
            <el-option :label="$t('item.categories.others')" value="others"></el-option>
          </el-select>
        </div>

        <!-- 价格区间 -->
        <div class="filter-item">
          <el-select v-model="filters.priceRange" :placeholder="$t('compare.list.priceRangePlaceholder')" clearable>
            <el-option :label="$t('compare.list.noLimit')" value=""></el-option>
            <el-option :label="$t('compare.list.price0_50')" value="0-50"></el-option>
            <el-option :label="$t('compare.list.price50_200')" value="50-200"></el-option>
            <el-option :label="$t('compare.list.price200_500')" value="200-500"></el-option>
            <el-option :label="$t('compare.list.price500_1000')" value="500-1000"></el-option>
            <el-option :label="$t('compare.list.priceAbove1000')" value="1000+"></el-option>
          </el-select>
        </div>

        <!-- 发布时间 -->
        <div class="filter-item">
          <el-select v-model="filters.timeRange" :placeholder="$t('compare.list.timeRangePlaceholder')" clearable>
            <el-option :label="$t('compare.list.allTime')" value=""></el-option>
            <el-option :label="$t('compare.list.today')" value="today"></el-option>
            <el-option :label="$t('compare.list.threeDays')" value="3days"></el-option>
            <el-option :label="$t('compare.list.oneWeek')" value="week"></el-option>
            <el-option :label="$t('compare.list.oneMonth')" value="month"></el-option>
          </el-select>
        </div>

        <!-- 状态筛选 -->
        <div class="filter-item">
          <el-select v-model="filters.status" :placeholder="$t('compare.list.statusPlaceholder')" clearable>
            <el-option :label="$t('compare.list.allStatus')" value=""></el-option>
            <el-option :label="$t('compare.list.statusActive')" value="active"></el-option>
            <el-option :label="$t('compare.list.statusCompleted')" value="completed"></el-option>
            <el-option :label="$t('compare.list.statusCancelled')" value="cancelled"></el-option>
          </el-select>
        </div>

        <!-- 搜索框 -->
        <div class="search-container">
          <el-input
            v-model="filters.keyword"
            :placeholder="$t('compare.list.searchPlaceholder')"
            prefix-icon="el-icon-search"
            @keyup.enter="search"
          >
            <template #append>
              <el-button type="primary" @click="search">{{ $t('compare.list.search') }}</el-button>
            </template>
          </el-input>
        </div>
      </div>

      <!-- 标签筛选 -->
      <div class="tags-filter">
        <span class="tags-title">{{ $t('compare.list.hotTags') }}</span>
        <el-tag
          v-for="tag in popularTags"
          :key="tag"
          :disable-transitions="false"
          :class="{ 'active-tag': activeTag === tag }"
          @click="selectTag(tag)"
        >
          {{ tag }}
        </el-tag>
      </div>

      <!-- 排序选项 -->
      <div class="sort-options">
        <span class="sort-title">{{ $t('compare.list.sortTitle') }}</span>
        <el-radio-group v-model="sortOption" size="small">
          <el-radio-button label="newest">{{ $t('compare.list.sortNewest') }}</el-radio-button>
          <el-radio-button label="priceAsc">{{ $t('compare.list.sortPriceAsc') }}</el-radio-button>
          <el-radio-button label="priceDesc">{{ $t('compare.list.sortPriceDesc') }}</el-radio-button>
          <el-radio-button label="hot">{{ $t('compare.list.sortHot') }}</el-radio-button>
        </el-radio-group>
        <el-button
          type="text"
          icon="el-icon-refresh-left"
          @click="resetFilters"
          class="reset-button"
        >
          {{ $t('compare.list.resetFilters') }}
        </el-button>
      </div>
    </div>

    <!-- 比价任务列表 -->
    <div class="compare-list">
      <!-- 列表头部信息 -->
      <div class="list-header">
        <span class="result-count">{{ $t('compare.list.resultCount') }} <strong>{{ compareTasks.length }}</strong> {{ $t('compare.list.resultCountUnit') }}</span>
        <div class="view-mode">
          <el-button-group size="small">
            <el-button
              :class="{ active: viewMode === 'list' }"
              icon="el-icon-s-order"
              @click="setViewMode('list')"
            ></el-button>
            <el-button
              :class="{ active: viewMode === 'grid' }"
              icon="el-icon-s-grid"
              @click="setViewMode('grid')"
            ></el-button>
          </el-button-group>
        </div>
      </div>

      <!-- 列表内容 -->
      <div v-if="compareTasks.length > 0" :class="`list-content ${viewMode}`">
        <!-- 列表模式 -->
        <div v-if="viewMode === 'list'" class="list-view">
          <el-card
            v-for="task in compareTasks"
            :key="task.id"
            class="compare-task-card"
            hover
            @click="viewTaskDetail(task.id)"
          >
            <div class="card-content">
              <div class="task-main">
                <div class="task-title">
                  <h3>{{ task.title }}</h3>
                  <span class="price-tag">{{ $t('compare.list.budget') }}￥{{ formatPrice(task.budget) }}</span>
                </div>
                <div class="task-info">
                  <div class="info-left">
                    <span class="category-tag">{{ getCategoryName(task.category) }}</span>
                    <span class="publish-time">{{ formatTime(task.createdAt) }}</span>
                    <span class="location">{{ task.location }}</span>
                  </div>
                  <div class="info-right">
                    <span class="status-badge" :class="getStatusClass(task.status)">{{ getStatusText(task.status) }}</span>
                    <span class="quote-count">
                      <i class="el-icon-chat-dot-round"></i> {{ $t('compare.list.quoteCount', { count: task.quoteCount || 0 }) }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="task-desc">
                {{ task.description }}
              </div>
              <div class="task-footer">
                <div class="tags">
                  <el-tag v-for="tag in task.tags" :key="tag" size="small" type="info" effect="plain">
                    {{ tag }}
                  </el-tag>
                </div>
                <div class="task-stats">
                  <span class="stat-item">
                    <i class="el-icon-view"></i> {{ task.viewCount || 0 }}
                  </span>
                  <span class="stat-item">
                    <i class="el-icon-user"></i> {{ task.userName }}
                  </span>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 网格模式 -->
        <div v-else class="grid-view">
          <el-card
            v-for="task in compareTasks"
            :key="task.id"
            class="compare-task-grid"
            hover
            @click="viewTaskDetail(task.id)"
          >
            <div class="grid-content">
              <div class="grid-header">
                <h3>{{ task.title }}</h3>
                <span class="price-tag">￥{{ formatPrice(task.budget) }}</span>
              </div>
              <div class="grid-info">
                <span class="category-tag">{{ getCategoryName(task.category) }}</span>
                <span class="publish-time">{{ formatTime(task.createdAt) }}</span>
              </div>
              <div class="grid-desc">
                {{ truncateText(task.description, 100) }}
              </div>
              <div class="grid-footer">
                <span class="status-badge" :class="getStatusClass(task.status)">{{ getStatusText(task.status) }}</span>
                <span class="quote-count">{{ $t('compare.list.quoteCount', { count: task.quoteCount || 0 }) }}</span>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <div class="empty-icon">
          <i class="el-icon-search"></i>
        </div>
        <p class="empty-text">{{ $t('compare.list.noResults') }}</p>
        <p class="empty-hint">{{ $t('compare.list.noResultsHint') }}</p>
        <el-button type="primary" @click="resetFilters">{{ $t('compare.list.resetFilters') }}</el-button>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination-container" v-if="compareTasks.length > 0">
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 30, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useI18n } from 'vue-i18n';
import { getCompareTaskList } from '@/api/compare';
import { formatPrice, formatTime, truncateText, getStatusClass } from '@/utils/common';

// i18n
const { t } = useI18n();

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
  return categoryMap[category] || category;
};

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    active: t('compare.list.statusActive'),
    completed: t('compare.list.statusCompleted'),
    cancelled: t('compare.list.statusCancelled')
  };
  return statusMap[status] || status;
};

// 路由
const router = useRouter();

// 筛选条件
const filters = reactive({
  keyword: '',
  category: '',
  priceRange: '',
  timeRange: '',
  status: ''
});

// 排序选项
const sortOption = ref('newest');

// 视图模式
const viewMode = ref('list');

// 活跃标签
const activeTag = ref('');

// 热门标签
const popularTags = computed(() => [
  t('item.list.popularTags.laptop'),
  t('item.list.popularTags.phone'),
  t('item.list.popularTags.headphones'),
  t('item.list.popularTags.examMaterials'),
  t('item.list.popularTags.textbook'),
  t('item.list.popularTags.monitor'),
  t('item.list.popularTags.keyboard'),
  t('item.list.popularTags.camera'),
  t('item.list.popularTags.sneakers'),
  t('item.list.popularTags.tablet')
]);

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
});

// 比价任务列表数据
const compareTasks = ref<any[]>([]);

// 加载状态
const loading = ref(false);

// 设置视图模式
const setViewMode = (mode: string) => {
  viewMode.value = mode;
};

// 选择标签
const selectTag = (tag: string) => {
  activeTag.value = activeTag.value === tag ? '' : tag;
  filters.keyword = activeTag.value;
  search();
};

// 重置筛选
const resetFilters = () => {
  filters.keyword = '';
  filters.category = '';
  filters.priceRange = '';
  filters.timeRange = '';
  filters.status = '';
  activeTag.value = '';
  sortOption.value = 'newest';
  pagination.currentPage = 1;
  loadCompareTasks();
};

// 搜索
const search = () => {
  pagination.currentPage = 1;
  loadCompareTasks();
};

// 处理页面大小变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  loadCompareTasks();
};

// 处理当前页面变化
const handleCurrentChange = (current: number) => {
  pagination.currentPage = current;
  loadCompareTasks();
};

// 查看比价详情
const viewTaskDetail = (id: string) => {
  router.push(`/compare-tasks/${id}`);
};

// 发布比价
const createCompareTask = () => {
  router.push('/compare-tasks/create');
};

// 加载比价任务列表
const loadCompareTasks = async () => {
  loading.value = true;
  try {
    // 构建请求参数
    const params = {
      keyword: filters.keyword,
      category: filters.category,
      priceRange: filters.priceRange,
      timeRange: filters.timeRange,
      status: filters.status,
      sortBy: sortOption.value,
      page: pagination.currentPage,
      pageSize: pagination.pageSize
    };

    // 调用API获取比价任务列表
    const response = await getCompareTaskList(params);
    compareTasks.value = response.data.tasks || [];
    pagination.total = response.data.total || 0;

    // 如果没有数据，显示提示
    if (compareTasks.value.length === 0) {
      ElMessage.info(t('compare.list.noMatchingInfo'));
    }
  } catch (error) {
    console.error('Failed to load compare tasks:', error);
    ElMessage.error(t('compare.list.loadFailed'));
  } finally {
    loading.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadCompareTasks();
});
</script>

<style lang="scss" scoped>
.compare-list-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 8px;
}

.header-content h1 {
  font-size: 28px;
  margin-bottom: 5px;
  color: #333;
}

.header-content p {
  font-size: 16px;
  color: #666;
}

.action-buttons .el-button {
  font-size: 16px;
  padding: 10px 20px;
}

/* 筛选区域 */
.filter-section {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
}

.filter-item {
  flex: 1;
  min-width: 150px;
}

.search-container {
  flex: 2;
  min-width: 250px;
}

/* 标签筛选 */
.tags-filter {
  margin-bottom: 20px;
  padding: 15px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.tags-title {
  font-weight: 500;
  margin-right: 10px;
}

.active-tag {
  background-color: #409eff !important;
  color: white !important;
}

/* 排序选项 */
.sort-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sort-title {
  font-weight: 500;
  margin-right: 10px;
}

/* 比价任务列表 */
.compare-list {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.result-count {
  font-size: 14px;
  color: #666;
}

.result-count strong {
  color: #409eff;
  margin: 0 5px;
}

/* 列表视图 */
.list-content {
  transition: all 0.3s ease;
}

.list-view {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.compare-task-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.compare-task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.task-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.task-title {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  flex: 1;
}

.task-title h3 {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin: 0;
  flex: 1;
}

.price-tag {
  font-size: 20px;
  font-weight: bold;
  color: #ff6700;
}

.task-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.info-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.category-tag {
  background-color: #e6f7ff;
  color: #1890ff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.publish-time {
  font-size: 12px;
  color: #999;
}

.location {
  font-size: 12px;
  color: #666;
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

.quote-count {
  font-size: 12px;
  color: #666;
  margin-left: 15px;
}

.task-desc {
  color: #666;
  line-height: 1.6;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.tags {
  display: flex;
  gap: 8px;
  flex: 1;
}

.task-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
}

/* 网格视图 */
.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.compare-task-grid {
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.compare-task-grid:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.grid-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
}

.grid-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.grid-header h3 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
  flex: 1;
}

.grid-info {
  display: flex;
  gap: 15px;
  padding: 5px 0;
  border-bottom: 1px solid #eee;
}

.grid-desc {
  color: #666;
  line-height: 1.5;
  font-size: 14px;
  flex: 1;
}

.grid-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  margin-top: auto;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.empty-icon {
  font-size: 60px;
  margin-bottom: 20px;
  color: #dcdfe6;
}

.empty-text {
  font-size: 18px;
  margin-bottom: 10px;
  color: #606266;
}

.empty-hint {
  font-size: 14px;
  margin-bottom: 30px;
}

/* 分页 */
.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .compare-list-container {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .filter-container {
    flex-direction: column;
  }
  
  .filter-item,
  .search-container {
    min-width: 100%;
  }
  
  .sort-options {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .list-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .task-main {
    flex-direction: column;
    gap: 10px;
  }
  
  .task-title {
    flex-direction: column;
    gap: 10px;
  }
  
  .task-info {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .task-footer {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .tags {
    flex-wrap: wrap;
  }
  
  .grid-view {
    grid-template-columns: 1fr;
  }
  
  .pagination-container {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .compare-list-container {
    padding: 10px;
  }
  
  .page-header {
    padding: 15px;
  }
  
  .header-content h1 {
    font-size: 24px;
  }
  
  .filter-section,
  .compare-list {
    padding: 15px;
  }
  
  .tags-filter {
    flex-direction: column;
    gap: 10px;
  }
  
  .sort-options .el-radio-group {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
  }
  
  .empty-state {
    padding: 40px 10px;
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

.compare-task-card,
.compare-task-grid {
  animation: fadeIn 0.3s ease-out;
}

.compare-task-card:nth-child(n+2),
.compare-task-grid:nth-child(n+2) {
  animation-delay: 0.1s;
}

.compare-task-card:nth-child(n+3),
.compare-task-grid:nth-child(n+3) {
  animation-delay: 0.2s;
}
</style>