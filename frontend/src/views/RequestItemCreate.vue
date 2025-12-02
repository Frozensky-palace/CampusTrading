<template>
  <div class="request-item-create-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>{{ $t('request.create.title') }}</h1>
      <p>{{ $t('request.create.subtitle') }}</p>
    </div>

    <!-- 发布表单 -->
    <div class="form-container">
      <el-form ref="requestFormRef" :model="requestForm" :rules="requestRules" label-width="120px">
        <!-- 求购信息 -->
        <el-form-item :label="$t('request.create.requestTitle')" prop="title">
          <el-input v-model="requestForm.title" :placeholder="$t('request.create.titlePlaceholder')" maxlength="50" show-word-limit />
        </el-form-item>

        <el-form-item :label="$t('request.create.category')" prop="category">
          <el-select v-model="requestForm.category" :placeholder="$t('request.create.categoryPlaceholder')">
            <el-option :label="$t('item.categories.digital')" value="digital"></el-option>
            <el-option :label="$t('item.categories.textbook')" value="textbook"></el-option>
            <el-option :label="$t('item.categories.home')" value="home"></el-option>
            <el-option :label="$t('item.categories.sports')" value="sports"></el-option>
            <el-option :label="$t('item.categories.clothing')" value="clothing"></el-option>
            <el-option :label="$t('item.categories.others')" value="others"></el-option>
          </el-select>
        </el-form-item>

        <!-- 价格信息 -->
        <el-form-item :label="$t('request.create.maxPrice')" prop="maxPrice">
          <el-input-number v-model="requestForm.maxPrice" :min="0" :precision="2" :placeholder="$t('request.create.maxPricePlaceholder')" />
        </el-form-item>

        <!-- 期望新旧程度 -->
        <el-form-item :label="$t('request.create.expectedCondition')" prop="expectedCondition">
          <el-radio-group v-model="requestForm.expectedCondition">
            <el-radio-button :label="$t('request.create.conditionNew')">{{ $t('request.create.conditionNew') }}</el-radio-button>
            <el-radio-button :label="$t('request.create.condition90')">{{ $t('request.create.condition90') }}</el-radio-button>
            <el-radio-button :label="$t('request.create.condition80')">{{ $t('request.create.condition80') }}</el-radio-button>
            <el-radio-button :label="$t('request.create.condition70')">{{ $t('request.create.condition70') }}</el-radio-button>
            <el-radio-button :label="$t('request.create.condition60')">{{ $t('request.create.condition60') }}</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <!-- 求购描述 -->
        <el-form-item :label="$t('request.create.description')" prop="description">
          <el-input
            v-model="requestForm.description"
            type="textarea"
            :rows="8"
            :placeholder="$t('request.create.descriptionPlaceholder')"
            maxlength="2000"
            show-word-limit
          />
          <div class="description-tip">{{ $t('request.create.descriptionTip') }}</div>
        </el-form-item>

        <!-- 交易信息 -->
        <el-form-item :label="$t('request.create.location')" prop="location">
          <el-input v-model="requestForm.location" :placeholder="$t('request.create.locationPlaceholder')" maxlength="100" show-word-limit />
        </el-form-item>

        <el-form-item :label="$t('request.create.shippingMethod')" prop="shippingMethods">
          <el-checkbox-group v-model="requestForm.shippingMethods">
            <el-checkbox :label="$t('request.create.faceToFace')" name="shipping" />
            <el-checkbox :label="$t('request.create.express')" name="shipping" />
            <el-checkbox :label="$t('request.create.otherMethod')" name="shipping" />
          </el-checkbox-group>
        </el-form-item>

        <!-- 求购标签 -->
        <el-form-item :label="$t('request.create.tags')">
          <el-input
            v-model="tagInput"
            :placeholder="$t('request.create.tagsPlaceholder')"
            @keyup.enter="addTag"
            style="width: 300px; margin-right: 10px;"
          />
          <el-tag
            v-for="tag in requestForm.tags"
            :key="tag"
            closable
            :disable-transitions="false"
            @close="removeTag(tag)"
          >
            {{ tag }}
          </el-tag>
          <div class="tag-tip">{{ $t('request.create.tagsTip') }}</div>
        </el-form-item>

        <!-- 特殊要求（动态添加） -->
        <el-form-item :label="$t('request.create.specialRequirements')">
          <div v-for="(requirement, index) in requestForm.requirements" :key="index" class="requirement-item">
            <el-input
              v-model="requirement.name"
              :placeholder="$t('request.create.requirementName')"
              style="width: 150px; margin-right: 10px;"
            />
            <span>:</span>
            <el-input
              v-model="requirement.value"
              :placeholder="$t('request.create.requirementValue')"
              style="width: 200px; margin-left: 10px;"
            />
            <el-button
              type="danger"
              icon="el-icon-delete"
              circle
              @click="removeRequirement(index)"
              style="margin-left: 10px;"
            />
          </div>
          <el-button
            type="primary"
            icon="el-icon-plus"
            @click="addRequirement"
            :disabled="requestForm.requirements.length >= 10"
            style="margin-top: 10px;"
          >
            {{ $t('request.create.addRequirement') }}
          </el-button>
          <div class="requirement-tip">{{ $t('request.create.requirementsTip') }}</div>
        </el-form-item>

        <!-- 期望完成时间 -->
        <el-form-item :label="$t('request.create.expectedDate')" prop="expectedCompletionDate">
          <el-date-picker
            v-model="requestForm.expectedCompletionDate"
            type="date"
            :placeholder="$t('request.create.expectedDatePlaceholder')"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <!-- 联系方式设置 -->
        <el-form-item :label="$t('request.create.contactSettings')">
          <div class="contact-settings">
            <el-checkbox-group v-model="contactOptions">
              <el-checkbox label="phone" name="contact">{{ $t('request.create.showPhone') }}</el-checkbox>
              <el-checkbox label="wechat" name="contact">{{ $t('request.create.showWechat') }}</el-checkbox>
              <el-checkbox label="qq" name="contact">{{ $t('request.create.showQQ') }}</el-checkbox>
            </el-checkbox-group>
            <div class="contact-hint">{{ $t('request.create.contactHint') }}</div>
          </div>
        </el-form-item>

        <!-- 提交按钮 -->
        <el-form-item>
          <div class="form-actions">
            <el-button @click="resetForm">{{ $t('common.reset') }}</el-button>
            <el-button type="primary" @click="submitForm">{{ $t('request.create.submit') }}</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>

    <!-- 发布成功提示 -->
    <el-dialog v-model="successDialogVisible" :title="$t('request.create.successTitle')" width="400px" :show-close="false">
      <div class="success-content">
        <div class="success-icon">
          <i class="el-icon-success"></i>
        </div>
        <p class="success-text">{{ $t('request.create.successText') }}</p>
        <p class="success-hint">{{ $t('request.create.successHint') }}</p>
      </div>
      <template #footer>
        <div class="dialog-actions">
          <el-button @click="viewRequestItem">{{ $t('request.create.viewRequest') }}</el-button>
          <el-button type="primary" @click="publishAnother">{{ $t('request.create.publishAnother') }}</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useI18n } from 'vue-i18n';
