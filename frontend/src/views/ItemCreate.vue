<template>
  <div class="item-create-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>{{ isRentPage ? $t('item.create.publishRent') : $t('item.create.publishItem') }}</h1>
      <p>{{ isRentPage ? $t('item.create.publishRentSubtitle') : $t('item.create.publishItemSubtitle') }}</p>
    </div>

    <!-- 发布表单 -->
    <div class="form-container">
      <el-form ref="itemFormRef" :model="itemForm" :rules="itemRules" label-width="120px">
        <!-- 商品信息 -->
        <el-form-item :label="$t('item.create.itemName')" prop="name">
          <el-input v-model="itemForm.name" :placeholder="$t('item.create.itemNamePlaceholder')" maxlength="50" show-word-limit />
        </el-form-item>

        <el-form-item :label="$t('item.create.itemCategory')" prop="category">
          <el-select v-model="itemForm.category" :placeholder="$t('item.create.selectCategory')">
            <el-option :label="$t('item.categories.digital')" value="digital"></el-option>
            <el-option :label="$t('item.categories.textbook')" value="textbook"></el-option>
            <el-option :label="$t('item.categories.home')" value="home"></el-option>
            <el-option :label="$t('item.categories.sports')" value="sports"></el-option>
            <el-option :label="$t('item.categories.clothing')" value="clothing"></el-option>
            <el-option :label="$t('item.categories.others')" value="others"></el-option>
          </el-select>
        </el-form-item>

        <!-- 交易类型 -->
        <el-form-item :label="$t('item.create.tradeType')" prop="transaction_type">
          <el-radio-group v-model="itemForm.transaction_type">
            <el-radio-button label="出售">{{ $t('item.transactionType.sale') }}</el-radio-button>
            <el-radio-button label="出租">{{ $t('item.transactionType.rent') }}</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <!-- 价格信息 - 出售 -->
        <div v-if="itemForm.transaction_type === 'sale'">
          <el-form-item :label="$t('item.create.sellPrice')" prop="price">
            <el-input-number v-model="itemForm.price" :min="0" :precision="2" :placeholder="$t('item.create.enterSellPrice')" />
          </el-form-item>

          <el-form-item :label="$t('item.originalPrice')" prop="originalPrice">
            <el-input-number v-model="itemForm.originalPrice" :min="0" :precision="2" :placeholder="$t('item.create.originalPriceOptional')" />
          </el-form-item>
        </div>

        <!-- 价格信息 - 出租 -->
        <div v-if="itemForm.transaction_type === 'rent'">
          <el-form-item :label="$t('item.create.dailyRent')" prop="rental_price_day">
            <el-input-number v-model="itemForm.rental_price_day" :min="0" :precision="2" :placeholder="$t('item.create.enterDailyRent')" />
          </el-form-item>

          <el-form-item :label="$t('item.create.weeklyRent')" prop="rental_price_week">
            <el-input-number v-model="itemForm.rental_price_week" :min="0" :precision="2" :placeholder="$t('item.create.enterWeeklyRent')" />
          </el-form-item>

          <el-form-item :label="$t('item.create.monthlyRent')" prop="rental_price_month">
            <el-input-number v-model="itemForm.rental_price_month" :min="0" :precision="2" :placeholder="$t('item.create.enterMonthlyRent')" />
          </el-form-item>

          <el-form-item :label="$t('item.create.depositLabel')" prop="deposit">
            <el-input-number v-model="itemForm.deposit" :min="0" :precision="2" :placeholder="$t('item.create.enterDeposit')" />
          </el-form-item>

          <el-form-item :label="$t('item.create.maxRentDays')" prop="max_rental_days">
            <el-input-number v-model="itemForm.max_rental_days" :min="1" :placeholder="$t('item.create.enterMaxRentDays')" />
          </el-form-item>
        </div>

        <!-- 商品状态 -->
        <el-form-item :label="$t('item.create.conditionLabel')" prop="condition">
          <el-radio-group v-model="itemForm.condition">
            <el-radio-button label="全新">{{ $t('item.create.conditionNew') }}</el-radio-button>
            <el-radio-button label="九成新">{{ $t('item.create.condition90') }}</el-radio-button>
            <el-radio-button label="八成新">{{ $t('item.create.condition80') }}</el-radio-button>
            <el-radio-button label="七成新">{{ $t('item.create.condition70') }}</el-radio-button>
            <el-radio-button label="六成新及以下">{{ $t('item.create.condition60') }}</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <!-- 商品图片 -->
        <el-form-item :label="$t('item.create.itemImages')" prop="images">
          <el-upload
            v-model:file-list="fileList"
            class="upload-demo"
            action=""
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleRemove"
            list-type="picture-card"
            :limit="8"
            :on-exceed="handleExceed"
          >
            <el-icon><Plus /></el-icon>
            <template #file="{ file }">
              <div>
                <img :src="file.url || file.thumbUrl" alt="" />
                <div class="el-upload__actions">
                  <el-icon class="el-upload__preview-cover--edit" @click.stop="handlePictureCardPreview(file)">
                    <Eye />
                  </el-icon>
                  <el-icon class="el-upload__preview-cover--remove" @click.stop="handleRemove(file)">
                    <Delete />
                  </el-icon>
                </div>
              </div>
            </template>
          </el-upload>
          <el-dialog v-model="dialogVisible" :title="$t('item.create.preview')" width="800px">
            <img w-full :src="dialogImageUrl" alt="" />
          </el-dialog>
          <div class="upload-tip">{{ $t('item.create.imageTip') }}</div>
        </el-form-item>

        <!-- 商品描述 -->
        <el-form-item :label="$t('item.create.itemDescLabel')" prop="description">
          <el-input
            v-model="itemForm.description"
            type="textarea"
            :rows="8"
            :placeholder="$t('item.create.itemDescPlaceholder')"
            maxlength="2000"
            show-word-limit
          />
          <div class="description-tip">{{ $t('item.create.descTip') }}</div>
        </el-form-item>

        <!-- 交易信息 -->
        <el-form-item :label="$t('item.create.tradeLocation')" prop="location">
          <el-input v-model="itemForm.location" :placeholder="$t('item.create.tradeLocationPlaceholder')" maxlength="100" show-word-limit />
        </el-form-item>

        <el-form-item :label="$t('item.create.tradeMethods')" prop="shippingMethods">
          <el-checkbox-group v-model="itemForm.shippingMethods">
            <el-checkbox label="校园面交" name="shipping">{{ $t('item.create.faceToFace') }}</el-checkbox>
            <el-checkbox label="快递邮寄" name="shipping">{{ $t('item.create.express') }}</el-checkbox>
            <el-checkbox label="其他方式" name="shipping">{{ $t('item.create.otherMethod') }}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <!-- 商品标签 -->
        <el-form-item :label="$t('item.create.itemTags')">
          <el-input
            v-model="tagInput"
            :placeholder="$t('item.create.tagPlaceholder')"
            @keyup.enter="addTag"
            style="width: 300px; margin-right: 10px;"
          />
          <el-tag
            v-for="tag in itemForm.tags"
            :key="tag"
            closable
            :disable-transitions="false"
            @close="removeTag(tag)"
          >
            {{ tag }}
          </el-tag>
          <div class="tag-tip">{{ $t('item.create.tagTip') }}</div>
        </el-form-item>

        <!-- 商品规格（动态添加） -->
        <el-form-item :label="$t('item.create.itemSpecs')">
          <div v-for="(spec, index) in itemForm.specs" :key="index" class="spec-item">
            <el-input
              v-model="spec.key"
              :placeholder="$t('item.create.specName')"
              style="width: 150px; margin-right: 10px;"
              @input="validateSpecs"
            />
            <span>:</span>
            <el-input
              v-model="spec.value"
              :placeholder="$t('item.create.specValue')"
              style="width: 200px; margin-left: 10px;"
              @input="validateSpecs"
            />
            <el-button
              type="danger"
              icon="el-icon-delete"
              circle
              @click="removeSpec(index)"
              style="margin-left: 10px;"
            />
          </div>
          <el-button
            type="primary"
            icon="el-icon-plus"
            @click="addSpec"
            :disabled="itemForm.specs.length >= 10"
            style="margin-top: 10px;"
          >
            {{ $t('item.create.addSpec') }}
          </el-button>
          <div class="spec-tip">{{ $t('item.create.specTip') }}</div>
        </el-form-item>

        <!-- 提交按钮 -->
        <el-form-item>
          <div class="form-actions">
            <el-button @click="resetForm">{{ $t('item.create.reset') }}</el-button>
            <el-button type="primary" @click="submitForm">{{ $t('item.create.publish') }}</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>

    <!-- 发布成功提示 -->
    <el-dialog v-model="successDialogVisible" :title="$t('item.create.publishSuccess')" width="400px" :show-close="false">
      <div class="success-content">
        <div class="success-icon">
          <i class="el-icon-success"></i>
        </div>
        <p class="success-text">{{ $t('item.create.congratsPublish') }}</p>
        <p class="success-hint">{{ $t('item.create.reviewHint') }}</p>
      </div>
      <template #footer>
        <div class="dialog-actions">
          <el-button @click="viewItem">{{ $t('item.create.viewItem') }}</el-button>
          <el-button type="primary" @click="publishAnother">{{ $t('item.create.publishAnother') }}</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { createItem, itemAPI } from '@/api/item';
