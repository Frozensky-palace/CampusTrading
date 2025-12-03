<template>
  <div class="home-container">
    <!-- 轮播图区域 -->
    <div class="carousel-section">
      <el-carousel :interval="5000" type="card" height="400px" indicator-position="outside">
        <el-carousel-item v-for="(item, index) in carouselItems" :key="index">
          <img :src="item.image" :alt="item.title" class="carousel-image">
          <div class="carousel-caption">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
            <el-button type="primary" :href="item.link">{{ $t('home.viewNow') }}</el-button>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 功能导航区域 -->
    <div class="feature-nav">
      <div class="feature-item" v-for="feature in features" :key="feature.id">
        <router-link :to="feature.route">
          <div class="feature-icon">
            <el-icon :size="32"><component :is="feature.icon" /></el-icon>
          </div>
          <div class="feature-text">{{ feature.name }}</div>
        </router-link>
      </div>
    </div>

    <!-- 热门商品区域 -->
    <section class="section-container">
      <div class="section-header">
        <h2 class="section-title">{{ $t('home.sections.hotItems') }}</h2>
        <router-link to="/items" class="section-more">{{ $t('common.viewMore') }} <el-icon><ArrowRight /></el-icon></router-link>
      </div>
      <div class="item-list">
        <div class="item-card" v-for="item in hotItems" :key="item.id">
          <router-link :to="`/items/${item.id}`" class="item-link">
            <div class="item-image">
              <img :src="item.image" :alt="item.name" class="image">
              <span v-if="item.discount" class="discount-badge">{{ item.discount }}{{ $t('mockItems.discount') }}</span>
            </div>
            <div class="item-info">
              <h3 class="item-name">{{ item.name }}</h3>
              <div class="item-price">
                <span class="price">¥{{ item.price }}</span>
                <span v-if="item.originalPrice" class="original-price">¥{{ item.originalPrice }}</span>
              </div>
              <div class="item-meta">
                <span class="location"><el-icon><Location /></el-icon>{{ item.location }}</span>
                <span class="views"><el-icon><View /></el-icon>{{ item.views }}</span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 最新求购区域 -->
    <section class="section-container bg-gray">
      <div class="section-header">
        <h2 class="section-title">{{ $t('home.sections.latestRequests') }}</h2>
        <router-link to="/requests" class="section-more">{{ $t('common.viewMore') }} <el-icon><ArrowRight /></el-icon></router-link>
      </div>
      <div class="request-list">
        <router-link :to="`/requests/detail/${request.id}`" class="request-item" v-for="request in latestRequests" :key="request.id">
          <div class="request-info">
            <h3 class="request-title">{{ request.title }}</h3>
            <p class="request-content">{{ request.content }}</p>
            <div class="request-tags">
              <el-tag v-for="tag in request.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
            </div>
          </div>
          <div class="request-meta">
            <div class="price-range">{{ $t('home.budget') }}: ¥{{ request.minPrice }} - ¥{{ request.maxPrice }}</div>
            <div class="time-posted">{{ formatTime(request.createdAt) }}</div>
          </div>
        </router-link>
      </div>
    </section>

    <!-- 比价任务区域 -->
    <section class="section-container">
      <div class="section-header">
        <h2 class="section-title">{{ $t('home.sections.hotCompare') }}</h2>
        <router-link to="/compare" class="section-more">{{ $t('common.viewMore') }} <el-icon><ArrowRight /></el-icon></router-link>
      </div>
      <div class="compare-list">
        <div class="compare-card" v-for="task in hotCompareTasks" :key="task.id">
          <router-link :to="`/compare/detail/${task.id}`" class="compare-link">
            <div class="compare-header">
              <h3 class="compare-title">{{ task.title }}</h3>
              <span class="compare-count">{{ task.products.length }} {{ $t('home.products') }}</span>
            </div>
            <div class="compare-products">
              <div class="product-mini" v-for="(product, index) in task.products.slice(0, 3)" :key="index">
                <img :src="product.image" :alt="product.name" class="mini-image">
                <span class="mini-price">¥{{ product.price }}</span>
              </div>
              <div v-if="task.products.length > 3" class="product-more">
                <span>+{{ task.products.length - 3 }}</span>
              </div>
            </div>
            <div class="compare-meta">
              <span class="creator">{{ $t('home.by') }} {{ task.creator }}</span>
              <span class="likes"><el-icon><Star /></el-icon>{{ task.likes }}</span>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 平台优势区域 -->
    <section class="advantages-section">
      <div class="advantage-item" v-for="advantage in advantages" :key="advantage.id">
        <div class="advantage-icon">
          <el-icon :size="48"><component :is="advantage.icon" /></el-icon>
        </div>
        <h3 class="advantage-title">{{ advantage.title }}</h3>
        <p class="advantage-description">{{ advantage.description }}</p>
      </div>
    </section>

    <!-- 统计数据区域 -->
    <section class="stats-section">
      <div class="stat-item" v-for="stat in stats" :key="stat.id">
        <div class="stat-number">{{ stat.value }}</div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { formatTime } from '@/utils/common';

