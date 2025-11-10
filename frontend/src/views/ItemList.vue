<template>
  <div class="item-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>商品列表</h1>
      <p>发现校园内的优质二手商品</p>
    </div>

    <!-- 筛选和排序区域 -->
    <div class="filter-sort-section">
      <div class="filter-container">
        <!-- 分类筛选 -->
        <div class="filter-item">
          <label>分类：</label>
          <el-select v-model="category" placeholder="全部分类" @change="handleFilterChange">
            <el-option label="全部分类" value=""></el-option>
            <el-option label="数码电子" value="digital"></el-option>
            <el-option label="学习资料" value="textbook"></el-option>
            <el-option label="生活家居" value="home"></el-option>
            <el-option label="体育用品" value="sports"></el-option>
            <el-option label="服饰鞋包" value="clothing"></el-option>
            <el-option label="其他类别" value="others"></el-option>
          </el-select>
        </div>

        <!-- 价格区间筛选 -->
        <div class="filter-item">
          <label>价格：</label>
          <el-input-number v-model="minPrice" placeholder="最低价" size="small" :min="0"></el-input-number>
          <span class="price-separator">-</span>
          <el-input-number v-model="maxPrice" placeholder="最高价" size="small" :min="minPrice || 0"></el-input-number>
          <el-button type="primary" size="small" @click="handleFilterChange">确定</el-button>
        </div>

        <!-- 状态筛选 -->
        <div class="filter-item">
          <label>状态：</label>
          <el-select v-model="status" placeholder="全部状态" @change="handleFilterChange">
            <el-option label="全部状态" value=""></el-option>
            <el-option label="在售" value="available"></el-option>
            <el-option label="已售出" value="sold"></el-option>
          </el-select>
        </div>

        <!-- 排序方式 -->
        <div class="filter-item">
          <label>排序：</label>
          <el-select v-model="sortBy" placeholder="默认排序" @change="handleFilterChange">
            <el-option label="默认排序" value=""></el-option>
            <el-option label="价格从低到高" value="price_asc"></el-option>
            <el-option label="价格从高到低" value="price_desc"></el-option>
            <el-option label="最新发布" value="time_desc"></el-option>
            <el-option label="最热商品" value="popular"></el-option>
          </el-select>
        </div>
      </div>

      <!-- 搜索框 -->
      <div class="search-container">
        <el-input v-model="searchQuery" placeholder="搜索商品名称、描述..." @keyup.enter="handleSearch">
          <template #append>
            <el-button @click="handleSearch"><i class="el-icon-search"></i></el-button>
          </template>
        </el-input>
      </div>
    </div>

    <!-- 标签筛选 -->
    <div class="tags-filter">
      <span class="tags-label">热门标签：</span>
      <el-tag v-for="tag in popularTags" :key="tag" :type="selectedTags.includes(tag) ? 'primary' : 'info'" @click="handleTagClick(tag)">{{ tag }}</el-tag>
    </div>

    <!-- 商品列表 -->
    <div class="items-container">
      <div class="item-card" v-for="item in items" :key="item.id">
        <router-link :to="`/items/${item.id}`" class="item-link">
          <div class="item-image">
            <img :src="item.image" :alt="item.name" class="image">
            <span v-if="item.discount" class="discount-badge">{{ item.discount }}折</span>
            <span v-if="item.status === 'sold'" class="sold-badge">已售出</span>
          </div>
          <div class="item-info">
            <h3 class="item-name">{{ item.name }}</h3>
            <div class="item-price">
              <span class="price">¥{{ item.price }}</span>
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
      <el-empty description="暂无符合条件的商品" />
      <el-button type="primary" @click="resetFilters">重置筛选条件</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { getItems, searchItems } from '@/api/item';
import { formatTime } from '@/utils/common';

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
}

// 筛选和排序参数
const category = ref('');
const minPrice = ref<number | null>(null);
const maxPrice = ref<number | null>(null);
const status = ref('');
const sortBy = ref('');
const searchQuery = ref('');
const selectedTags = ref<string[]>([]);
const currentPage = ref(1);
const pageSize = ref(12);
const totalItems = ref(0);
const loading = ref(false);
const items = ref<Item[]>([]);

// 热门标签
const popularTags = ref([
  '二手教材', '考研资料', '笔记本电脑', '平板', '手机', '自行车', '电动车',
  '吉他', '篮球', '羽毛球拍', '键盘', '鼠标', '显示器', '耳机', '充电宝'
]);

// 加载商品列表
const loadItems = async () => {
  loading.value = true;
  try {
    const params = {
      category: category.value,
      minPrice: minPrice.value,
      maxPrice: maxPrice.value,
      status: status.value,
      sortBy: sortBy.value,
      tags: selectedTags.value.join(','),
      page: currentPage.value,
      pageSize: pageSize.value
    };

    let response;
    if (searchQuery.value) {
      response = await searchItems({ keyword: searchQuery.value, ...params });
    } else {
      response = await getItems(params);
    }

    items.value = response.data?.items || [];
    totalItems.value = response.data?.total || 0;
  } catch (error) {
    console.error('Failed to load items:', error);
    ElMessage.error('加载商品列表失败，请稍后重试');
    // 使用模拟数据
    items.value = mockItems;
    totalItems.value = mockItems.length;
  } finally {
    loading.value = false;
  }
};

// 处理筛选条件变化
const handleFilterChange = () => {
  currentPage.value = 1;
  loadItems();
};

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1;
  loadItems();
};

