<template>
  <div class="item-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>{{ $t('item.list.title') }}</h1>
      <p>{{ $t('item.list.subtitle') }}</p>
    </div>

    <!-- 筛选和排序区域 -->
    <div class="filter-sort-section">
      <div class="filter-container">
        <!-- 分类筛选 -->
        <div class="filter-item">
          <label>{{ $t('item.list.filterCategory') }}：</label>
          <el-select v-model="category" :placeholder="$t('item.list.allCategories')" @change="handleFilterChange">
            <el-option :label="$t('item.list.allCategories')" value=""></el-option>
            <el-option :label="$t('item.categories.digital')" value="digital"></el-option>
            <el-option :label="$t('item.categories.textbook')" value="textbook"></el-option>
            <el-option :label="$t('item.categories.home')" value="home"></el-option>
            <el-option :label="$t('item.categories.sports')" value="sports"></el-option>
            <el-option :label="$t('item.categories.clothing')" value="clothing"></el-option>
            <el-option :label="$t('item.categories.others')" value="others"></el-option>
          </el-select>
        </div>

        <!-- 交易类型筛选 -->
        <div class="filter-item">
          <label>{{ $t('item.list.filterTradeType') }}：</label>
          <el-select v-model="tradeType" :placeholder="$t('item.list.allTypes')" @change="handleFilterChange">
            <el-option :label="$t('item.list.allTypes')" value=""></el-option>
            <el-option :label="$t('item.list.normalTrade')" value="sale"></el-option>
            <el-option :label="$t('item.list.rental')" value="rent"></el-option>
          </el-select>
        </div>

        <!-- 价格区间筛选 -->
        <div class="filter-item">
          <label>{{ $t('item.list.filterPrice') }}：</label>
          <el-input-number v-model="minPrice" :placeholder="$t('item.list.minPrice')" size="small" :min="0"></el-input-number>
          <span class="price-separator">-</span>
          <el-input-number v-model="maxPrice" :placeholder="$t('item.list.maxPrice')" size="small" :min="minPrice || 0"></el-input-number>
          <el-button type="primary" size="small" @click="handleFilterChange">{{ $t('item.list.confirm') }}</el-button>
        </div>

        <!-- 状态筛选 -->
        <div class="filter-item">
          <label>{{ $t('item.list.filterStatus') }}：</label>
          <el-select v-model="status" :placeholder="$t('item.list.allStatus')" @change="handleFilterChange">
            <el-option :label="$t('item.list.allStatus')" value=""></el-option>
            <el-option :label="$t('item.list.onSale')" value="available"></el-option>
            <el-option :label="$t('item.list.soldOut')" value="sold"></el-option>
          </el-select>
        </div>

        <!-- 排序方式 -->
        <div class="filter-item">
          <label>{{ $t('item.list.sortBy') }}：</label>
          <el-select v-model="sortBy" :placeholder="$t('item.list.defaultSort')" @change="handleFilterChange">
            <el-option :label="$t('item.list.defaultSort')" value=""></el-option>
            <el-option :label="$t('item.list.priceLowToHigh')" value="price_asc"></el-option>
            <el-option :label="$t('item.list.priceHighToLow')" value="price_desc"></el-option>
            <el-option :label="$t('item.list.newest')" value="time_desc"></el-option>
            <el-option :label="$t('item.list.popular')" value="popular"></el-option>
          </el-select>
        </div>
      </div>

      <!-- 搜索框 -->
      <div class="search-container">
        <el-input v-model="searchQuery" :placeholder="$t('item.list.searchPlaceholder')" @keyup.enter="handleSearch">
          <template #append>
            <el-button @click="handleSearch"><i class="el-icon-search"></i></el-button>
          </template>
        </el-input>
      </div>
    </div>

    <!-- 标签筛选 -->
    <div class="tags-filter">
      <span class="tags-label">{{ $t('item.list.hotTags') }}：</span>
      <el-tag v-for="tag in popularTags" :key="tag" :type="selectedTags.includes(tag) ? 'primary' : 'info'" @click="handleTagClick(tag)">{{ tag }}</el-tag>
    </div>

    <!-- 商品列表 -->
    <div class="items-container">
      <div class="item-card" v-for="item in items" :key="item.id">
        <router-link :to="`/items/${item.id}`" class="item-link">
          <div class="item-image">
            <img :src="item.image" :alt="item.name" class="image">
            <span v-if="item.discount" class="discount-badge">{{ item.discount }}{{ $t('item.list.discount') }}</span>
            <span v-if="item.status === 'sold'" class="sold-badge">{{ $t('item.list.soldOut') }}</span>
            <span v-if="item.tradeType === 'rent'" class="rent-badge">{{ $t('item.list.rental') }}</span>
          </div>
          <div class="item-info">
            <h3 class="item-name">{{ item.name }}</h3>
            <div class="item-price">
              <span v-if="item.tradeType === 'rent'" class="price-label">￥{{ item.rental_price_day }}{{ $t('item.list.perDay') }}</span>
              <span v-else class="price">¥{{ item.price }}</span>
              <span v-if="item.originalPrice" class="original-price">¥{{ item.originalPrice }}</span>
            </div>
            <div class="item-meta">
              <span class="location"><i class="el-icon-location"></i>{{ item.location }}</span>
              <span class="views"><i class="el-icon-view"></i>{{ item.views }}</span>
              <span class="time"><i class="el-icon-clock"></i>{{ formatTime(item.createdAt) }}</span>
            </div>
            <div class="item-tags">
              <el-tag size="small" v-for="tag in item.tags.slice(0, 3)" :key="tag">{{ tag }}</el-tag>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[12, 24, 36, 48]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalItems"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 加载中 -->
    <el-loading v-if="loading" :target="'.item-list-container'" fullscreen />

    <!-- 空状态 -->
    <div v-if="!loading && items.length === 0" class="empty-state">
      <el-empty :description="$t('item.list.noItems')" />
      <el-button type="primary" @click="resetFilters">{{ $t('item.list.resetFilters') }}</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { searchItems } from '@/api/item';