import { getHotItems, getLatestRequests, getHotCompareTasks, getPlatformStats } from '@/api/item';
import {
  CirclePlus,
  QuestionFilled,
  Sort,
  User,
  Lock,
  Lightning,
  PriceTag,
  Headset,
  ArrowRight,
  Location,
  View,
  Star
} from '@element-plus/icons-vue';

const { t } = useI18n();

// 获取静态资源路径的帮助函数
const getAssetUrl = (path: string) => {
  return new URL(`../assets/images/${path}`, import.meta.url).href;
};

// 轮播图数据 - 使用计算属性支持语言切换
const carouselItems = computed(() => [
  {
    image: getAssetUrl('back-to-school.png'),
    title: t('home.banner.newSemester'),
    description: t('home.banner.newSemesterDesc'),
    link: '/items?category=textbook'
  },
  {
    image: getAssetUrl('campus-digital-festival.jpg'),
    title: t('home.banner.digitalFestival'),
    description: t('home.banner.digitalFestivalDesc'),
    link: '/items?category=digital'
  },
  {
    image: getAssetUrl('graduation-season.png'),
    title: t('home.banner.graduation'),
    description: t('home.banner.graduationDesc'),
    link: '/items?tag=graduate'
  }
]);

// 功能导航数据 - 使用计算属性支持语言切换
const features = computed(() => [
  { id: 1, name: t('home.features.publishItem'), icon: CirclePlus, route: '/items/create' },
  { id: 2, name: t('home.features.publishRequest'), icon: QuestionFilled, route: '/requests/create' },
  { id: 3, name: t('home.features.createCompare'), icon: Sort, route: '/compare/create' },
  { id: 4, name: t('home.features.myCenter'), icon: User, route: '/user/profile' }
]);

// 平台优势数据 - 使用计算属性支持语言切换
const advantages = computed(() => [
  {
    id: 1,
    icon: Lock,
    title: t('home.advantages.safeTransaction'),
    description: t('home.advantages.safeTransactionDesc')
  },
  {
    id: 2,
    icon: Lightning,
    title: t('home.advantages.quickPublish'),
    description: t('home.advantages.quickPublishDesc')
  },
  {
    id: 3,
    icon: PriceTag,
    title: t('home.advantages.goodValue'),
    description: t('home.advantages.goodValueDesc')
  },
  {
    id: 4,
    icon: Headset,
    title: t('home.advantages.goodService'),
    description: t('home.advantages.goodServiceDesc')
  }
]);

// 统计数据
const stats = ref([
  { id: 1, value: '10,000+', label: '' },
  { id: 2, value: '5,000+', label: '' },
  { id: 3, value: '8,000+', label: '' },
  { id: 4, value: '98%', label: '' }
]);

