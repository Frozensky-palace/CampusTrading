<template>
  <div class="rent-detail-container">
    <el-breadcrumb separator="/" class="breadcrumb">
      <el-breadcrumb-item><router-link to="/">{{ $t('rent.breadcrumb.home') }}</router-link></el-breadcrumb-item>
      <el-breadcrumb-item><router-link to="/rent/list">{{ $t('rent.breadcrumb.rentList') }}</router-link></el-breadcrumb-item>
      <el-breadcrumb-item>{{ rentItem.name }}</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 物品详情 -->
    <div class="item-detail">
      <!-- 物品图片 -->
      <div class="item-images">
        <img :src="rentItem.image" :alt="rentItem.name" class="main-image">
        <div class="thumbnails">
          <img
            v-for="(thumb, index) in rentItem.images"
            :key="index"
            :src="thumb"
            :alt="rentItem.name"
            class="thumbnail"
            @click="setMainImage(thumb)"
          >
        </div>
      </div>

      <!-- 物品信息 -->
      <div class="item-info">
        <h1 class="item-name">{{ rentItem.name }}</h1>
        <div class="item-price-section">
          <div class="price">
            <span class="currency">¥</span>
            <span class="price-value">{{ rentItem.rental_price_day }}</span>
            <span class="price-unit">{{ $t('rent.perDay') }}</span>
            <span v-if="rentItem.rental_price_week" class="price-option">
              ¥{{ rentItem.rental_price_week }}{{ $t('rent.perWeek') }}
            </span>
            <span v-if="rentItem.rental_price_month" class="price-option">
              ¥{{ rentItem.rental_price_month }}{{ $t('rent.perMonth') }}
            </span>
          </div>
          <div class="deposit">{{ $t('rent.deposit') }}: ¥{{ rentItem.deposit }}</div>
        </div>

        <div class="item-meta">
          <div class="meta-item">
            <span class="meta-label">{{ $t('rent.category') }}:</span>
            <span class="meta-value">{{ getCategoryName(rentItem.category) }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">{{ $t('rent.location') }}:</span>
            <span class="meta-value">{{ rentItem.location }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">{{ $t('rent.publishTime') }}:</span>
            <span class="meta-value">{{ formatDate(rentItem.createTime) }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">{{ $t('rent.status') }}:</span>
            <span :class="['meta-value', rentItem.available ? 'available' : 'unavailable']">
              {{ rentItem.available ? $t('rent.available') : $t('rent.rented') }}
            </span>
          </div>
        </div>

        <!-- 租赁时间选择 -->
        <div class="rental-time">
          <div class="time-label">{{ $t('rent.rentalTime') }}</div>
          <el-date-picker
            v-model="startDate"
            type="date"
            :placeholder="$t('rent.startDate')"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            class="date-picker"
          />
          <span class="time-separator">{{ $t('rent.to') }}</span>
          <el-date-picker
            v-model="endDate"
            type="date"
            :placeholder="$t('rent.endDate')"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            class="date-picker"
          />
          <div class="rental-days" v-if="startDate && endDate">
            {{ $t('rent.totalDays', { days: getRentalDays(), price: getTotalPrice() }) }}
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button type="danger" size="large" @click="contactOwner" class="contact-btn">
            <i class="el-icon-phone"></i> {{ $t('rent.contactOwner') }}
          </el-button>
          <el-button type="primary" size="large" @click="applyForRental" class="rent-btn" :disabled="!rentItem.available || !canApply">
            {{ rentItem.available ? $t('rent.rentNow') : $t('rent.alreadyRented') }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- 物品详细描述 -->
    <div class="item-description">
      <h2>{{ $t('rent.itemDescription') }}</h2>
      <div class="description-content" v-html="rentItem.description"></div>
    </div>

    <!-- 租赁须知 -->
    <div class="rental-notice">
      <h2>{{ $t('rent.rentalNotice') }}</h2>
      <ul>
        <li>{{ $t('rent.notices.checkCondition') }}</li>
        <li>{{ $t('rent.notices.returnOnTime') }}</li>
        <li>{{ $t('rent.notices.keepSafe') }}</li>
        <li>{{ $t('rent.notices.depositReturn') }}</li>
        <li>{{ $t('rent.notices.extendContact') }}</li>
      </ul>
    </div>

    <!-- 出租方信息 -->
    <div class="owner-info">
      <h2>{{ $t('rent.ownerInfo') }}</h2>
      <div class="owner-details">
        <img :src="rentItem.ownerAvatar" :alt="$t('rent.ownerInfo')" class="owner-avatar">
        <div class="owner-meta">
          <div class="owner-name">{{ rentItem.ownerName }}</div>
          <div class="owner-rating">
            <span class="rating-label">{{ $t('rent.creditScore') }}:</span>
            <el-rate v-model="rentItem.ownerRating" disabled show-score />
          </div>
          <div class="owner-stats">
            <span>{{ $t('rent.rentedTimes', { count: rentItem.rentalCount }) }}</span>
            <span>{{ $t('rent.positiveRate', { rate: rentItem.reviewRate }) }}</span>
          </div>
        </div>
        <el-button type="default" class="view-profile-btn">{{ $t('rent.viewProfile') }}</el-button>
      </div>
    </div>

    <!-- 相关推荐 -->
    <div class="related-items">
      <h2>{{ $t('rent.relatedItems') }}</h2>
      <div class="related-grid">
        <div class="related-item" v-for="item in relatedItems" :key="item.id">
          <router-link :to="`/rent/detail/${item.id}`" class="related-link">
            <img :src="item.image" :alt="item.name" class="related-image">
            <div class="related-name">{{ item.name }}</div>
            <div class="related-price">¥{{ item.rental_price_day }}{{ $t('rent.perDay') }}</div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { getRentItemDetail, applyForRental as applyForRentalAPI } from '@/api/rent';
import { ElMessage, ElMessageBox } from 'element-plus';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const itemId = ref(Number(route.params.id));

// 获取静态资源路径的帮助函数
const getAssetUrl = (path: string) => {
  return new URL(`../assets/images/${path}`, import.meta.url).href;
};

// 租赁物品数据
interface RentItemDetail {
  id: number;
  name: string;
  image: string;
  images: string[];
  rental_price_day: number;
  rental_price_week?: number;
  rental_price_month?: number;
  deposit: number;
  location: string;
  available: boolean;
  category: string;
  description: string;
  createTime: string;
  ownerId: number;
  ownerName: string;
  ownerAvatar: string;
  ownerRating: number;
  rentalCount: number;
  reviewRate: number;
  max_rental_days?: number;
}

// 模拟租赁详情数据
const mockRentItemDetail: RentItemDetail = {
  id: itemId.value || 1,
  name: '专业相机Canon EOS R5',
  image: getAssetUrl('camera.webp'),
  images: [
    getAssetUrl('camera.webp'),
    getAssetUrl('camera.webp'),
    getAssetUrl('camera.webp')
  ],
  rental_price_day: 150,
  rental_price_week: 900,
  rental_price_month: 3000,
  deposit: 3000,
  location: '主校区',
  available: true,
  category: 'electronics',
  description: `
    <p>Canon EOS R5是一款专业全画幅无反相机，配备4500万像素传感器，支持8K视频录制。</p>
    <p>相机状况良好，快门次数低于10000次，无任何划痕或损坏。</p>
    <p>配件包括：</p>
    <ul>
      <li>原装电池2块</li>
      <li>充电器</li>
      <li>相机包</li>
      <li>128GB SD卡</li>
      <li>说明书</li>
    </ul>
    <p>适合摄影课程作业、毕业拍摄、活动记录等场景使用。</p>
  `,
  createTime: '2023-05-15T08:30:00',
  ownerId: 101,
  ownerName: '摄影爱好者小张',
  ownerAvatar: getAssetUrl('camera.webp'),
  ownerRating: 4.8,
  rentalCount: 12,
  reviewRate: 96,
  max_rental_days: 30
}

// 模拟相关推荐数据
const mockRelatedItems = [
  {
    id: 2,
    name: '专业绘图板Wacom',
    image: getAssetUrl('tablet.webp'),
    images: [getAssetUrl('tablet.webp')],
    rental_price_day: 50,
    rental_price_week: 300,
    rental_price_month: 1000,
    deposit: 500,
    location: '主校区',
    available: true,
    category: 'electronics',
    description: '专业绘图板',
    createTime: '2023-05-20T10:00:00',
    ownerId: 102,
    ownerName: '创意设计小李',
    ownerAvatar: getAssetUrl('tablet.webp'),
    ownerRating: 4.7,
    rentalCount: 8,
    reviewRate: 94
  },
  {
    id: 3,
    name: '无人机DJI Mini 3',
    image: getAssetUrl('camera.webp'),
    images: [getAssetUrl('camera.webp')],
    rental_price_day: 200,
    rental_price_week: 1200,
    rental_price_month: 4000,
    deposit: 2000,
    location: '东校区',
    available: true,
    category: 'electronics',
    description: '入门级无人机',
    createTime: '2023-06-05T14:30:00',
    ownerId: 103,
    ownerName: '航拍爱好者小王',
    ownerAvatar: getAssetUrl('camera.webp'),
    ownerRating: 4.9,
    rentalCount: 5,
    reviewRate: 98
  },
  {
    id: 4,
    name: '拍立得相机富士Instax',
    image: getAssetUrl('camera.webp'),
    images: [getAssetUrl('camera.webp')],
    rental_price_day: 30,
    rental_price_week: 180,
    rental_price_month: 600,
    deposit: 200,
    location: '西校区',
    available: true,
    category: 'electronics',
    description: '拍立得相机',
    createTime: '2023-07-10T09:15:00',
    ownerId: 104,
    ownerName: '摄影爱好者小赵',
    ownerAvatar: getAssetUrl('camera.webp'),
    ownerRating: 4.6,
    rentalCount: 15,
    reviewRate: 92
  },
  {
    id: 5,
    name: '三脚架曼富图',
    image: getAssetUrl('camera.webp'),
    images: [getAssetUrl('camera.webp')],
    rental_price_day: 40,
    rental_price_week: 240,
    rental_price_month: 800,
    deposit: 300,
    location: '主校区',
    available: true,
    category: 'electronics',
    description: '专业三脚架',
    createTime: '2023-08-15T16:45:00',
    ownerId: 105,
    ownerName: '摄影爱好者小张',
    ownerAvatar: getAssetUrl('camera.webp'),
    ownerRating: 4.8,
    rentalCount: 10,
    reviewRate: 95
  }
];

// 响应式变量声明
const rentItem = ref<RentItemDetail>(mockRentItemDetail);
const relatedItems = ref<RentItemDetail[]>(mockRelatedItems);
const startDate = ref<string>('');
const endDate = ref<string>('');

// 获取租赁物品详情
const loadRentItemDetail = async () => {
  try {
    const res = await getRentItemDetail(itemId.value.toString());
    rentItem.value = res.data;
    
    // 加载相关推荐
    relatedItems.value = mockRelatedItems;
  } catch (error) {
    console.error(t('rent.loadDetailFailed'), error);
    // 加载失败时使用模拟数据
    rentItem.value = { ...mockRentItemDetail, id: itemId.value || 1 };
    relatedItems.value = mockRelatedItems;
  }
};

// 设置主图片
const setMainImage = (image: string) => {
  rentItem.value.image = image;
};

// 获取分类名称
const getCategoryName = (category: string) => {
  const categoryMap: Record<string, string> = {
    'electronics': t('rent.categories.electronics'),
    'sports': t('rent.categories.sports'),
    'music': t('rent.categories.music'),
    'books': t('rent.categories.books'),
    'other': t('rent.categories.other')
  };
  return categoryMap[category] || category;
};

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN');
};

// 计算租赁天数
const getRentalDays = () => {
  if (!startDate.value || !endDate.value) return 0;
  const start = new Date(startDate.value);
  const end = new Date(endDate.value);
  const diffTime = Math.abs(end.getTime() - start.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
  return diffDays;
};

// 计算租赁总价
const getTotalPrice = () => {
  const days = getRentalDays();
  const item = rentItem.value;
  let total = 0;
  
  if (days <= 0) return 0;
  
  // 根据租赁天数选择最合适的价格
  if (days >= 30 && item.rental_price_month) {
    const months = Math.floor(days / 30);
    const remainingDays = days % 30;
    total = (months * item.rental_price_month) + (remainingDays * item.rental_price_day);
  } else if (days >= 7 && item.rental_price_week) {
    const weeks = Math.floor(days / 7);
    const remainingDays = days % 7;
    total = (weeks * item.rental_price_week) + (remainingDays * item.rental_price_day);
  } else {
    total = days * item.rental_price_day;
  }
  
  return total;
};

// 检查是否可以申请租赁
const canApply = computed(() => {
  const days = getRentalDays();
  const item = rentItem.value;
  
  return startDate.value && endDate.value && 
         new Date(startDate.value) >= new Date() && 
         new Date(endDate.value) > new Date(startDate.value) &&
         // 检查是否超过最大租赁天数
         (!item.max_rental_days || days <= item.max_rental_days);
});

// 联系出租人
const contactOwner = () => {
  ElMessage({
    message: `${t('rent.contactCopied')}: ${rentItem.value.ownerName}`,
    type: 'success'
  });
};

// 申请租赁
const applyForRental = () => {
  if (!canApply.value) {
    ElMessage.warning(t('rent.selectValidTime'));
    return;
  }

  ElMessageBox.confirm(
    t('rent.confirmRentalMsg', {
      name: rentItem.value.name,
      start: startDate.value,
      end: endDate.value,
      days: getRentalDays(),
      deposit: rentItem.value.deposit
    }),
    t('rent.confirmRental'),
    {
      confirmButtonText: t('common.confirm'),
      cancelButtonText: t('common.cancel'),
      type: 'info'
    }
  ).then(async () => {
    try {
      await applyForRentalAPI({
        item_id: rentItem.value.id.toString(),
        rental_days: getRentalDays(),
        start_date: startDate.value,
        end_date: endDate.value,
        total_amount: getTotalPrice(),
        deposit: rentItem.value.deposit
      });
      ElMessage.success(t('rent.rentalSubmitted'));
      // 跳转到租赁订单页面
      setTimeout(() => {
        router.push('/rent/orders');
      }, 1500);
    } catch (error) {
      console.error(t('rent.applyFailed'), error);
      ElMessage.error(t('rent.rentalFailed'));
    }
  }).catch(() => {
    ElMessage.info(t('rent.rentalCancelled'));
  });
};

// 页面加载时初始化数据
onMounted(() => {
  loadRentItemDetail();
});
</script>

<style lang="scss" scoped>
.rent-detail-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
}

.breadcrumb {
  margin-bottom: 20px;
}

.item-detail {
  display: flex;
  gap: 40px;
  margin-bottom: 60px;
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.item-images {
  flex: 1;
  max-width: 500px;
}

.main-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 15px;
}

.thumbnails {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.thumbnail {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.3s ease;
}

.thumbnail:hover,
.thumbnail.active {
  border-color: #409eff;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 28px;
  font-weight: 500;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.4;
}

.item-price-section {
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.price {
  display: flex;
  align-items: baseline;
  margin-bottom: 10px;
}

.currency {
  font-size: 20px;
  color: #f56c6c;
  margin-right: 2px;
}

.price-value {
  font-size: 40px;
  font-weight: bold;
  color: #f56c6c;
}

.price-unit {
  font-size: 16px;
  color: #f56c6c;
  margin-left: 5px;
}

.deposit {
  font-size: 16px;
  color: #666;
}

.item-meta {
  margin-bottom: 30px;
}

.meta-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  font-size: 16px;
}

.meta-label {
  width: 80px;
  color: #999;
}

.meta-value {
  color: #333;
}

.available {
  color: #67c23a;
}

.unavailable {
  color: #f56c6c;
}

.rental-time {
  margin-bottom: 30px;
}

.time-label {
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
}

.rental-time {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.date-picker {
  width: 200px;
}

.time-separator {
  color: #999;
}

.rental-days {
  margin-top: 10px;
  margin-left: 0;
  color: #666;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 20px;
}

.contact-btn,
.rent-btn {
  flex: 1;
}

.item-description,
.rental-notice,
.owner-info,
.related-items {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.item-description h2,
.rental-notice h2,
.owner-info h2,
.related-items h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.description-content {
  font-size: 16px;
  line-height: 1.8;
  color: #666;
}

.description-content p {
  margin-bottom: 15px;
}

.description-content ul {
  margin-left: 20px;
  margin-bottom: 15px;
}

.description-content li {
  margin-bottom: 8px;
  list-style-type: disc;
}

.rental-notice ul {
  font-size: 16px;
  line-height: 1.8;
  color: #666;
  margin-left: 20px;
}

.rental-notice li {
  margin-bottom: 10px;
  list-style-type: disc;
}

.owner-details {
  display: flex;
  align-items: center;
  gap: 30px;
}

.owner-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.owner-meta {
  flex: 1;
}

.owner-name {
  font-size: 20px;
  font-weight: 500;
  color: #333;
  margin-bottom: 10px;
}

.owner-rating {
  margin-bottom: 10px;
}

.rating-label {
  font-size: 16px;
  color: #666;
  margin-right: 10px;
}

.owner-stats {
  display: flex;
  gap: 30px;
  font-size: 14px;
  color: #999;
}

.view-profile-btn {
  min-width: 120px;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.related-item {
  background-color: #f5f7fa;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.related-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.related-link {
  display: block;
  text-decoration: none;
}

.related-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.related-name {
  padding: 10px 15px;
  font-size: 16px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-price {
  padding: 0 15px 15px;
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}

@media (max-width: 768px) {
  .item-detail {
    flex-direction: column;
    gap: 20px;
    padding: 20px;
  }
  
  .item-images {
    max-width: 100%;
  }
  
  .main-image {
    height: 250px;
  }
  
  .item-name {
    font-size: 24px;
  }
  
  .price-value {
    font-size: 32px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .owner-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
}
</style>