import { Plus, Delete } from '@element-plus/icons-vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// 路由
const router = useRouter();
const route = useRoute();

// 表单引用
const itemFormRef = ref<any>();

// 文件上传相关
const fileList = ref<Array<any>>([]);
const dialogVisible = ref(false);
const dialogImageUrl = ref('');
const uploadedFiles = ref<File[]>([]);
// 判断是否是租赁页面
const isRentPage = computed(() => route.name === 'RentCreate');

// 表单数据
const itemForm = reactive({
  name: '',
  category: '',
  price: 0,
  originalPrice: 0,
  // 租赁相关字段
  transaction_type: isRentPage.value ? 'rent' : 'sale',
  rental_price_day: 0,
  rental_price_week: 0,
  rental_price_month: 0,
  deposit: 0,
  max_rental_days: 30,
  condition: '九成新',
  description: '',
  location: '',
  shippingMethods: [] as string[],
  tags: [] as string[],
  specs: [] as Array<{ key: string; value: string }>,
  images: [] as string[]
});

// 标签输入
const tagInput = ref('');

// 成功弹窗
const successDialogVisible = ref(false);
const createdItemId = ref('');

// 表单验证规则
const itemRules = computed(() => ({
  name: [
    { required: true, message: t('item.create.validation.nameRequired'), trigger: 'blur' },
    { min: 2, max: 50, message: t('item.create.validation.nameLength'), trigger: 'blur' }
  ],
  category: [
    { required: true, message: t('item.create.validation.categoryRequired'), trigger: 'change' }
  ],
  transaction_type: [
    { required: true, message: t('item.create.validation.tradeTypeRequired'), trigger: 'change' }
  ],
  price: [
    { required: (() => itemForm.transaction_type === 'sale'), message: t('item.create.validation.priceRequired'), trigger: 'blur' },
    { type: 'number', min: 0.01, message: t('item.create.validation.pricePositive'), trigger: 'blur' }
  ],
  // 租赁相关验证
  rental_price_day: [
    { required: (() => itemForm.transaction_type === 'rent'), message: t('item.create.validation.dailyRentRequired'), trigger: 'blur' },
    { type: 'number', min: 0.01, message: t('item.create.validation.dailyRentPositive'), trigger: 'blur' }
  ],
  rental_price_week: [
    { type: 'number', min: 0, message: t('item.create.validation.weeklyRentPositive'), trigger: 'blur' }
  ],
  rental_price_month: [
    { type: 'number', min: 0, message: t('item.create.validation.monthlyRentPositive'), trigger: 'blur' }
  ],
  deposit: [
    { type: 'number', min: 0, message: t('item.create.validation.depositPositive'), trigger: 'blur' }
  ],
  max_rental_days: [
    { required: (() => itemForm.transaction_type === 'rent'), message: t('item.create.validation.maxRentDaysRequired'), trigger: 'blur' },
    { type: 'number', min: 1, message: t('item.create.validation.maxRentDaysPositive'), trigger: 'blur' }
  ],
  condition: [
    { required: true, message: t('item.create.validation.conditionRequired'), trigger: 'change' }
  ],
  description: [
    { required: true, message: t('item.create.validation.descRequired'), trigger: 'blur' },
    { min: 10, max: 2000, message: t('item.create.validation.descLength'), trigger: 'blur' }
  ],
  location: [
    { required: true, message: t('item.create.validation.locationRequired'), trigger: 'blur' },
    { min: 2, max: 100, message: t('item.create.validation.locationLength'), trigger: 'blur' }
  ],
  shippingMethods: [
    { required: true, message: t('item.create.validation.shippingRequired'), trigger: 'change' }
  ],
  images: [
    { required: true, message: t('item.create.validation.imagesRequired'), trigger: 'change' }
  ]
}));