// 更新统计数据标签
const updateStatsLabels = () => {
  stats.value = [
    { id: 1, value: stats.value[0].value, label: t('home.stats.registeredUsers') },
    { id: 2, value: stats.value[1].value, label: t('home.stats.itemsOnSale') },
    { id: 3, value: stats.value[2].value, label: t('home.stats.successfulDeals') },
    { id: 4, value: stats.value[3].value, label: t('home.stats.positiveRate') }
  ];
};

// 类型定义
interface HotItem {
  id: number;
  name: string;
  image: string;
  price: number;
  originalPrice: number;
  discount?: number;
  location: string;
  views: number;
}

interface RequestItem {
  id: number;
  title: string;
  content: string;
  tags: string[];
  minPrice: number;
  maxPrice: number;
  createdAt: number;
}

interface ProductItem {
  name: string;
  price: number;
  image: string;
}

interface CompareTask {
  id: number;
  title: string;
  products: ProductItem[];
  creator: string;
  likes: number;
}

// 热门商品数据
const hotItems = ref<HotItem[]>([]);

// 最新求购数据
const latestRequests = ref<RequestItem[]>([]);

// 热门比价任务
const hotCompareTasks = ref<CompareTask[]>([]);

// 加载数据
onMounted(async () => {
  // 初始化统计标签
  updateStatsLabels();

  try {
    // 加载热门商品
    const itemsRes = await getHotItems({ limit: 8 });
    hotItems.value = itemsRes.data || mockHotItems.value;

    // 加载最新求购
    const requestsRes = await getLatestRequests({ limit: 5 });
    latestRequests.value = requestsRes.data || mockLatestRequests.value;

    // 加载热门比价任务（修正路径为正确的API端点）
    try {
      const response = await fetch('/api/compare/hot?limit=4');
      if (response.ok) {
        const data = await response.json();
        hotCompareTasks.value = data.data || mockHotCompareTasks.value;
      } else {
        console.warn('Compare API failed, using mock data');
        hotCompareTasks.value = mockHotCompareTasks.value;
      }
    } catch (e) {
      console.warn('Compare API error, using mock data', e);
      hotCompareTasks.value = mockHotCompareTasks.value;
    }

    // 加载平台统计数据
    const statsRes = await getPlatformStats();
    if (statsRes.data) {
      stats.value = [
        { id: 1, value: statsRes.data.userCount, label: t('home.stats.registeredUsers') },
        { id: 2, value: statsRes.data.itemCount, label: t('home.stats.itemsOnSale') },
        { id: 3, value: statsRes.data.transactionCount, label: t('home.stats.successfulDeals') },
        { id: 4, value: statsRes.data.ratingRate, label: t('home.stats.positiveRate') }
      ];
    }
  } catch (error) {
    console.error('Failed to load home page data:', error);
    // 使用模拟数据
    hotItems.value = mockHotItems.value;
    latestRequests.value = mockLatestRequests.value;
    hotCompareTasks.value = mockHotCompareTasks.value;
  }
});

