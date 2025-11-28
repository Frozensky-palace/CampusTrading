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
            <el-button type="primary" :href="item.link">立即查看</el-button>
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
        <h2 class="section-title">热门商品</h2>
        <router-link to="/items" class="section-more">查看更多 <el-icon><ArrowRight /></el-icon></router-link>
      </div>
      <div class="item-list">
        <div class="item-card" v-for="item in hotItems" :key="item.id">
          <router-link :to="`/items/${item.id}`" class="item-link">
            <div class="item-image">
              <img :src="item.image" :alt="item.name" class="image">
              <span v-if="item.discount" class="discount-badge">{{ item.discount }}折</span>
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
        <h2 class="section-title">最新求购</h2>
        <router-link to="/requests" class="section-more">查看更多 <el-icon><ArrowRight /></el-icon></router-link>
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
            <div class="price-range">预算: ¥{{ request.minPrice }} - ¥{{ request.maxPrice }}</div>
            <div class="time-posted">{{ formatTime(request.createdAt) }}</div>
          </div>
        </router-link>
      </div>
    </section>

    <!-- 比价任务区域 -->
    <section class="section-container">
      <div class="section-header">
        <h2 class="section-title">热门比价</h2>
        <router-link to="/compare" class="section-more">查看更多 <el-icon><ArrowRight /></el-icon></router-link>
      </div>
      <div class="compare-list">
        <div class="compare-card" v-for="task in hotCompareTasks" :key="task.id">
          <router-link :to="`/compare/detail/${task.id}`" class="compare-link">
            <div class="compare-header">
              <h3 class="compare-title">{{ task.title }}</h3>
              <span class="compare-count">{{ task.products.length }}个商品</span>
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
              <span class="creator">by {{ task.creator }}</span>
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
import { ref, onMounted } from 'vue';
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

// 轮播图数据
const carouselItems = ref([
  {
    image: '@/assets/images/banner1.jpg',
    title: '新学期特惠',
    description: '二手教材大促销，助力新学期学习',
    link: '/items?category=textbook'
  },
  {
    image: '@/assets/images/campus-digital-festival.jpg',
    title: '校园数码节',
    description: '数码产品低至5折，品质保证',
    link: '/items?category=digital'
  },
  {
    image: '@/assets/images/banner3.jpg',
    title: '毕业季特惠',
    description: '学长学姐低价转让，学弟学妹快来淘',
    link: '/items?tag=graduate'
  }
]);

// 功能导航数据
const features = ref([
  { id: 1, name: '发布商品', icon: CirclePlus, route: '/items/create' },
  { id: 2, name: '发布求购', icon: QuestionFilled, route: '/requests/create' },
  { id: 3, name: '发起比价', icon: Sort, route: '/compare/create' },
  { id: 4, name: '个人中心', icon: User, route: '/user/profile' }
]);

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

// 平台优势数据
const advantages = ref([
  {
    id: 1,
    icon: Lock,
    title: '安全交易',
    description: '实名认证，交易保障，让您放心购买'
  },
  {
    id: 2,
    icon: Lightning,
    title: '快速发布',
    description: '简单几步，轻松发布您的闲置物品'
  },
  {
    id: 3,
    icon: PriceTag,
    title: '高性价比',
    description: '校园内交易，省去中间环节，价格更优惠'
  },
  {
    id: 4,
    icon: Headset,
    title: '贴心服务',
    description: '专业客服团队，7x12小时为您服务'
  }
]);

// 统计数据
const stats = ref([
  { id: 1, value: '10,000+', label: '注册用户' },
  { id: 2, value: '5,000+', label: '在售商品' },
  { id: 3, value: '8,000+', label: '成功交易' },
  { id: 4, value: '98%', label: '好评率' }
]);

// 加载数据
onMounted(async () => {
  try {
    // 加载热门商品
    const itemsRes = await getHotItems({ limit: 8 });
    hotItems.value = itemsRes.data || mockHotItems;
    
    // 加载最新求购
    const requestsRes = await getLatestRequests({ limit: 5 });
    latestRequests.value = requestsRes.data || mockLatestRequests;
    
    // 加载热门比价任务
    const compareRes = await getHotCompareTasks({ limit: 4 });
    hotCompareTasks.value = compareRes.data || mockHotCompareTasks;
    
    // 加载平台统计数据
    const statsRes = await getPlatformStats();
    if (statsRes.data) {
      stats.value = [
        { id: 1, value: statsRes.data.userCount, label: '注册用户' },
        { id: 2, value: statsRes.data.itemCount, label: '在售商品' },
        { id: 3, value: statsRes.data.transactionCount, label: '成功交易' },
        { id: 4, value: statsRes.data.ratingRate, label: '好评率' }
      ];
    }
  } catch (error) {
    console.error('Failed to load home page data:', error);
    // 使用模拟数据
    hotItems.value = mockHotItems;
    latestRequests.value = mockLatestRequests;
    hotCompareTasks.value = mockHotCompareTasks;
  }
});

