<template>
  <div class="item-detail-container">
    <!-- 面包屑导航 -->
    <div class="breadcrumb">
      <el-breadcrumb separator="/">
          <el-breadcrumb-item><router-link to="/">{{ $t('item.detail.breadcrumbHome') }}</router-link></el-breadcrumb-item>
          <el-breadcrumb-item><router-link to="/items">{{ $t('item.detail.breadcrumbList') }}</router-link></el-breadcrumb-item>
          <el-breadcrumb-item :to="`/items?category=${item.category}`">{{ getCategoryName(item.category) }}</el-breadcrumb-item>
          <el-breadcrumb-item>{{ item.name }}</el-breadcrumb-item>
        </el-breadcrumb>
    </div>

    <!-- 商品信息卡片 -->
    <div class="item-card">
      <!-- 商品图片区域 -->
      <div class="item-images">
        <el-image-viewer
          v-if="showViewer"
          :url-list="imageList"
          @close="showViewer = false"
        />
        <div class="main-image">
          <img :src="item.image" :alt="item.name" @click="showViewer = true" class="image">
          <span v-if="item.discount" class="discount-badge">{{ item.discount }}{{ $t('item.list.discount') }}</span>
          <span v-if="item.status === 'sold'" class="sold-badge">{{ $t('item.list.soldOut') }}</span>
        </div>
        <div class="image-preview" v-if="imageList.length > 1">
          <div class="preview-item" v-for="(img, index) in imageList" :key="index">
            <img :src="img" :alt="`${item.name}图片${index+1}`" @click="showViewer = true; currentImageIndex = index" class="preview-image">
          </div>
        </div>
      </div>

      <!-- 商品基本信息 -->
      <div class="item-basic-info">
        <h1 class="item-name">{{ item.name }}</h1>
        <div class="item-rating">
          <el-rate v-model="item.rating" :max="5" disabled show-score score-template="{{ value }}分"></el-rate>
          <span class="review-count">({{ item.reviewCount }}{{ $t('item.detail.reviews') }})</span>
        </div>
        <div class="item-price-section">
          <div class="price-container">
            <span class="price-label">{{ $t('item.detail.priceLabel') }}</span>
            <span class="price">¥{{ item.price }}</span>
            <span v-if="item.originalPrice" class="original-price">¥{{ item.originalPrice }}</span>
          </div>
          <div class="price-info">
            <span class="view-count"><i class="el-icon-view"></i>{{ item.views }}{{ $t('item.detail.viewCount') }}</span>
            <span class="publish-time"><i class="el-icon-clock"></i>{{ formatTime(item.createdAt) }}</span>
          </div>
        </div>
        <div class="item-meta">
          <div class="meta-item">
            <span class="meta-label">{{ $t('item.detail.itemStatus') }}</span>
            <span class="meta-value" :class="getStatusClass(item.status)">{{ getStatusText(item.status) }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">{{ $t('item.detail.itemCondition') }}</span>
            <span class="meta-value">{{ item.condition || $t('item.detail.notFilled') }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">{{ $t('item.detail.tradeLocation') }}</span>
            <span class="meta-value">{{ item.location || $t('item.detail.notFilled') }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">{{ $t('item.detail.itemTags') }}</span>
            <div class="tags-container">
              <el-tag v-for="tag in item.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
            </div>
          </div>
        </div>
        <div class="action-buttons">
          <el-button type="primary" size="large" @click="contactSeller" :disabled="item.status === 'sold'">{{ item.status === 'sold' ? $t('item.detail.itemSold') : $t('item.contactSeller') }}</el-button>
          <el-button type="default" size="large" @click="addToFavorite" :icon="isFavorite ? 'el-icon-star-on' : 'el-icon-star-off'">{{ isFavorite ? $t('item.detail.favorited') : $t('item.detail.favorite') }}</el-button>
          <el-button type="default" size="large" @click="shareItem"><i class="el-icon-share"></i>{{ $t('item.share') }}</el-button>
        </div>
      </div>
    </div>

    <!-- 商品详细信息 -->
    <div class="item-detail-section">
      <div class="detail-tabs">
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane :label="$t('item.detail.tabDetail')" name="detail"></el-tab-pane>
          <el-tab-pane :label="$t('item.detail.tabReviews')" name="reviews"></el-tab-pane>
          <el-tab-pane :label="$t('item.detail.tabSeller')" name="seller"></el-tab-pane>
        </el-tabs>
      </div>

      <!-- 商品详情内容 -->
      <div v-if="activeTab === 'detail'" class="detail-content">
        <div class="detail-description">
          <h3>{{ $t('item.detail.itemDescription') }}</h3>
          <div class="description-content" v-html="item.description"></div>
        </div>
        <div class="detail-specs">
          <h3>{{ $t('item.detail.itemSpecs') }}</h3>
          <table class="specs-table">
            <tr v-for="(value, key) in item.specs" :key="key">
              <td class="spec-key">{{ key }}</td>
              <td class="spec-value">{{ value }}</td>
            </tr>
          </table>
        </div>
        <div class="detail-shipping">
          <h3>{{ $t('item.detail.tradeMethods') }}</h3>
          <div class="shipping-methods">
            <div class="shipping-item" v-for="method in item.shippingMethods" :key="method">
              <i class="el-icon-check"></i>
              <span>{{ method }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 用户评价内容 -->
      <div v-if="activeTab === 'reviews'" class="reviews-content">
        <div class="reviews-summary">
          <div class="rating-overview">
            <div class="overall-score">
              <span class="score">{{ item.rating }}</span>
              <span class="score-label">{{ $t('item.detail.overallScore') }}</span>
            </div>
            <div class="rating-details">
              <div class="rating-item" v-for="(count, star) in ratingDistribution" :key="star">
                <span class="star-label">{{ star }}{{ $t('item.detail.stars') }}</span>
                <el-progress :percentage="count / totalReviews * 100" :show-text="false"></el-progress>
                <span class="count">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="reviews-list">
          <div class="review-item" v-for="review in reviews" :key="review.id">
            <div class="review-header">
              <img :src="review.userAvatar" :alt="review.userName" class="user-avatar">
              <div class="user-info">
                <span class="user-name">{{ review.userName }}</span>
                <el-rate v-model="review.rating" :max="5" disabled size="small"></el-rate>
                <span class="review-time">{{ formatTime(review.createdAt) }}</span>
              </div>
            </div>
            <div class="review-content">{{ review.content }}</div>
            <div class="review-images" v-if="review.images && review.images.length > 0">
              <img v-for="(img, index) in review.images" :key="index" :src="img" :alt="`Review image ${index+1}`" class="review-image">
            </div>
          </div>
        </div>
        <div v-if="reviews.length === 0" class="no-reviews">
          <el-empty :description="$t('item.detail.noReviews')" />
        </div>
      </div>

      <!-- 卖家信息内容 -->
      <div v-if="activeTab === 'seller'" class="seller-content">
        <div class="seller-info">
          <img :src="seller.avatar" :alt="seller.name" class="seller-avatar">
          <div class="seller-details">
            <h3 class="seller-name">{{ seller.name }}</h3>
            <div class="seller-stats">
              <span class="stat-item"><i class="el-icon-goods"></i>{{ $t('item.detail.sellerOnSale') }}{{ seller.activeItems }}{{ $t('item.detail.sellerItems') }}</span>
              <span class="stat-item"><i class="el-icon-success"></i>{{ $t('item.detail.sellerPositiveRate') }}{{ seller.ratingRate }}%</span>
              <span class="stat-item"><i class="el-icon-time"></i>{{ $t('item.detail.registeredAt') }}{{ formatYear(seller.registeredAt) }}</span>
            </div>
            <div class="seller-tags">
              <el-tag v-for="tag in seller.tags" :key="tag" size="small">{{ tag }}</el-tag>
            </div>
          </div>
          <div class="seller-actions">
            <el-button type="primary" @click="contactSeller">{{ $t('item.contactSeller') }}</el-button>
            <el-button type="default" @click="viewSellerProfile">{{ $t('item.detail.viewShop') }}</el-button>
          </div>
        </div>
        <div class="seller-other-items">
          <h3>{{ $t('item.detail.sellerOtherItems') }}</h3>
          <div class="other-items-list">
            <router-link :to="`/items/${otherItem.id}`" class="other-item" v-for="otherItem in seller.otherItems" :key="otherItem.id">
              <img :src="otherItem.image" :alt="otherItem.name" class="other-item-image">
              <span class="other-item-name">{{ otherItem.name }}</span>
              <span class="other-item-price">¥{{ otherItem.price }}</span>
            </router-link>
          </div>
          <div v-if="seller.otherItems.length === 0" class="no-other-items">
            <el-empty :description="$t('item.detail.noOtherItems')" />
          </div>
        </div>
      </div>
    </div>

    <!-- 相关推荐 -->
    <div class="recommendations-section">
      <h3>{{ $t('item.detail.youMayLike') }}</h3>
      <div class="recommendations-list">
        <router-link :to="`/items/${recItem.id}`" class="recommendation-item" v-for="recItem in recommendations" :key="recItem.id">
          <img :src="recItem.image" :alt="recItem.name" class="rec-image">
          <span class="rec-name">{{ recItem.name }}</span>
          <span class="rec-price">¥{{ recItem.price }}</span>
        </router-link>
      </div>
    </div>

    <!-- 加载中 -->
    <el-loading v-if="loading" :target="'.item-detail-container'" fullscreen />

    <!-- 联系卖家弹窗 -->
    <el-dialog v-model="contactDialogVisible" :title="$t('item.detail.contactSellerTitle')" width="600px">
      <div class="contact-form">
        <div class="seller-contact-info">
          <p><strong>{{ $t('item.detail.sellerLabel') }}</strong>{{ seller.name }}</p>
          <p><strong>{{ $t('item.detail.phoneLabel') }}</strong>{{ seller.phone || $t('item.detail.notSet') }}</p>
          <p><strong>{{ $t('item.detail.wechatLabel') }}</strong>{{ seller.wechat || $t('item.detail.notSet') }}</p>
          <p><strong>{{ $t('item.detail.qqLabel') }}</strong>{{ seller.qq || $t('item.detail.notSet') }}</p>
        </div>
        <div class="contact-message">
          <el-input
            v-model="contactMessage"
            type="textarea"
            :rows="4"
            :placeholder="$t('item.detail.enterMessage')"
          ></el-input>
        </div>
      </div>
      <template #footer>
        <el-button @click="contactDialogVisible = false">{{ $t('common.cancel') }}</el-button>
        <el-button type="primary" @click="sendMessage">{{ $t('item.detail.sendMessage') }}</el-button>
      </template>
    </el-dialog>

    <!-- 分享弹窗 -->
    <el-dialog v-model="shareDialogVisible" :title="$t('item.detail.shareItem')" width="400px">
      <div class="share-content">
        <div class="share-link">
          <el-input v-model="shareUrl" readonly></el-input>
          <el-button type="primary" @click="copyShareUrl">{{ $t('item.detail.copyLink') }}</el-button>
        </div>
        <div class="share-qrcode">
          <div class="qrcode-image">
            <!-- 这里应该是二维码图片，暂时用占位符 -->
            <div class="qrcode-placeholder">{{ $t('item.detail.qrcode') }}</div>
          </div>
          <p class="qrcode-text">{{ $t('item.detail.scanToShare') }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import { getItemDetail, favoriteItem, unfavoriteItem, getRecommendedItems } from '@/api/item';
import { formatTime, formatYear } from '@/utils/common';
import { ElMessage } from 'element-plus';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// 路由参数
const route = useRoute();
const itemId = computed(() => route.params.id as string);

// 定义类型
interface Item {
  id: string;
  name: string;
  image: string;
  price: number;
  originalPrice: number;
  discount: number;
  description: string;
  category: string;
  status: string;
  condition: string;
  location: string;
  tags: string[];
  views: number;
  createdAt: number;
  rating: number;
  reviewCount: number;
  specs: Record<string, string>;
  shippingMethods: string[];
  sellerId?: string;
}

// 组件状态
const loading = ref(false);
const item = ref<Item>({
  id: '',
  name: '',
  image: '',
  price: 0,
  originalPrice: 0,
  discount: 0,
  description: '',
  category: '',
  status: 'available',
  condition: '',
  location: '',
  tags: [],
  views: 0,
  createdAt: 0,
  rating: 0,
  reviewCount: 0,
  specs: {},
  shippingMethods: []
});

const imageList = ref<string[]>([]);
const showViewer = ref(false);
const currentImageIndex = ref(0);
const isFavorite = ref(false);
const activeTab = ref('detail');
const contactDialogVisible = ref(false);
const shareDialogVisible = ref(false);
const contactMessage = ref('');
const shareUrl = ref('');

// 定义类型
interface OtherItem {
  id: string;
  name: string;
  image: string;
  price: number;
}

interface Seller {
  id: string;
  name: string;
  avatar: string;
  activeItems: number;
  ratingRate: number;
  registeredAt: number;
  tags: string[];
  phone: string;
  wechat: string;
  qq: string;
  otherItems: OtherItem[];
}

interface Review {
  id: string;
  userName: string;
  userAvatar: string;
  rating: number;
  content: string;
  createdAt: number;
  images: string[];
}

interface Recommendation {
  id: string;
  name: string;
  image: string;
  price: number;
}

// 卖家信息
const seller = ref<Seller>({
  id: '',
  name: '',
  avatar: '',
  activeItems: 0,
  ratingRate: 0,
  registeredAt: 0,
  tags: [],
  phone: '',
  wechat: '',
  qq: '',
  otherItems: []
});

// 评价信息
const reviews = ref<Review[]>([]);
const ratingDistribution = ref({ 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 });
const totalReviews = ref(0);

// 推荐商品
const recommendations = ref<Recommendation[]>([]);

// 辅助函数
const getCategoryName = (category: string): string => {
  const categoryMap: Record<string, string> = {
    digital: t('item.categories.digital'),
    textbook: t('item.categories.textbook'),
    home: t('item.categories.home'),
    sports: t('item.categories.sports'),
    clothing: t('item.categories.clothing'),
    others: t('item.categories.others')
  };
  return categoryMap[category] || t('item.categories.others');
};

const getStatusText = (status: string): string => {
  return status === 'available' ? t('item.list.onSale') : t('item.list.soldOut');
};

const getStatusClass = (status: string): string => {
  return status === 'available' ? 'status-available' : 'status-sold';
};

// 加载商品详情
const loadItemDetail = async () => {
  loading.value = true;
  try {
    const response = await getItemDetail(itemId.value);
    item.value = response.data || mockItem;
    
    // 设置图片列表
    if (item.value.image) {
      imageList.value = [item.value.image];
      // 这里应该从API获取更多图片，但现在用模拟数据
      if (mockItemImages.length > 0) {
        imageList.value = [...imageList.value, ...mockItemImages];
      }
    }
    
    // 设置卖家信息
    seller.value = response.data?.seller || mockSeller;
    
    // 设置评价信息
    reviews.value = response.data?.reviews || mockReviews;
    
    // 计算评分分布
    calculateRatingDistribution();
    
    // 检查是否已收藏
    isFavorite.value = response.data?.isFavorite || false;

    // 生成分享链接
    shareUrl.value = `${window.location.origin}/#/items/${itemId.value}`;
  } catch (error) {
    console.error('Failed to load item detail:', error);
    ElMessage.error(t('item.detail.loadFailed'));
    // 使用模拟数据
    item.value = mockItem;
    imageList.value = [mockItem.image, ...mockItemImages];
    seller.value = mockSeller;
    reviews.value = mockReviews;
    calculateRatingDistribution();
  } finally {
    loading.value = false;
  }
};

// 计算评分分布
const calculateRatingDistribution = () => {
  const distribution = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
  reviews.value.forEach((review) => {
    const rating = Math.max(1, Math.min(5, review.rating)); // 确保评分在1-5之间
    distribution[rating as keyof typeof distribution]++;
  });
  ratingDistribution.value = distribution;
  totalReviews.value = reviews.value.length;
};

// 加载相关推荐
const loadRecommendations = async () => {
  try {
    const response = await getRecommendedItems(6); // 获取6个推荐商品
    recommendations.value = response.data || mockRecommendations;
  } catch (error) {
    console.error('Failed to load recommendations:', error);
    // 使用模拟数据
    recommendations.value = mockRecommendations;
  }
};

// 处理标签点击
const handleTabClick = () => {
  // 可以在这里添加标签切换时的逻辑
};

// 联系卖家
const contactSeller = () => {
  if (item.value.status === 'sold') {
    ElMessage.warning(t('item.detail.itemSold'));
    return;
  }
  contactDialogVisible.value = true;
};

// 发送消息
const sendMessage = () => {
  // 这里应该调用发送消息的API
  ElMessage.success(t('item.detail.messageSent'));
  contactDialogVisible.value = false;
  contactMessage.value = '';
};

// 切换收藏状态
const addToFavorite = async () => {
  try {
    if (isFavorite.value) {
      await unfavoriteItem(itemId.value);
      ElMessage.success(t('item.detail.unfavoriteSuccess'));
    } else {
      await favoriteItem(itemId.value);
      ElMessage.success(t('item.detail.favoriteSuccess'));
    }
    isFavorite.value = !isFavorite.value;
  } catch (error) {
    console.error('Failed to toggle favorite:', error);
    ElMessage.error(t('item.detail.operationFailed'));
  }
};

// 分享商品
const shareItem = () => {
  shareDialogVisible.value = true;
};

// 复制分享链接
const copyShareUrl = async () => {
  try {
    await navigator.clipboard.writeText(shareUrl.value);
    ElMessage.success(t('item.detail.linkCopied'));
  } catch (error) {
    console.error('Failed to copy share url:', error);
    ElMessage.error(t('item.detail.copyFailed'));
  }
};

// 查看卖家店铺
const viewSellerProfile = () => {
  // 这里应该跳转到卖家店铺页面
  ElMessage.info(t('item.detail.goToSellerShop'));
};

// 监听路由变化
watch(itemId, () => {
  loadItemDetail();
  loadRecommendations();
});

// 组件挂载时加载数据
onMounted(() => {
  loadItemDetail();
  loadRecommendations();
});

// 模拟数据
const mockItem = {
  id: '1',
  name: '全新未拆封MacBook Pro 2022',
  image: '/assets/images/macbook.jpg',
  price: 8999,
  originalPrice: 11999,
  discount: 7.5,
  description: '<p>全新未拆封MacBook Pro 2022款，14英寸，M2 Pro芯片，16GB内存，512GB固态硬盘。</p><p>机器是今年3月购买的，因个人原因闲置未使用，包装完好，配件齐全，有发票和保修凭证。</p><p>支持面交验货，非诚勿扰。</p>',
  category: 'digital',
  status: 'available',
  condition: '全新',
  location: '主校区教学楼A栋',
  tags: ['笔记本电脑', '苹果', '全新', 'MacBook Pro', 'M2'],
  views: 238,
  createdAt: Date.now() - 3600000,
  rating: 4.8,
  reviewCount: 25,
  specs: {
    '品牌': 'Apple',
    '型号': 'MacBook Pro 2022',
    '屏幕尺寸': '14英寸',
    '处理器': 'M2 Pro',
    '内存': '16GB',
    '存储': '512GB SSD',
    '显卡': 'M2 Pro 10核图形处理器',
    '电池循环': '0次'
  },
  shippingMethods: ['校园面交', '快递邮寄']
};

const mockItemImages = [
  '/assets/images/macbook2.jpg',
  '/assets/images/macbook3.jpg',
  '/assets/images/macbook4.jpg'
];

const mockSeller = {
  id: '101',
  name: '数码达人',
  avatar: '/assets/images/avatar1.jpg',
  activeItems: 12,
  ratingRate: 98,
  registeredAt: Date.now() - 365 * 24 * 60 * 60 * 1000,
  tags: ['诚信卖家', '快速回复', '优质服务'],
  phone: '138****6789',
  wechat: 'digital_daren',
  qq: '123456789',
  otherItems: [
    {
      id: '9',
      name: '无线耳机AirPods Pro',
      image: '/assets/images/airpods.jpg',
      price: 1200
    },
    {
      id: '10',
      name: '机械键盘青轴',
      image: '/assets/images/keyboard.jpg',
      price: 150
    },
    {
      id: '11',
      name: '电动车60V',
      image: '/assets/images/ebike.jpg',
      price: 1200
    },
    {
      id: '12',
      name: '羽毛球拍尤尼克斯',
      image: '/assets/images/badminton.jpg',
      price: 200
    }
  ]
};

const mockReviews = [
  {
    id: '1',
    userName: '小明',
    userAvatar: '/assets/images/avatar2.jpg',
    rating: 5,
    content: '商品非常好，全新未拆封，和描述的一样，卖家很热情，交易很愉快！',
    createdAt: Date.now() - 7200000,
    images: ['/assets/images/review1.jpg']
  },
  {
    id: '2',
    userName: '小红',
    userAvatar: '/assets/images/avatar3.jpg',
    rating: 4,
    content: '电脑很棒，就是包装有一点挤压，但不影响使用，总体很满意。',
    createdAt: Date.now() - 14400000,
    images: []
  },
  {
    id: '3',
    userName: '小刚',
    userAvatar: '/assets/images/avatar4.jpg',
    rating: 5,
    content: '价格比官网便宜了很多，机器是正品，有发票，推荐购买！',
    createdAt: Date.now() - 21600000,
    images: []
  }
];

const mockRecommendations = [
  {
    id: '2',
    name: '九成新iPad Pro 2021',
    image: '/assets/images/ipad.jpg',
    price: 4500
  },
  {
    id: '3',
    name: '大学英语四六级词汇书',
    image: '/assets/images/englishbook.jpg',
    price: 25
  },
  {
    id: '4',
    name: '考研数学复习全书',
    image: '/assets/images/mathbook.jpg',
    price: 35
  },
  {
    id: '5',
    name: '篮球Nike NBA官方用球',
    image: '/assets/images/basketball.jpg',
    price: 80
  },
  {
    id: '6',
    name: '吉他初学者套装',
    image: '/assets/images/guitar.jpg',
    price: 199
  },
  {
    id: '7',
    name: '专业绘图板Wacom',
    image: '/assets/images/tablet.jpg',
    price: 450
  }
];
</script>

<style lang="scss" scoped>
.item-detail-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.breadcrumb {
  margin-bottom: 20px;
}

.item-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}

/* 商品图片区域 */
.item-images {
  position: relative;
}

.main-image {
  position: relative;
  margin-bottom: 20px;
}

.main-image .image {
  width: 100%;
  height: 400px;
  object-fit: contain;
  cursor: pointer;
  transition: transform 0.3s;
}

.main-image .image:hover {
  transform: scale(1.02);
}

.discount-badge,
.sold-badge {
  position: absolute;
  top: 10px;
  padding: 5px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  color: white;
}

.discount-badge {
  left: 10px;
  background-color: #ff4d4f;
}

.sold-badge {
  right: 10px;
  background-color: #999;
}

.image-preview {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 10px 0;
}

.preview-item {
  flex: 0 0 80px;
  height: 80px;
  border: 2px solid transparent;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.preview-item:hover {
  border-color: #409eff;
  transform: scale(1.05);
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 商品基本信息 */
.item-basic-info {
  display: flex;
  flex-direction: column;
}

.item-name {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.4;
}

.item-rating {
  margin-bottom: 20px;
}

.review-count {
  margin-left: 10px;
  color: #999;
  font-size: 14px;
}

.item-price-section {
  margin-bottom: 25px;
}

.price-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.price-label {
  font-size: 16px;
  color: #666;
  margin-right: 10px;
}

.price {
  font-size: 28px;
  font-weight: bold;
  color: #ff4d4f;
}

.original-price {
  font-size: 16px;
  color: #999;
  text-decoration: line-through;
  margin-left: 15px;
}

.price-info {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #999;
}

.price-info i {
  margin-right: 5px;
}

.item-meta {
  margin-bottom: 30px;
}

.meta-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
  line-height: 1.6;
}

.meta-label {
  font-weight: 500;
  color: #666;
  width: 100px;
  flex-shrink: 0;
}

.meta-value {
  color: #333;
  flex: 1;
}

.status-available {
  color: #67c23a;
}

.status-sold {
  color: #999;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: auto;
}

.action-buttons .el-button {
  flex: 1;
}

/* 商品详细信息区域 */
.item-detail-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 30px;
  overflow: hidden;
}

.detail-tabs {
  border-bottom: 1px solid #e4e7ed;
}

.el-tabs {
  width: 100%;
}

.detail-content,
.reviews-content,
.seller-content {
  padding: 30px;
}

/* 商品详情内容 */
.detail-description h3,
.detail-specs h3,
.detail-shipping h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
}

.detail-description {
  margin-bottom: 30px;
}

.description-content {
  line-height: 1.8;
  color: #333;
  font-size: 16px;
}

.description-content p {
  margin-bottom: 15px;
}

.detail-specs {
  margin-bottom: 30px;
}

.specs-table {
  width: 100%;
  border-collapse: collapse;
}

.specs-table tr {
  border-bottom: 1px solid #e4e7ed;
}

.specs-table td {
  padding: 12px;
}

.spec-key {
  font-weight: 500;
  color: #666;
  width: 150px;
  background-color: #f5f7fa;
}

.spec-value {
  color: #333;
}

.shipping-methods {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.shipping-item {
  display: flex;
  align-items: center;
  color: #333;
  font-size: 16px;
}

.shipping-item i {
  color: #67c23a;
  margin-right: 8px;
  font-size: 18px;
}

/* 用户评价内容 */
.reviews-summary {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.rating-overview {
  display: flex;
  gap: 40px;
}

.overall-score {
  text-align: center;
}

.overall-score .score {
  display: block;
  font-size: 48px;
  font-weight: bold;
  color: #ff4d4f;
  margin-bottom: 10px;
}

.overall-score .score-label {
  font-size: 16px;
  color: #666;
}

.rating-details {
  flex: 1;
}

.rating-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.star-label {
  width: 50px;
  font-size: 14px;
  color: #666;
}

.rating-item .el-progress {
  flex: 1;
  margin: 0 15px;
}

.count {
  font-size: 14px;
  color: #999;
  width: 40px;
  text-align: right;
}

.reviews-list {
  margin-top: 30px;
}

.review-item {
  padding: 20px 0;
  border-bottom: 1px solid #e4e7ed;
}

.review-item:last-child {
  border-bottom: none;
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 15px;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-right: 15px;
}

.review-time {
  font-size: 12px;
  color: #999;
  margin-left: 15px;
}

.review-content {
  font-size: 16px;
  color: #333;
  line-height: 1.6;
  margin-bottom: 15px;
}

.review-images {
  display: flex;
  gap: 10px;
}

.review-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.3s;
}

.review-image:hover {
  transform: scale(1.05);
}

.no-reviews {
  text-align: center;
  padding: 40px 0;
}

/* 卖家信息内容 */
.seller-info {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 30px;
}

.seller-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}

.seller-details {
  flex: 1;
}

.seller-name {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.seller-stats {
  display: flex;
  gap: 30px;
  margin-bottom: 15px;
}

.stat-item {
  font-size: 14px;
  color: #666;
}

.stat-item i {
  color: #409eff;
  margin-right: 5px;
}

.seller-tags {
  display: flex;
  gap: 8px;
}

.seller-actions {
  display: flex;
  gap: 10px;
}

.seller-other-items h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
}

.other-items-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.other-item {
  text-decoration: none;
  color: #333;
  transition: all 0.3s;
}

.other-item:hover {
  transform: translateY(-5px);
}

.other-item-image {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 10px;
}

.other-item-name {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.other-item-price {
  font-size: 16px;
  font-weight: bold;
  color: #ff4d4f;
}

.no-other-items {
  text-align: center;
  padding: 40px 0;
}

/* 推荐商品区域 */
.recommendations-section {
  margin-bottom: 30px;
}

.recommendations-section h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
}

.recommendations-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.recommendation-item {
  text-decoration: none;
  color: #333;
  transition: all 0.3s;
}

.recommendation-item:hover {
  transform: translateY(-5px);
}

.rec-image {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 10px;
}

.rec-name {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rec-price {
  font-size: 16px;
  font-weight: bold;
  color: #ff4d4f;
}

/* 弹窗样式 */
.contact-form {
  max-height: 400px;
  overflow-y: auto;
}

.seller-contact-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.seller-contact-info p {
  margin-bottom: 10px;
  font-size: 14px;
}

.seller-contact-info p:last-child {
  margin-bottom: 0;
}

.share-content {
  text-align: center;
}

.share-link {
  margin-bottom: 20px;
}

.share-link .el-input {
  margin-bottom: 15px;
}

.qrcode-image {
  margin: 0 auto;
  width: 150px;
  height: 150px;
  background-color: white;
  border: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.qrcode-placeholder {
  font-size: 16px;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .item-detail-container {
    max-width: 100%;
    padding: 15px;
  }
}

@media (max-width: 768px) {
  .item-card {
    grid-template-columns: 1fr;
    padding: 20px;
  }
  
  .main-image .image {
    height: 300px;
  }
  
  .item-name {
    font-size: 20px;
  }
  
  .price {
    font-size: 24px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .detail-content,
  .reviews-content,
  .seller-content {
    padding: 20px;
  }
  
  .rating-overview {
    flex-direction: column;
    gap: 20px;
  }
  
  .seller-info {
    flex-direction: column;
    text-align: center;
  }
  
  .seller-avatar {
    margin-right: 0;
    margin-bottom: 15px;
  }
  
  .seller-stats {
    justify-content: center;
  }
  
  .seller-tags {
    justify-content: center;
  }
  
  .seller-actions {
    margin-top: 15px;
  }
  
  .other-items-list,
  .recommendations-list {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .item-detail-container {
    padding: 10px;
  }
  
  .item-card {
    padding: 15px;
  }
  
  .main-image .image {
    height: 200px;
  }
  
  .item-name {
    font-size: 18px;
  }
  
  .price {
    font-size: 20px;
  }
  
  .detail-content,
  .reviews-content,
  .seller-content {
    padding: 15px;
  }
  
  .spec-key {
    width: 100px;
    font-size: 14px;
  }
  
  .spec-value {
    font-size: 14px;
  }
  
  .other-items-list,
  .recommendations-list {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
  }
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.item-card,
.item-detail-section,
.recommendations-section {
  animation: fadeInUp 0.5s ease-out;
}
</style>