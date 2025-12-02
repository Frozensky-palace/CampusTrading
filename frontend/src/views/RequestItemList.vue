<template>
  <div class="request-item-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1>{{ $t('request.list.title') }}</h1>
        <p>{{ $t('request.list.subtitle') }}</p>
      </div>
      <div class="action-buttons">
        <el-button type="primary" icon="el-icon-plus" @click="createRequestItem">{{ $t('request.list.publishRequest') }}</el-button>
      </div>
    </div>

    <!-- 筛选和搜索区域 -->
    <div class="filter-section">
      <div class="filter-container">
        <!-- 分类筛选 -->
        <div class="filter-item">
          <el-select v-model="filters.category" :placeholder="$t('request.list.categoryPlaceholder')" clearable>
            <el-option :label="$t('request.list.allCategories')" value=""></el-option>
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
          <el-select v-model="filters.priceRange" :placeholder="$t('request.list.priceRangePlaceholder')" clearable>
            <el-option :label="$t('request.list.noLimit')" value=""></el-option>
            <el-option :label="$t('request.list.price0_50')" value="0-50"></el-option>
            <el-option :label="$t('request.list.price50_200')" value="50-200"></el-option>
            <el-option :label="$t('request.list.price200_500')" value="200-500"></el-option>
            <el-option :label="$t('request.list.price500_1000')" value="500-1000"></el-option>
            <el-option :label="$t('request.list.priceAbove1000')" value="1000+"></el-option>
          </el-select>
        </div>

        <!-- 发布时间 -->
        <div class="filter-item">
          <el-select v-model="filters.timeRange" :placeholder="$t('request.list.timeRangePlaceholder')" clearable>
            <el-option :label="$t('request.list.allTime')" value=""></el-option>
            <el-option :label="$t('request.list.today')" value="today"></el-option>
            <el-option :label="$t('request.list.threeDays')" value="3days"></el-option>
            <el-option :label="$t('request.list.oneWeek')" value="week"></el-option>
            <el-option :label="$t('request.list.oneMonth')" value="month"></el-option>
          </el-select>
        </div>

        <!-- 状态筛选 -->
        <div class="filter-item">
          <el-select v-model="filters.status" :placeholder="$t('request.list.statusPlaceholder')" clearable>
            <el-option :label="$t('request.list.allStatus')" value=""></el-option>
            <el-option :label="$t('request.list.statusActive')" value="active"></el-option>
            <el-option :label="$t('request.list.statusCompleted')" value="completed"></el-option>
            <el-option :label="$t('request.list.statusCancelled')" value="cancelled"></el-option>
          </el-select>
        </div>

        <!-- 搜索框 -->
        <div class="search-container">
          <el-input
            v-model="filters.keyword"
            :placeholder="$t('request.list.searchPlaceholder')"
            prefix-icon="el-icon-search"
            @keyup.enter="search"
          >
            <template #append>
              <el-button type="primary" @click="search">{{ $t('request.list.search') }}</el-button>
            </template>
          </el-input>
        </div>
      </div>

      <!-- 标签筛选 -->
      <div class="tags-filter">
        <span class="tags-title">{{ $t('request.list.hotTags') }}</span>
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
        <span class="sort-title">{{ $t('request.list.sortTitle') }}</span>
        <el-radio-group v-model="sortOption" size="small">
          <el-radio-button label="newest">{{ $t('request.list.sortNewest') }}</el-radio-button>
          <el-radio-button label="priceAsc">{{ $t('request.list.sortPriceAsc') }}</el-radio-button>
          <el-radio-button label="priceDesc">{{ $t('request.list.sortPriceDesc') }}</el-radio-button>
          <el-radio-button label="hot">{{ $t('request.list.sortHot') }}</el-radio-button>
        </el-radio-group>
        <el-button
          type="text"
          icon="el-icon-refresh-left"
          @click="resetFilters"
          class="reset-button"
        >
          {{ $t('request.list.resetFilters') }}
        </el-button>
      </div>
    </div>

    <!-- 求购列表 -->
    <div class="request-item-list">
      <!-- 列表头部信息 -->
      <div class="list-header">
        <span class="result-count">{{ $t('request.list.resultCount') }} <strong>{{ requestItems.length }}</strong> {{ $t('request.list.resultCountUnit') }}</span>
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
      <div v-if="requestItems.length > 0" :class="`list-content ${viewMode}`">
        <!-- 列表模式 -->
        <div v-if="viewMode === 'list'" class="list-view">
          <el-card
            v-for="item in requestItems"
            :key="item.id"
            class="request-item-card"
            hover
            @click="viewItemDetail(item.id)"
          >
            <div class="card-content">
              <div class="item-main">
                <div class="item-title">
                  <h3>{{ item.title }}</h3>
                  <span class="price-tag">￥{{ formatPrice(item.maxPrice) }}</span>
                </div>
                <div class="item-info">
                  <div class="info-left">
                    <span class="category-tag">{{ getCategoryName(item.category) }}</span>
                    <span class="publish-time">{{ formatTime(item.createdAt) }}</span>
                    <span class="location">{{ item.location }}</span>
                  </div>
                  <div class="info-right">
                    <span class="status-badge" :class="getStatusClass(item.status)">{{ getStatusText(item.status) }}</span>
                  </div>
                </div>
              </div>
              <div class="item-desc">
                {{ item.description }}
              </div>
              <div class="item-footer">
                <div class="tags">
                  <el-tag v-for="tag in item.tags" :key="tag" size="small" type="info" effect="plain">
                    {{ tag }}
                  </el-tag>
                </div>
                <div class="item-stats">
                  <span class="stat-item">
                    <i class="el-icon-view"></i> {{ item.viewCount || 0 }}
                  </span>
                  <span class="stat-item">
                    <i class="el-icon-chat-dot-round"></i> {{ item.commentCount || 0 }}
                  </span>
                  <span class="stat-item">
                    <i class="el-icon-user"></i> {{ item.userName }}
                  </span>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 网格模式 -->
        <div v-else class="grid-view">
          <el-card
            v-for="item in requestItems"
            :key="item.id"
            class="request-item-grid"
            hover
            @click="viewItemDetail(item.id)"
          >
            <div class="grid-content">
              <div class="grid-header">
                <h3>{{ item.title }}</h3>
                <span class="price-tag">￥{{ formatPrice(item.maxPrice) }}</span>
              </div>
              <div class="grid-info">
                <span class="category-tag">{{ getCategoryName(item.category) }}</span>
                <span class="publish-time">{{ formatTime(item.createdAt) }}</span>
              </div>
              <div class="grid-desc">
                {{ truncateText(item.description, 100) }}
              </div>
              <div class="grid-footer">
                <span class="status-badge" :class="getStatusClass(item.status)">{{ getStatusText(item.status) }}</span>
                <span class="location">{{ item.location }}</span>
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
        <p class="empty-text">{{ $t('request.list.noResults') }}</p>
        <p class="empty-hint">{{ $t('request.list.noResultsHint') }}</p>
        <el-button type="primary" @click="resetFilters">{{ $t('request.list.resetFilters') }}</el-button>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination-container" v-if="requestItems.length > 0">
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
import { getRequestItemList } from '@/api/requestItem';
import { formatPrice, formatTime, truncateText } from '@/utils/common';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

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
  t('item.list.popularTags.textbook'),
  t('item.list.popularTags.laptop'),
  t('item.list.popularTags.basketball'),
  t('item.list.popularTags.headphones'),
  t('item.list.popularTags.bicycle'),
  t('item.list.popularTags.examMaterials'),
  t('item.list.popularTags.hanfu'),
  t('item.list.popularTags.guitar'),
  t('item.list.popularTags.keyboard'),
  t('item.list.popularTags.monitor')
]);

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
});