import { createRequestItem } from '@/api/requestItem';
import { useUserStore } from '@/store/user';

const { t } = useI18n();

// 路由和状态管理
const router = useRouter();
const userStore = useUserStore();

// 表单引用
const requestFormRef = ref<any>();

// 表单数据
const requestForm = reactive({
  title: '',
  category: '',
  maxPrice: 0,
  expectedCondition: '八成新',
  description: '',
  location: '',
  shippingMethods: [] as string[],
  tags: [] as string[],
  requirements: [] as Array<{ name: string; value: string }>,
  expectedCompletionDate: ''
});

// 标签输入
const tagInput = ref('');

// 联系方式选项
const contactOptions = ref<string[]>(['phone']);

// 成功弹窗
const successDialogVisible = ref(false);
const createdRequestItemId = ref('');

// 表单验证规则
const requestRules = computed(() => ({
  title: [
    { required: true, message: t('request.create.validation.titleRequired'), trigger: 'blur' },
    { min: 2, max: 50, message: t('request.create.validation.titleLength'), trigger: 'blur' }
  ],
  category: [
    { required: true, message: t('request.create.validation.categoryRequired'), trigger: 'change' }
  ],
  maxPrice: [
    { required: true, message: t('request.create.validation.priceRequired'), trigger: 'blur' },
    { type: 'number', min: 0.01, message: t('request.create.validation.priceMin'), trigger: 'blur' }
  ],
  expectedCondition: [
    { required: true, message: t('request.create.validation.conditionRequired'), trigger: 'change' }
  ],
  description: [
    { required: true, message: t('request.create.validation.descriptionRequired'), trigger: 'blur' },
    { min: 10, max: 2000, message: t('request.create.validation.descriptionLength'), trigger: 'blur' }
  ],
  location: [
    { required: true, message: t('request.create.validation.locationRequired'), trigger: 'blur' },
    { min: 2, max: 100, message: t('request.create.validation.locationLength'), trigger: 'blur' }
  ],
  shippingMethods: [
    { required: true, message: t('request.create.validation.shippingRequired'), trigger: 'change' }
  ],
  expectedCompletionDate: [
    { required: true, message: t('request.create.validation.dateRequired'), trigger: 'change' }
  ]
}));