// 模拟热门商品数据
const mockHotItems = [
  {
    id: 1,
    name: '全新未拆封MacBook Pro 2022',
    image: '@/assets/images/macbook.jpg',
    price: 8999,
    originalPrice: 11999,
    discount: 7.5,
    location: '主校区',
    views: 238
  },
  {
    id: 2,
    name: '九成新iPad Pro 2021',
    image: '@/assets/images/ipad.jpg',
    price: 4500,
    originalPrice: 6299,
    location: '东校区',
    views: 196
  },
  {
    id: 3,
    name: '大学英语四六级词汇书',
    image: '@/assets/images/englishbook.jpg',
    price: 25,
    originalPrice: 58,
    discount: 4.3,
    location: '图书馆',
    views: 152
  },
  {
    id: 4,
    name: '考研数学复习全书',
    image: '/assets/images/mathbook.jpg',
    price: 35,
    originalPrice: 78,
    location: '西校区',
    views: 128
  },
  {
    id: 5,
    name: '篮球Nike NBA官方用球',
    image: '/assets/images/basketball.jpg',
    price: 80,
    originalPrice: 168,
    location: '体育馆',
    views: 96
  },
  {
    id: 6,
    name: '吉他初学者套装',
    image: '/assets/images/guitar.jpg',
    price: 199,
    originalPrice: 399,
    location: '音乐楼',
    views: 85
  },
  {
    id: 7,
    name: '专业绘图板Wacom',
    image: '/assets/images/tablet.jpg',
    price: 450,
    originalPrice: 899,
    location: '设计学院',
    views: 72
  },
  {
    id: 8,
    name: '校园自行车',
    image: '/assets/images/bike.jpg',
    price: 150,
    originalPrice: 350,
    location: '车棚',
    views: 65
  }
];

// 模拟最新求购数据
const mockLatestRequests = [
  {
    id: 1,
    title: '求购二手考研政治资料',
    content: '求购最新版考研政治全套资料，最好是2023年的，有笔记更好。',
    tags: ['考研', '政治', '资料'],
    minPrice: 50,
    maxPrice: 150,
    createdAt: new Date().getTime() - 3600000
  },
  {
    id: 2,
    title: '寻找二手专业相机',
    content: '求购一台入门级单反或微单相机，用于学习摄影课程，预算2000左右。',
    tags: ['相机', '摄影', '数码'],
    minPrice: 1500,
    maxPrice: 2500,
    createdAt: new Date().getTime() - 7200000
  },
  {
    id: 3,
    title: '求购二手电动车',
    content: '求购一辆二手电动车，电池续航至少30公里，有正规发票。',
    tags: ['电动车', '代步', '出行'],
    minPrice: 800,
    maxPrice: 1500,
    createdAt: new Date().getTime() - 10800000
  },
  {
    id: 4,
    title: '收购计算机专业教材',
    content: '收购计算机科学与技术专业大二教材，包括数据结构、操作系统等。',
    tags: ['教材', '计算机', '专业'],
    minPrice: 100,
    maxPrice: 300,
    createdAt: new Date().getTime() - 14400000
  },
  {
    id: 5,
    title: '求购二手空调',
    content: '求购一台1.5匹二手空调，制冷效果好，价格实惠。',
    tags: ['电器', '空调', '夏季'],
    minPrice: 800,
    maxPrice: 1200,
    createdAt: new Date().getTime() - 18000000
  }
];

// 模拟热门比价任务数据
const mockHotCompareTasks = [
  {
    id: 1,
    title: '2000元预算笔记本电脑推荐',
    products: [
      { name: '联想小新', price: 1999, image: '/assets/images/laptop1.jpg' },
      { name: '戴尔灵越', price: 2199, image: '/assets/images/laptop2.jpg' },
      { name: '惠普星系列', price: 1899, image: '/assets/images/laptop3.jpg' },
      { name: '华为MateBook', price: 2399, image: '/assets/images/laptop4.jpg' }
    ],
    creator: '数码达人',
    likes: 128
  },
  {
    id: 2,
    title: '校园周边美食性价比大比拼',
    products: [
      { name: '一号食堂', price: 15, image: '@/assets/images/food1.jpg' },
      { name: '校外小吃街', price: 25, image: '@/assets/images/food2.jpg' },
      { name: '外卖平台', price: 20, image: '@/assets/images/food3.jpg' }
    ],
    creator: '美食家',
    likes: 95
  },
  {
    id: 3,
    title: '考研辅导书最全对比',
    products: [
      { name: '张宇数学', price: 68, image: '@/assets/images/book1.jpg' },
      { name: '李永乐复习全书', price: 78, image: '@/assets/images/book2.jpg' },
      { name: '肖秀荣政治', price: 58, image: '@/assets/images/book3.jpg' },
      { name: '新东方英语', price: 98, image: '@/assets/images/book4.jpg' },
      { name: '启航考研', price: 65, image: '@/assets/images/book5.jpg' }
    ],
    creator: '考研学长',
    likes: 215
  },
  {
    id: 4,
    title: '校园代步工具对比',
    products: [
      { name: '自行车', price: 300, image: '@/assets/images/bike1.jpg' },
      { name: '电动车', price: 1200, image: '@/assets/images/ebike.jpg' },
      { name: '平衡车', price: 800, image: '@/assets/images/hoverboard.jpg' }
    ],
    creator: '校园生活家',
    likes: 76
  }
];
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