// 模拟热门商品数据 - 使用计算属性支持语言切换
const mockHotItems = computed(() => [
  {
    id: 1,
    name: t('mockItems.item1.name'),
    image: getAssetUrl('macbook.webp'),
    price: 8999,
    originalPrice: 11999,
    discount: 7.5,
    location: t('mockItems.item1.location'),
    views: 238
  },
  {
    id: 2,
    name: t('mockItems.item2.name'),
    image: getAssetUrl('ipadpro.webp'),
    price: 4500,
    originalPrice: 6299,
    location: t('mockItems.item2.location'),
    views: 196
  },
  {
    id: 3,
    name: t('mockItems.item3.name'),
    image: getAssetUrl('englishbook.webp'),
    price: 25,
    originalPrice: 58,
    discount: 4.3,
    location: t('mockItems.item3.location'),
    views: 152
  },
  {
    id: 4,
    name: t('mockItems.item4.name'),
    image: getAssetUrl('mathbook.webp'),
    price: 35,
    originalPrice: 78,
    location: t('mockItems.item4.location'),
    views: 128
  },
  {
    id: 5,
    name: t('mockItems.item5.name'),
    image: getAssetUrl('basketball.webp'),
    price: 80,
    originalPrice: 168,
    location: t('mockItems.item5.location'),
    views: 96
  },
  {
    id: 6,
    name: t('mockItems.item6.name'),
    image: getAssetUrl('guitar.webp'),
    price: 199,
    originalPrice: 399,
    location: t('mockItems.item6.location'),
    views: 85
  },
  {
    id: 7,
    name: t('mockItems.item7.name'),
    image: getAssetUrl('tablet.webp'),
    price: 450,
    originalPrice: 899,
    location: t('mockItems.item7.location'),
    views: 72
  },
  {
    id: 8,
    name: t('mockItems.item8.name'),
    image: getAssetUrl('bike.webp'),
    price: 150,
    originalPrice: 350,
    location: t('mockItems.item8.location'),
    views: 65
  }
]);

// 模拟最新求购数据 - 使用计算属性支持语言切换
const mockLatestRequests = computed(() => [
  {
    id: 1,
    title: t('mockRequests.request1.title'),
    content: t('mockRequests.request1.content'),
    tags: [t('mockRequests.request1.tag1'), t('mockRequests.request1.tag2'), t('mockRequests.request1.tag3')],
    minPrice: 50,
    maxPrice: 150,
    createdAt: new Date().getTime() - 3600000
  },
  {
    id: 2,
    title: t('mockRequests.request2.title'),
    content: t('mockRequests.request2.content'),
    tags: [t('mockRequests.request2.tag1'), t('mockRequests.request2.tag2'), t('mockRequests.request2.tag3')],
    minPrice: 1500,
    maxPrice: 2500,
    createdAt: new Date().getTime() - 7200000
  },
  {
    id: 3,
    title: t('mockRequests.request3.title'),
    content: t('mockRequests.request3.content'),
    tags: [t('mockRequests.request3.tag1'), t('mockRequests.request3.tag2'), t('mockRequests.request3.tag3')],
    minPrice: 800,
    maxPrice: 1500,
    createdAt: new Date().getTime() - 10800000
  },
  {
    id: 4,
    title: t('mockRequests.request4.title'),
    content: t('mockRequests.request4.content'),
    tags: [t('mockRequests.request4.tag1'), t('mockRequests.request4.tag2'), t('mockRequests.request4.tag3')],
    minPrice: 100,
    maxPrice: 300,
    createdAt: new Date().getTime() - 14400000
  },
  {
    id: 5,
    title: t('mockRequests.request5.title'),
    content: t('mockRequests.request5.content'),
    tags: [t('mockRequests.request5.tag1'), t('mockRequests.request5.tag2'), t('mockRequests.request5.tag3')],
    minPrice: 800,
    maxPrice: 1200,
    createdAt: new Date().getTime() - 18000000
  }
]);

