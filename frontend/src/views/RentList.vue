<template>
  <div class="rent-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>{{ $t('rent.title') }}</h1>
      <p>{{ $t('rent.subtitle') }}</p>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-section">
      <div class="filter-row">
        <el-input
          v-model="searchKeyword"
          :placeholder="$t('rent.searchPlaceholder')"
          class="search-input"
          prefix-icon="el-icon-search"
        />
        <el-select
          v-model="categoryFilter"
          :placeholder="$t('rent.selectCategory')"
          class="category-select"
        >
          <el-option :label="$t('rent.categories.all')" value="" />
          <el-option :label="$t('rent.categories.electronics')" value="electronics" />
          <el-option :label="$t('rent.categories.sports')" value="sports" />
          <el-option :label="$t('rent.categories.music')" value="music" />
          <el-option :label="$t('rent.categories.books')" value="books" />
          <el-option :label="$t('rent.categories.other')" value="other" />
        </el-select>
        <el-button type="primary" @click="searchItems" class="search-btn">{{ $t('rent.search') }}</el-button>
      </div>
      <div class="filter-row">
        <el-slider
          v-model="priceRange"
          range
          :min="0"
          :max="2000"
          :marks="{0: '¥0', 500: '¥500', 1000: '¥1000', 1500: '¥1500', 2000: '¥2000'}"
          class="price-slider"
        />
      </div>
    </div>

    <!-- 租赁物品列表 -->
    <div class="rent-items-grid">
      <div class="rent-item-card" v-for="item in rentItems" :key="item.id">
        <router-link :to="`/rent/detail/${item.id}`" class="item-link">
          <div class="item-image">
            <img :src="item.image" :alt="item.name" class="image">
            <span class="rent-tag">{{ $t('rent.forRent') }}</span>
          </div>
          <div class="item-info">
            <h3 class="item-name">{{ item.name }}</h3>
            <div class="item-price">
              <span class="price">¥{{ item.price }}{{ $t('rent.perDay') }}</span>
              <span class="deposit">{{ $t('rent.deposit') }}: ¥{{ item.deposit }}</span>
            </div>
            <div class="item-meta">
              <span class="location"><i class="el-icon-location"></i>{{ item.location }}</span>
              <span class="available"><i class="el-icon-check"></i>{{ item.available ? $t('rent.available') : $t('rent.rented') }}</span>
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
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalCount"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 发布租赁按钮 -->
    <router-link to="/rent/create" class="create-btn">
      <el-button type="primary" size="large">{{ $t('rent.publishRent') }}</el-button>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// 获取静态资源路径的帮助函数
const getAssetUrl = (path: string) => {
  return new URL(`../assets/images/${path}`, import.meta.url).href;
};

// 搜索和筛选条件
const searchKeyword = ref('');
const categoryFilter = ref('');
const priceRange = ref([0, 2000]);

// 分页数据
const currentPage = ref(1);
const pageSize = ref(12);
const totalCount = ref(0);

// 租赁物品数据
interface RentItem {
  id: number;
  name: string;
  image: string;
  price: number;
  deposit: number;
  location: string;
  available: boolean;
  category: string;
}

const rentItems = ref<RentItem[]>([]);

// 模拟租赁数据 - 使用 computed 支持 i18n
const mockRentItems = computed(() => [
  {
    id: 1,
    name: t('rent.mockData.camera'),
    image: getAssetUrl('camera.webp'),
    price: 150,
    deposit: 3000,
    location: t('rent.mockData.locations.mainCampus'),
    available: true,
    category: 'electronics'
  },
  {
    id: 2,
    name: t('rent.mockData.tablet'),
    image: getAssetUrl('tablet.webp'),
    price: 50,
    deposit: 800,
    location: t('rent.mockData.locations.designSchool'),
    available: true,
    category: 'electronics'
  },
  {
    id: 3,
    name: t('rent.mockData.basketball'),
    image: getAssetUrl('basketball.webp'),
    price: 20,
    deposit: 200,
    location: t('rent.mockData.locations.gym'),
    available: true,
    category: 'sports'
  },
  {
    id: 4,
    name: t('rent.mockData.guitar'),
    image: getAssetUrl('guitar.webp'),
    price: 80,
    deposit: 1000,
    location: t('rent.mockData.locations.musicBuilding'),
    available: false,
    category: 'music'
  },
  {
    id: 5,
    name: t('rent.mockData.examBooks'),
    image: getAssetUrl('englishbook.webp'),
    price: 10,
    deposit: 200,
    location: t('rent.mockData.locations.library'),
    available: true,
    category: 'books'
  },
  {
    id: 6,
    name: t('rent.mockData.bicycle'),
    image: getAssetUrl('bike.webp'),
    price: 30,
    deposit: 500,
    location: t('rent.mockData.locations.bikeShed'),
    available: true,
    category: 'other'
  }
]);

// 加载租赁物品数据
const loadRentItems = async () => {
  try {
    // 在实际项目中，这里应该调用API获取数据
    // const res = await getRentItems({
    //   page: currentPage.value,
    //   pageSize: pageSize.value,
    //   keyword: searchKeyword.value,
    //   category: categoryFilter.value,
    //   minPrice: priceRange.value[0],
    //   maxPrice: priceRange.value[1]
    // });

    // 使用模拟数据
    rentItems.value = mockRentItems.value;
    totalCount.value = mockRentItems.value.length;
  } catch (error) {
    console.error(t('rent.loadFailed'), error);
    rentItems.value = mockRentItems.value;
    totalCount.value = mockRentItems.value.length;
  }
};

// 搜索按钮点击事件
const searchItems = () => {
  currentPage.value = 1;
  loadRentItems();
};

// 分页大小变化
const handleSizeChange = (size: number) => {
  pageSize.value = size;
  loadRentItems();
};

// 当前页变化
const handleCurrentChange = (current: number) => {
  currentPage.value = current;
  loadRentItems();
};

// 页面加载时初始化数据
onMounted(() => {
  loadRentItems();
});
</script>

<style lang="scss" scoped>
.rent-list-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 16px;
  color: #666;
}

.filter-section {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.search-input {
  flex: 1;
  max-width: 300px;
}

.category-select {
  width: 180px;
}

.search-btn {
  white-space: nowrap;
}

.price-slider {
  flex: 1;
}

.rent-items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.rent-item-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.rent-item-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
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
  transition: transform 0.3s ease;
}

.rent-item-card:hover .image {
  transform: scale(1.05);
}

.rent-tag {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #409eff;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.item-info {
  padding: 15px;
}

.item-name {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.price {
  font-size: 20px;
  font-weight: bold;
  color: #f56c6c;
}

.deposit {
  font-size: 14px;
  color: #666;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #999;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.create-btn {
  display: block;
  text-align: center;
  margin-bottom: 40px;
}

.create-btn .el-button {
  width: 200px;
}
</style>