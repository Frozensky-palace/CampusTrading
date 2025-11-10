<template>
  <div class="rent-detail-container">
    <el-breadcrumb separator="/" class="breadcrumb">
      <el-breadcrumb-item><router-link to="/">首页</router-link></el-breadcrumb-item>
      <el-breadcrumb-item><router-link to="/rent/list">租赁列表</router-link></el-breadcrumb-item>
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
            :alt="rentItem.name + ' 缩略图'"
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
            <span class="price-value">{{ rentItem.price }}</span>
            <span class="price-unit">/天</span>
          </div>
          <div class="deposit">押金: ¥{{ rentItem.deposit }}</div>
        </div>
        
        <div class="item-meta">
          <div class="meta-item">
            <span class="meta-label">分类:</span>
            <span class="meta-value">{{ getCategoryName(rentItem.category) }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">位置:</span>
            <span class="meta-value">{{ rentItem.location }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">发布时间:</span>
            <span class="meta-value">{{ formatDate(rentItem.createTime) }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">状态:</span>
            <span :class="['meta-value', rentItem.available ? 'available' : 'unavailable']">
              {{ rentItem.available ? '可租' : '已租' }}
            </span>
          </div>
        </div>

        <!-- 租赁时间选择 -->
        <div class="rental-time">
          <div class="time-label">租赁时间</div>
          <el-date-picker
            v-model="startDate"
            type="date"
            placeholder="开始日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            class="date-picker"
          />
          <span class="time-separator">至</span>
          <el-date-picker
            v-model="endDate"
            type="date"
            placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            class="date-picker"
          />
          <div class="rental-days" v-if="startDate && endDate">
            共 {{ getRentalDays() }} 天，总价: ¥{{ getTotalPrice() }}
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button type="danger" size="large" @click="contactOwner" class="contact-btn">
            <i class="el-icon-phone"></i> 联系出租人
          </el-button>
          <el-button type="primary" size="large" @click="applyForRental" class="rent-btn" :disabled="!rentItem.available || !canApply">
            {{ rentItem.available ? '立即租赁' : '已被租赁' }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- 物品详细描述 -->
    <div class="item-description">
      <h2>物品描述</h2>
      <div class="description-content" v-html="rentItem.description"></div>
    </div>

    <!-- 租赁须知 -->
    <div class="rental-notice">
      <h2>租赁须知</h2>
      <ul>
        <li>请在租赁前确认物品的完好状态</li>
        <li>请按时归还物品，逾期将收取额外费用</li>
        <li>租赁期间请妥善保管物品，如有损坏需按价赔偿</li>
        <li>押金将在物品完好归还后全额退还</li>
        <li>如需延长租赁时间，请提前与出租人协商</li>
      </ul>
    </div>

    <!-- 出租方信息 -->
    <div class="owner-info">
      <h2>出租方信息</h2>
      <div class="owner-details">
        <img :src="rentItem.ownerAvatar" alt="出租方头像" class="owner-avatar">
        <div class="owner-meta">
          <div class="owner-name">{{ rentItem.ownerName }}</div>
          <div class="owner-rating">
            <span class="rating-label">信誉评分:</span>
            <el-rate v-model="rentItem.ownerRating" disabled show-score />
          </div>
          <div class="owner-stats">
            <span>已出租 {{ rentItem.rentalCount }} 次</span>
            <span>好评率 {{ rentItem.reviewRate }}%</span>
          </div>
        </div>
        <el-button type="default" class="view-profile-btn">查看个人主页</el-button>
      </div>
    </div>

    <!-- 相关推荐 -->
    <div class="related-items">
      <h2>相关推荐</h2>
      <div class="related-grid">
        <div class="related-item" v-for="item in relatedItems" :key="item.id">
          <router-link :to="`/rent/detail/${item.id}`" class="related-link">
            <img :src="item.image" :alt="item.name" class="related-image">
            <div class="related-name">{{ item.name }}</div>
            <div class="related-price">¥{{ item.price }}/天</div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getRentItemDetail } from '@/api/rent';

const route = useRoute();
const router = useRouter();
const itemId = ref(Number(route.params.id));

// 租赁物品数据
interface RentItemDetail {
  id: number;
  name: string;
  image: string;
  images: string[];
  price: number;
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
}

const rentItem = ref<RentItemDetail>({
  id: 0,
  name: '',
  image: '',
  images: [],
  price: 0,
  deposit: 0,
  location: '',
  available: false,
  category: '',
  description: '',
  createTime: '',
  ownerId: 0,
  ownerName: '',
  ownerAvatar: '',
  ownerRating: 0,
  rentalCount: 0,
  reviewRate: 0
});

// 租赁时间
const startDate = ref<string>('');
const endDate = ref<string>('');

// 相关推荐物品
const relatedItems = ref<any[]>([]);

// 模拟租赁详情数据
const mockRentItemDetail: RentItemDetail = {
  id: itemId.value || 1,
  name: '专业相机Canon EOS R5',
  image: '/assets/images/camera.jpg',
  images: [
    '/assets/images/camera.jpg',
    '/assets/images/camera2.jpg',
    '/assets/images/camera3.jpg'
  ],
  price: 150,
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
  ownerAvatar: '/assets/images/avatar1.jpg',
  ownerRating: 4.8,
  rentalCount: 12,
  reviewRate: 96
};

// 模拟相关推荐数据
const mockRelatedItems = [
  {
    id: 2,
    name: '专业绘图板Wacom',
    image: '/assets/images/tablet.jpg',
    price: 50
  },
  {
    id: 3,
    name: '无人机DJI Mini 3',
    image: '/assets/images/drone.jpg',
    price: 200
  },
  {
    id: 4,
    name: '拍立得相机富士Instax',
    image: '/assets/images/instax.jpg',
    price: 30
  },
  {
    id: 5,
    name: '三脚架曼富图',
    image: '/assets/images/tripod.jpg',
    price: 40
  }
];

// 获取租赁物品详情
const loadRentItemDetail = async () => {
  try {
    // 在实际项目中，这里应该调用API获取数据
    // const res = await getRentItemDetail(itemId.value);
    // rentItem.value = res.data;
    
    // 使用模拟数据
    rentItem.value = { ...mockRentItemDetail, id: itemId.value || 1 };
    
    // 加载相关推荐
    relatedItems.value = mockRelatedItems;
  } catch (error) {
    console.error('加载租赁物品详情失败:', error);
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
    'electronics': '电子产品',
    'sports': '体育用品',
    'music': '乐器',
    'books': '书籍',
    'other': '其他'
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
  return days * rentItem.value.price;
};

// 检查是否可以申请租赁
const canApply = computed(() => {
  return startDate.value && endDate.value && 
         new Date(startDate.value) >= new Date() && 
         new Date(endDate.value) > new Date(startDate.value);
});

// 联系出租人
const contactOwner = () => {
  ElMessage({ 
    message: `已复制出租人联系方式: ${rentItem.value.ownerName} (虚拟联系方式)`, 
    type: 'success' 
  });
};

// 申请租赁
const applyForRental = () => {
  if (!canApply.value) {
    ElMessage.warning('请选择有效的租赁时间');
    return;
  }
  
  ElMessageBox.confirm(
    `您确定要租赁${rentItem.value.name}，从${startDate.value}至${endDate.value}，共${getRentalDays()}天，总价¥${getTotalPrice()}，押金¥${rentItem.value.deposit}吗？`,
    '确认租赁',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(() => {
    // 实际项目中，这里应该调用API提交租赁申请
    ElMessage.success('租赁申请已提交，请等待出租人确认');
    // 跳转到租赁订单页面
    setTimeout(() => {
      router.push('/rent/orders');
    }, 1500);
  }).catch(() => {
    ElMessage.info('已取消租赁申请');
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