// 处理标签点击
const handleTagClick = (tag: string) => {
  const index = selectedTags.value.indexOf(tag);
  if (index > -1) {
    selectedTags.value.splice(index, 1);
  } else {
    selectedTags.value.push(tag);
  }
  currentPage.value = 1;
  loadItems();
};

// 处理分页大小变化
const handleSizeChange = (size: number) => {
  pageSize.value = size;
  loadItems();
};

// 处理当前页变化
const handleCurrentChange = (current: number) => {
  currentPage.value = current;
  loadItems();
};

// 重置筛选条件
const resetFilters = () => {
  category.value = '';
  minPrice.value = null;
  maxPrice.value = null;
  status.value = '';
  sortBy.value = '';
  searchQuery.value = '';
  selectedTags.value = [];
  currentPage.value = 1;
  loadItems();
};

// 组件挂载时加载数据
onMounted(() => {
  loadItems();
});

// 模拟商品数据
const mockItems = [
  {
    id: 1,
    name: '全新未拆封MacBook Pro 2022',
    image: '/assets/images/macbook.jpg',
    price: 8999,
    originalPrice: 11999,
    discount: 7.5,
    location: '主校区',
    views: 238,
    status: 'available',
    createdAt: Date.now() - 3600000,
    tags: ['笔记本电脑', '苹果', '全新']
  },
  {
    id: 2,
    name: '九成新iPad Pro 2021',
    image: '/assets/images/ipad.jpg',
    price: 4500,
    originalPrice: 6299,
    location: '东校区',
    views: 196,
    status: 'available',
    createdAt: Date.now() - 7200000,
    tags: ['平板', 'iPad', '九成新']
  },
  {
    id: 3,
    name: '大学英语四六级词汇书',
    image: '/assets/images/englishbook.jpg',
    price: 25,
    originalPrice: 58,
    discount: 4.3,
    location: '图书馆',
    views: 152,
    status: 'available',
    createdAt: Date.now() - 10800000,
    tags: ['二手教材', '英语', '四六级']
  },
  {
    id: 4,
    name: '考研数学复习全书',
    image: '/assets/images/mathbook.jpg',
    price: 35,
    originalPrice: 78,
    location: '西校区',
    views: 128,
    status: 'available',
    createdAt: Date.now() - 14400000,
    tags: ['考研资料', '数学', '复习全书']
  },
  {
    id: 5,
    name: '篮球Nike NBA官方用球',
    image: '/assets/images/basketball.jpg',
    price: 80,
    originalPrice: 168,
    location: '体育馆',
    views: 96,
    status: 'available',
    createdAt: Date.now() - 18000000,
    tags: ['体育用品', '篮球', 'Nike']
  },
  {
    id: 6,
    name: '吉他初学者套装',
    image: '/assets/images/guitar.jpg',
    price: 199,
    originalPrice: 399,
    location: '音乐楼',
    views: 85,
    status: 'available',
    createdAt: Date.now() - 21600000,
    tags: ['乐器', '吉他', '初学者']
  },
  {
    id: 7,
    name: '专业绘图板Wacom',
    image: '/assets/images/tablet.jpg',
    price: 450,
    originalPrice: 899,
    location: '设计学院',
    views: 72,
    status: 'sold',
    createdAt: Date.now() - 25200000,
    tags: ['数码电子', '绘图板', '设计']
  },
  {
    id: 8,
    name: '校园自行车',
    image: '/assets/images/bike.jpg',
    price: 150,
    originalPrice: 350,
    location: '车棚',
    views: 65,
    status: 'available',
    createdAt: Date.now() - 28800000,
    tags: ['交通工具', '自行车', '校园']
  },
  {
    id: 9,
    name: '无线耳机AirPods Pro',
    image: '/assets/images/airpods.jpg',
    price: 1200,
    originalPrice: 1999,
    location: '主校区',
    views: 189,
    status: 'available',
    createdAt: Date.now() - 32400000,
    tags: ['耳机', '无线', '苹果']
  },
  {
    id: 10,
    name: '机械键盘青轴',
    image: '/assets/images/keyboard.jpg',
    price: 150,
    originalPrice: 299,
    location: '计算机学院',
    views: 145,
    status: 'available',
    createdAt: Date.now() - 36000000,
    tags: ['键盘', '机械键盘', '游戏']
  },
  {
    id: 11,
    name: '电动车60V',
    image: '/assets/images/ebike.jpg',
    price: 1200,
    originalPrice: 2500,
    location: '东校区',
    views: 210,
    status: 'available',
    createdAt: Date.now() - 39600000,
    tags: ['交通工具', '电动车', '代步']
  },
  {
    id: 12,
    name: '羽毛球拍尤尼克斯',
    image: '/assets/images/badminton.jpg',
    price: 200,
    originalPrice: 450,
    location: '体育馆',
    views: 89,
    status: 'available',
    createdAt: Date.now() - 43200000,
    tags: ['体育用品', '羽毛球拍', '尤尼克斯']
  }
];
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
}

.items-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.item-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s;
}

.item-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

.item-link {
  display: block;
  text-decoration: none;
  color: #333;
}

.item-image {
  position: relative;
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
  background-color: #ff4d4f;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.sold-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #999;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.item-info {
  padding: 15px;
}

.item-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-price {
  margin-bottom: 10px;
}

.price {
  font-size: 18px;
  font-weight: bold;
  color: #ff4d4f;
}

.original-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
  margin-left: 10px;
}

.item-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #999;
  margin-bottom: 10px;
}

.item-meta i {
  margin-right: 4px;
}

.item-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
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