// 模拟热门比价任务数据 - 使用计算属性支持语言切换
const mockHotCompareTasks = computed(() => [
  {
    id: 1,
    title: t('mockCompare.compare1.title'),
    products: [
      { name: t('mockCompare.compare1.product1'), price: 1999, image: getAssetUrl('laptop1.jpg') },
      { name: t('mockCompare.compare1.product2'), price: 2199, image: getAssetUrl('laptop2.jpg') },
      { name: t('mockCompare.compare1.product3'), price: 1899, image: getAssetUrl('laptop3.jpg') },
      { name: t('mockCompare.compare1.product4'), price: 2399, image: getAssetUrl('laptop4.jpg') }
    ],
    creator: t('mockCompare.compare1.creator'),
    likes: 128
  },
  {
    id: 2,
    title: t('mockCompare.compare2.title'),
    products: [
      { name: t('mockCompare.compare2.product1'), price: 15, image: getAssetUrl('food1.jpg') },
      { name: t('mockCompare.compare2.product2'), price: 25, image: getAssetUrl('food2.jpg') },
      { name: t('mockCompare.compare2.product3'), price: 20, image: getAssetUrl('food3.jpg') }
    ],
    creator: t('mockCompare.compare2.creator'),
    likes: 95
  },
  {
    id: 3,
    title: t('mockCompare.compare3.title'),
    products: [
      { name: t('mockCompare.compare3.product1'), price: 68, image: getAssetUrl('book1.jpg') },
      { name: t('mockCompare.compare3.product2'), price: 78, image: getAssetUrl('book2.jpg') },
      { name: t('mockCompare.compare3.product3'), price: 58, image: getAssetUrl('book3.jpg') },
      { name: t('mockCompare.compare3.product4'), price: 98, image: getAssetUrl('book4.jpg') },
      { name: t('mockCompare.compare3.product5'), price: 65, image: getAssetUrl('book5.jpg') }
    ],
    creator: t('mockCompare.compare3.creator'),
    likes: 215
  },
  {
    id: 4,
    title: t('mockCompare.compare4.title'),
    products: [
      { name: t('mockCompare.compare4.product1'), price: 300, image: getAssetUrl('bike1.jpg') },
      { name: t('mockCompare.compare4.product2'), price: 1200, image: getAssetUrl('ebike.jpg') },
      { name: t('mockCompare.compare4.product3'), price: 800, image: getAssetUrl('hoverboard.jpg') }
    ],
    creator: t('mockCompare.compare4.creator'),
    likes: 76
  }
]);
</script>

<style scoped>
.home-container {
  width: 100%;
  overflow-x: hidden;
}

/* 轮播图样式 */
.carousel-section {
  width: 100%;
  margin-bottom: 40px;
  position: relative;
}

.el-carousel {
  width: 100%;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.carousel-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 30px;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  color: white;
  border-radius: 0 0 8px 8px;
}

.carousel-caption h3 {
  font-size: 24px;
  margin-bottom: 10px;
}

.carousel-caption p {
  font-size: 16px;
  margin-bottom: 20px;
}

/* 功能导航样式 */
.feature-nav {
  display: flex;
  justify-content: space-around;
  margin: 0 auto 40px;
  max-width: 1200px;
  padding: 0 20px;
}

.feature-item {
  text-align: center;
  width: 150px;
}

.feature-item a {
  display: block;
  text-decoration: none;
  color: #333;
  transition: all 0.3s;
}

.feature-item a:hover {
  transform: translateY(-5px);
  color: #409eff;
}

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 10px;
  border-radius: 50%;
  background-color: #f0f9ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: #409eff;
}

.feature-text {
  font-size: 16px;
  font-weight: 500;
}

/* 通用区域样式 */
.section-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto 60px;
  padding: 0 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px 0;
  border-bottom: 2px solid #409eff;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.section-more {
  color: #409eff;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s;
}

.section-more:hover {
  color: #66b1ff;
}

.bg-gray {
  background-color: #f9f9f9;
  padding: 40px 0;
  margin: 60px 0;
}

/* 商品列表样式 */
.item-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
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
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

/* 求购列表样式 */
.request-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.request-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  text-decoration: none;
  color: #333;
  transition: all 0.3s;
}

.request-item:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  transform: translateX(5px);
}

.request-info {
  flex: 1;
  margin-right: 20px;
}

.request-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #333;
}