// 处理文件变化
const handleFileChange = (uploadFile: any, _uploadFiles: any[]) => {
  // 检查文件类型
  const isJPG = uploadFile.raw.type === 'image/jpeg';
  const isPNG = uploadFile.raw.type === 'image/png';
  const isJPEG = uploadFile.raw.type === 'image/jpeg';
  const isLt5M = uploadFile.raw.size / 1024 / 1024 < 5;

  if (!isJPG && !isPNG && !isJPEG) {
    ElMessage.error(t('item.create.imageFormatError'));
    return false;
  }
  if (!isLt5M) {
    ElMessage.error(t('item.create.imageSizeError'));
    return false;
  }

  // 将文件添加到上传列表
  uploadedFiles.value.push(uploadFile.raw);
  return true;
};

// 处理文件删除
const handleRemove = (file: any) => {
  const index = fileList.value.indexOf(file);
  if (index > -1) {
    fileList.value.splice(index, 1);
    // 从上传列表中移除
    const uploadedIndex = uploadedFiles.value.findIndex(f => f.name === file.name);
    if (uploadedIndex > -1) {
      uploadedFiles.value.splice(uploadedIndex, 1);
    }
  }
};

// 处理文件超出数量限制
const handleExceed = (_files: any, fileList: any) => {
  ElMessage.error(t('item.create.maxImages'));
};