// 添加标签
const addTag = () => {
  if (tagInput.value.trim() && requestForm.tags.length < 5) {
    if (requestForm.tags.includes(tagInput.value.trim())) {
      ElMessage.warning(t('request.create.tagExists'));
    } else {
      requestForm.tags.push(tagInput.value.trim());
      tagInput.value = '';
    }
  } else if (requestForm.tags.length >= 5) {
    ElMessage.warning(t('request.create.maxTags'));
  }
};

// 移除标签
const removeTag = (tag: string) => {
  const index = requestForm.tags.indexOf(tag);
  if (index > -1) {
    requestForm.tags.splice(index, 1);
  }
};

// 添加要求
const addRequirement = () => {
  if (requestForm.requirements.length < 10) {
    requestForm.requirements.push({ name: '', value: '' });
  } else {
    ElMessage.warning(t('request.create.maxRequirements'));
  }
};

// 移除要求
const removeRequirement = (index: number) => {
  requestForm.requirements.splice(index, 1);
};

// 重置表单
const resetForm = () => {
  requestFormRef.value?.resetFields();
  requestForm.tags = [];
  requestForm.requirements = [];
  tagInput.value = '';
  contactOptions.value = ['phone'];
};

// 提交表单
const submitForm = async () => {
  if (!requestFormRef.value) return;
  
  // 检查联系方式
  if (contactOptions.value.length === 0) {
    ElMessage.error(t('request.create.contactRequired'));
    return;
  }
  
  try {
    // 表单验证
    await requestFormRef.value.validate();
    
    // 构建请求数据，调整格式以匹配API要求
      const requestData = {
        title: requestForm.title,
        description: requestForm.description,
        priceRange: {
          min: 0,
          max: requestForm.maxPrice
        },
        categoryId: requestForm.category,
        tags: requestForm.tags,
        location: requestForm.location,
        status: 'active',
        contactOptions: contactOptions.value
      };
    
    // 提交数据
    const response = await createRequestItem(requestData);
    createdRequestItemId.value = response.data?.id || '';
    successDialogVisible.value = true;
  } catch (error: any) {
    console.error('Failed to create request item:', error);
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message);
    } else {
      ElMessage.error(t('request.create.submitFailed'));
    }
  }
};

// 查看已发布求购
const viewRequestItem = () => {
  successDialogVisible.value = false;
  router.push(`/request-items/${createdRequestItemId.value}`);
};

// 发布另一个求购
const publishAnother = () => {
  successDialogVisible.value = false;
  resetForm();
};

// 组件挂载时
onMounted(() => {
  // 检查用户是否登录
  if (!userStore.isLoggedIn) {
    ElMessage.warning(t('request.create.loginRequired'));
    router.push('/login');
    return;
  }
  
  // 设置默认交易地点（可以从用户信息中获取）
  const defaultLocation = localStorage.getItem('defaultLocation');
  if (defaultLocation) {
    requestForm.location = defaultLocation;
  }
  
  // 设置默认期望完成时间（当前时间+7天）
  const today = new Date();
  const nextWeek = new Date(today);
  nextWeek.setDate(today.getDate() + 7);
  const formattedDate = nextWeek.toISOString().split('T')[0];
  requestForm.expectedCompletionDate = formattedDate;
});
</script>

<style lang="scss" scoped>
.request-item-create-container {
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

/* 要求样式 */
.requirement-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.requirement-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

/* 联系方式设置 */
.contact-settings {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.contact-hint {
  font-size: 12px;
  color: #999;
  margin-top: 10px;
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
  .request-item-create-container {
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
  
  .requirement-item {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .requirement-item .el-input {
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
  .request-item-create-container {
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
  
  .requirement-item .el-input {
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