.request-content {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.request-tags {
  display: flex;
  gap: 8px;
}

.request-meta {
  text-align: right;
}

.price-range {
  font-size: 16px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.time-posted {
  font-size: 12px;
  color: #999;
}

/* 比价任务样式 */
.compare-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.compare-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s;
}

.compare-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

.compare-link {
  display: block;
  text-decoration: none;
  color: #333;
  padding: 15px;
}

.compare-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.compare-title {
  font-size: 16px;
  font-weight: 500;
  margin: 0;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.compare-count {
  font-size: 12px;
  color: #409eff;
  background-color: #ecf5ff;
  padding: 2px 8px;
  border-radius: 12px;
  margin-left: 10px;
}

.compare-products {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.product-mini {
  flex: 1;
  text-align: center;
}

.mini-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 5px;
}

.mini-price {
  font-size: 14px;
  font-weight: bold;
  color: #ff4d4f;
}

.product-more {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background-color: #f0f0f0;
  border-radius: 4px;
  font-size: 14px;
  color: #666;
}

.compare-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

/* 平台优势样式 */
.advantages-section {
  background-color: #f0f9ff;
  padding: 60px 0;
  margin: 60px 0;
}

.advantages-section .section-container {
  margin-bottom: 0;
}

.advantages-section .section-header {
  text-align: center;
  border-bottom: none;
  margin-bottom: 40px;
}

.advantages-section .section-title {
  color: #409eff;
}

.advantage-item {
  text-align: center;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: all 0.3s;
}

.advantage-item:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  transform: translateY(-5px);
}

.advantage-icon {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 20px;
}

.advantage-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #333;
}

.advantage-description {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

/* 统计数据样式 */
.stats-section {
  background-color: #409eff;
  color: white;
  padding: 40px 0;
}

.stats-section .section-container {
  margin-bottom: 0;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 16px;
  opacity: 0.9;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .section-container {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .carousel-section {
    margin-bottom: 30px;
  }
  
  .carousel-caption {
    padding: 20px;
  }
  
  .carousel-caption h3 {
    font-size: 20px;
  }
  
  .carousel-caption p {
    font-size: 14px;
  }
  
  .feature-nav {
    flex-wrap: wrap;
    margin-bottom: 30px;
  }
  
  .feature-item {
    width: 45%;
    margin-bottom: 20px;
  }
  
  .section-container {
    margin-bottom: 40px;
  }
  
  .section-title {
    font-size: 20px;
  }
  
  .item-list {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
  
  .request-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .request-info {
    margin-right: 0;
    margin-bottom: 15px;
  }
  
  .request-meta {
    text-align: left;
  }
  
  .compare-list {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
  
  .advantages-section {
    padding: 40px 0;
    margin: 40px 0;
  }
  
  .advantage-item {
    margin-bottom: 20px;
  }
  
  .stat-number {
    font-size: 28px;
  }
  
  .stat-label {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .carousel-image {
    height: 200px;
  }
  
  .carousel-caption {
    padding: 15px;
  }
  
  .carousel-caption h3 {
    font-size: 18px;
  }
  
  .carousel-caption p {
    font-size: 12px;
    margin-bottom: 15px;
  }
  
  .feature-item {
    width: 100%;
  }
  
  .item-list,
  .compare-list {
    grid-template-columns: 1fr;
  }
  
  .advantages-section {
    padding: 30px 0;
    margin: 30px 0;
  }
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.item-card,
.request-item,
.compare-card,
.advantage-item {
  animation: fadeInUp 0.5s ease-out;
}

.item-card:nth-child(1),
.request-item:nth-child(1),
.compare-card:nth-child(1),
.advantage-item:nth-child(1) {
  animation-delay: 0.1s;
}

.item-card:nth-child(2),
.request-item:nth-child(2),
.compare-card:nth-child(2),
.advantage-item:nth-child(2) {
  animation-delay: 0.2s;
}

.item-card:nth-child(3),
.request-item:nth-child(3),
.compare-card:nth-child(3),
.advantage-item:nth-child(3) {
  animation-delay: 0.3s;
}

.item-card:nth-child(4),
.request-item:nth-child(4),
.compare-card:nth-child(4),
.advantage-item:nth-child(4) {
  animation-delay: 0.4s;
}
</style>