// 预览图片
const handlePictureCardPreview = (file: any) => {
  dialogImageUrl.value = file.url || file.thumbUrl;
  dialogVisible.value = true;
};

// 添加标签
const addTag = () => {
  if (tagInput.value.trim() && itemForm.tags.length < 5) {
    if (itemForm.tags.includes(tagInput.value.trim())) {
      ElMessage.warning(t('item.create.tagExists'));
    } else {
      itemForm.tags.push(tagInput.value.trim());
      tagInput.value = '';
    }
  } else if (itemForm.tags.length >= 5) {
    ElMessage.warning(t('item.create.maxTags'));
  }
};

// 移除标签
const removeTag = (tag: string) => {
  const index = itemForm.tags.indexOf(tag);
  if (index > -1) {
    itemForm.tags.splice(index, 1);
  }
};

// 添加规格
const addSpec = () => {
  if (itemForm.specs.length < 10) {
    itemForm.specs.push({ key: '', value: '' });
  } else {
    ElMessage.warning(t('item.create.maxSpecs'));
  }
};

// 移除规格
const removeSpec = (index: number) => {
  itemForm.specs.splice(index, 1);
};

// 验证规格
const validateSpecs = () => {
  // 这里可以添加规格验证逻辑
};

// 重置表单
const resetForm = () => {
  itemFormRef.value?.resetFields();
  itemForm.tags = [];
  itemForm.specs = [];
  fileList.value = [];
  uploadedFiles.value = [];
  tagInput.value = '';
};