import { formatTime } from '@/utils/common';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// 定义商品类型接口
interface Item {
  id: number;
  name: string;
  image: string;
  price: number;
  originalPrice?: number;
  discount?: number;
  location: string;
  views: number;
  status: string;
  createdAt: number;
  tags: string[];
  tradeType?: string;
  rental_price_day?: number;
}

// 分页方法
const handleSizeChange = (val: number) => {
  pageSize.value = val;
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
};

// 过滤条件变化方法
const handleFilterChange = () => {
  // 实现过滤逻辑，可能需要调用API获取数据
};

// 搜索方法
const handleSearch = async () => {
  try {
    const res = await searchItems({
      keyword: searchQuery.value,
      page: 1,
      pageSize: pageSize.value,
      sortBy: sortBy.value,
      sortOrder: sortOrder.value
    });
    items.value = res.data.items;
    totalItems.value = res.data.total;
  } catch (error) {
    console.error(t('item.list.searchFailed'), error);
  }
};

// 标签点击方法
const handleTagClick = (tag: string) => {
  const index = selectedTags.value.indexOf(tag);
  if (index > -1) {
    selectedTags.value.splice(index, 1);
  } else {
    selectedTags.value.push(tag);
  }
};

// 重置筛选条件
const resetFilters = () => {
  category.value = '';
  minPrice.value = null;
  maxPrice.value = null;
  searchQuery.value = '';
  sortBy.value = 'createdAt';
  sortOrder.value = 'desc';
  tradeType.value = '';
  selectedTags.value = [];
};