// 求购列表数据
const requestItems = ref<any[]>([]);

// 加载状态
const loading = ref(false);

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

// 获取状态样式
const getStatusClass = (status: string) => {
  const statusClassMap: Record<string, string> = {
    active: 'status-active',
    completed: 'status-completed',
    cancelled: 'status-cancelled'
  };
  return statusClassMap[status] || '';
};

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
  loadRequestItems();
};

// 搜索
const search = () => {
  pagination.currentPage = 1;
  loadRequestItems();
};

// 处理页面大小变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  loadRequestItems();
};

// 处理当前页面变化
const handleCurrentChange = (current: number) => {
  pagination.currentPage = current;
  loadRequestItems();
};

// 查看求购详情
const viewItemDetail = (id: string) => {
  router.push(`/request-items/${id}`);
};

// 发布求购
const createRequestItem = () => {
  router.push('/request-items/create');
};

// 加载求购列表
const loadRequestItems = async () => {
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

    // 调用API获取求购列表
    const response = await getRequestItemList(params);
    requestItems.value = response.data.items || [];
    pagination.total = response.data.total || 0;

    // 如果没有数据，显示提示
    if (requestItems.value.length === 0) {
      ElMessage.info(t('request.list.noMatchingInfo'));
    }
  } catch (error) {
    console.error('Failed to load request items:', error);
    ElMessage.error(t('request.list.loadFailed'));
  } finally {
    loading.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadRequestItems();
});
</script>

<style lang="scss" scoped>
.request-item-list-container {
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

/* 求购列表 */
.request-item-list {
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

.request-item-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.request-item-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.item-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.item-title {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  flex: 1;
}

.item-title h3 {
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

.item-info {
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

.item-desc {
  color: #666;
  line-height: 1.6;
}

.item-footer {
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

.item-stats {
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

.request-item-grid {
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.request-item-grid:hover {
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
  .request-item-list-container {
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
  
  .item-main {
    flex-direction: column;
    gap: 10px;
  }
  
  .item-title {
    flex-direction: column;
    gap: 10px;
  }
  
  .item-info {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .item-footer {
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
  .request-item-list-container {
    padding: 10px;
  }
  
  .page-header {
    padding: 15px;
  }
  
  .header-content h1 {
    font-size: 24px;
  }
  
  .filter-section,
  .request-item-list {
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

.request-item-card,
.request-item-grid {
  animation: fadeIn 0.3s ease-out;
}

.request-item-card:nth-child(n+2),
.request-item-grid:nth-child(n+2) {
  animation-delay: 0.1s;
}

.request-item-card:nth-child(n+3),
.request-item-grid:nth-child(n+3) {
  animation-delay: 0.2s;
}
</style>