// 提交表单
const submitForm = async () => {
  if (!itemFormRef.value) return;
  
  const loading = ref(false);
  loading.value = true;
  try {
    // 表单验证
    await itemFormRef.value.validate();
    
    // 检查是否有图片
    if (uploadedFiles.value.length === 0) {
      ElMessage.error(t('item.create.uploadAtLeastOne'));
      return;
    }
    
    let imageUrls: string[] = [];
    
    // 上传图片
    if (uploadedFiles.value.length > 0) {
      const imageFormData = new FormData();
      uploadedFiles.value.forEach(file => {
        imageFormData.append('images', file);
      });
      
      const uploadResponse = await itemAPI.uploadItemImages(imageFormData);
      imageUrls = uploadResponse.data?.images || [];
    }
    
    // 创建商品数据
    const itemData: any = {
      title: itemForm.name,
      description: itemForm.description,
      categoryId: itemForm.category,
      tags: itemForm.tags.length > 0 ? itemForm.tags : undefined,
      images: imageUrls,
      location: itemForm.location || undefined,
      status: 'available',
      transaction_type: itemForm.transaction_type
    };
    
    // 出售商品参数
    if (itemForm.transaction_type === 'sale') {
      itemData.price = Number(itemForm.price);
      if (itemForm.originalPrice) {
        itemData.originalPrice = Number(itemForm.originalPrice);
      }
    }
    
    // 租赁商品参数
    if (itemForm.transaction_type === 'rent') {
      itemData.rental_price_day = Number(itemForm.rental_price_day);
      if (itemForm.rental_price_week) {
        itemData.rental_price_week = Number(itemForm.rental_price_week);
      }
      if (itemForm.rental_price_month) {
        itemData.rental_price_month = Number(itemForm.rental_price_month);
      }
      if (itemForm.deposit) {
        itemData.deposit = Number(itemForm.deposit);
      }
      itemData.max_rental_days = Number(itemForm.max_rental_days);
    }
    
    // 提交数据
    const response = await createItem(itemData);
    createdItemId.value = response.data?.id || '';
    successDialogVisible.value = true;
  } catch (error: any) {
    console.error('Failed to create item:', error);
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message);
    } else {
      ElMessage.error(isRentPage.value ? t('item.create.publishRentFailed') : t('item.create.publishFailed'));
    }
  } finally {
    loading.value = false;
  }
};

// 查看已发布商品
const viewItem = () => {
  successDialogVisible.value = false;
  router.push(`/items/${createdItemId.value}`);
};

// 发布另一个商品
const publishAnother = () => {
  successDialogVisible.value = false;
  resetForm();
};

// 组件挂载时
onMounted(() => {
  // 设置默认交易地点（可以从用户信息中获取）
  const defaultLocation = localStorage.getItem('defaultLocation');
  if (defaultLocation) {
    itemForm.location = defaultLocation;
  }
});
</script>

<style lang="scss" scoped>
.item-create-container {
  width: 100%;
  max-width: 1000px;
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

.form-container {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.el-form-item {
  margin-bottom: 25px;
}

.el-form-item__label {
  font-weight: 500;
}

/* 文件上传样式 */
.upload-demo {
  margin-bottom: 10px;
}

.upload-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

/* 描述提示 */
.description-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

/* 标签样式 */
.tag-tip {
  font-size: 12px;
  color: #999;
  margin-top: 10px;
}

/* 规格样式 */
.spec-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.spec-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

/* 表单操作按钮 */
.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

.form-actions .el-button {
  width: 120px;
  height: 40px;
  font-size: 16px;
}

/* 成功弹窗样式 */
.success-content {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  font-size: 60px;
  color: #67c23a;
  margin-bottom: 20px;
}

.success-text {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.success-hint {
  font-size: 14px;
  color: #999;
}

.dialog-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

/* 响应式设计 */
@media (max-width: 1000px) {
  .item-create-container {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 24px;
  }
  
  .form-container {
    padding: 20px;
  }
  
  .el-form-item {
    margin-bottom: 20px;
  }
  
  .el-form-item__label {
    width: 100px;
    font-size: 14px;
  }
  
  .el-upload {
    width: 100%;
  }
  
  .spec-item {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .spec-item .el-input {
    width: calc(50% - 30px) !important;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .form-actions .el-button {
    width: 100%;
    max-width: 200px;
  }
}

@media (max-width: 480px) {
  .item-create-container {
    padding: 10px;
  }
  
  .page-header {
    padding: 15px 0;
  }
  
  .page-header h1 {
    font-size: 20px;
  }
  
  .form-container {
    padding: 15px;
  }
  
  .el-form-item__label {
    width: 80px;
    font-size: 12px;
  }
  
  .spec-item .el-input {
    width: 100% !important;
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

.page-header,
.form-container {
  animation: fadeInUp 0.5s ease-out;
}
</style>