// 筛选和排序参数
const category = ref('');
const minPrice = ref<number | null>(null);
const maxPrice = ref<number | null>(null);
const status = ref('');
const sortBy = ref('createdAt');
const sortOrder = ref<'desc' | 'asc' | undefined>('desc');
const searchQuery = ref('');
const selectedTags = ref<string[]>([]);
const tradeType = ref('');
const currentPage = ref(1);
const pageSize = ref(12);
const loading = ref(false);
const items = ref<Item[]>([]);
const totalItems = ref(0);
const popularTags = computed(() => [
  t('item.list.popularTags.laptop'),
  t('item.list.popularTags.examMaterials'),
  t('item.list.popularTags.bicycle'),
  t('item.list.popularTags.basketball'),
  t('item.list.popularTags.guitar'),
  t('item.list.popularTags.drawingTablet')
]);
// ... existing code ...
</script>

<style lang="scss" scoped>
.item-list-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
}

.page-header h1 {
  font-size: 32px;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 16px;
  opacity: 0.9;
}

.filter-sort-section {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.filter-container {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-item label {
  font-weight: 500;
  color: #333;
  white-space: nowrap;
}

.el-select {
  min-width: 120px;
}

.price-separator {
  margin: 0 5px;
  color: #999;
}

.search-container {
  margin-top: 10px;
}

.el-input {
  width: 300px;
}

.tags-filter {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.tags-label {
  font-weight: 500;
  margin-right: 15px;
  color: #333;
}

.el-tag {
  margin-right: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.el-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.items-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.item-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s;
  overflow: hidden;
}

.item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.item-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.item-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.item-card:hover .image {
  transform: scale(1.05);
}

.discount-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: #ff4500;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  z-index: 1;
}

.sold-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #ccc;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  z-index: 1;
}

.rent-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #52c41a;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  z-index: 1;
}

.item-info {
  padding: 16px;
}

.item-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-price {
  margin-bottom: 8px;
}

.price {
  font-size: 20px;
  font-weight: 600;
  color: #ff4500;
}

.price-label {
  font-size: 18px;
  font-weight: 600;
  color: #52c41a;
}

.original-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
  margin-left: 8px;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 4px;
}

.location {
  flex: 1;
  min-width: 120px;
}

.views {
  flex: 1;
  min-width: 100px;
}

.time {
  flex: 1;
  min-width: 120px;
}

.item-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.pagination {
  text-align: center;
  margin-bottom: 30px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state .el-button {
  margin-top: 20px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .item-list-container {
    max-width: 100%;
    padding: 15px;
  }
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 24px;
  }
  
  .filter-container {
    flex-direction: column;
    gap: 15px;
  }
  
  .filter-item {
    width: 100%;
    justify-content: space-between;
  }
  
  .el-select,
  .el-input {
    width: 100%;
  }
  
  .items-container {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

@media (max-width: 480px) {
  .item-list-container {
    padding: 10px;
  }
  
  .page-header {
    padding: 15px 0;
  }
  
  .page-header h1 {
    font-size: 20px;
  }
  
  .filter-sort-section,
  .tags-filter {
    padding: 15px;
  }
  
  .items-container {
    grid-template-columns: 1fr;
  }
  
  .item-image {
    height: 180px;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.item-card {
  animation: fadeIn 0.5s ease-out;
}

.item-card:nth-child(1) { animation-delay: 0.05s; }
.item-card:nth-child(2) { animation-delay: 0.1s; }
.item-card:nth-child(3) { animation-delay: 0.15s; }
.item-card:nth-child(4) { animation-delay: 0.2s; }
.item-card:nth-child(5) { animation-delay: 0.25s; }
.item-card:nth-child(6) { animation-delay: 0.3s; }
.item-card:nth-child(7) { animation-delay: 0.35s; }
.item-card:nth-child(8) { animation-delay: 0.4s; }
.item-card:nth-child(9) { animation-delay: 0.45s; }
.item-card:nth-child(10) { animation-delay: 0.5s; }
.item-card:nth-child(11) { animation-delay: 0.55s; }
.item-card:nth-child(12) { animation-delay: 0.6s; }
</style>