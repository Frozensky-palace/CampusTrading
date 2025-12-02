<template>
  <div class="compare-create-container">
    <!-- 面包屑导航 -->
    <div class="breadcrumb-section">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">{{ $t('compare.create.breadcrumbHome') }}</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/compare-tasks' }">{{ $t('compare.create.breadcrumbList') }}</el-breadcrumb-item>
        <el-breadcrumb-item>{{ $t('compare.create.breadcrumbCreate') }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 页面标题 -->
    <div class="page-header">
      <h1>{{ $t('compare.create.title') }}</h1>
      <p>{{ $t('compare.create.subtitle') }}</p>
    </div>

    <!-- 发布表单 -->
    <div class="form-container">
      <el-card class="form-card">
        <el-form
          ref="compareFormRef"
          :model="compareForm"
          :rules="compareRules"
          label-width="120px"
          class="compare-form"
        >
          <!-- 基本信息 -->
          <div class="form-section">
            <h3 class="section-title">{{ $t('compare.create.basicInfo') }}</h3>
            <div class="form-row">
              <el-form-item :label="$t('compare.create.taskTitle')" prop="title" class="form-item-full">
                <el-input
                  v-model="compareForm.title"
                  :placeholder="$t('compare.create.taskTitlePlaceholder')"
                  maxlength="50"
                  show-word-limit
                ></el-input>
              </el-form-item>
            </div>
            <div class="form-row">
              <el-form-item :label="$t('compare.create.category')" prop="category" class="form-item-half">
                <el-select v-model="compareForm.category" :placeholder="$t('compare.create.categoryPlaceholder')">
                  <el-option :label="$t('item.categories.digital')" value="digital"></el-option>
                  <el-option :label="$t('item.categories.textbook')" value="textbook"></el-option>
                  <el-option :label="$t('item.categories.home')" value="home"></el-option>
                  <el-option :label="$t('item.categories.sports')" value="sports"></el-option>
                  <el-option :label="$t('item.categories.clothing')" value="clothing"></el-option>
                  <el-option :label="$t('item.categories.others')" value="others"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item :label="$t('compare.create.budget')" prop="budget" class="form-item-half">
                <el-input-number
                  v-model="compareForm.budget"
                  :placeholder="$t('compare.create.budgetPlaceholder')"
                  :min="0"
                  :precision="2"
                  style="width: 100%;"
                ></el-input-number>
              </el-form-item>
            </div>
            <div class="form-row">
              <el-form-item :label="$t('compare.create.expectedCondition')" prop="condition" class="form-item-half">
                <el-radio-group v-model="compareForm.condition">
                  <el-radio-button label="全新">{{ $t('compare.create.conditionNew') }}</el-radio-button>
                  <el-radio-button label="9成新">{{ $t('compare.create.condition90') }}</el-radio-button>
                  <el-radio-button label="8成新">{{ $t('compare.create.condition80') }}</el-radio-button>
                  <el-radio-button label="7成新及以下">{{ $t('compare.create.condition70') }}</el-radio-button>
                  <el-radio-button label="不限">{{ $t('compare.create.conditionAny') }}</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item :label="$t('compare.create.deadline')" prop="deadline" class="form-item-half">
                <el-date-picker
                  v-model="compareForm.deadline"
                  type="datetime"
                  :placeholder="$t('compare.create.deadlinePlaceholder')"
                  :picker-options="dateOptions"
                  style="width: 100%;"
                ></el-date-picker>
              </el-form-item>
            </div>
          </div>

          <!-- 详细描述 -->
          <div class="form-section">
            <h3 class="section-title">{{ $t('compare.create.detailDescription') }}</h3>
            <div class="form-row">
              <el-form-item :label="$t('compare.create.taskDescription')" prop="description" class="form-item-full">
                <el-input
                  v-model="compareForm.description"
                  type="textarea"
                  :placeholder="$t('compare.create.taskDescPlaceholder')"
                  :rows="6"
                  maxlength="1000"
                  show-word-limit
                ></el-input>
              </el-form-item>
            </div>
          </div>

          <!-- 交易信息 -->
          <div class="form-section">
            <h3 class="section-title">{{ $t('compare.create.tradeInfo') }}</h3>
            <div class="form-row">
              <el-form-item :label="$t('compare.create.tradeLocation')" prop="location" class="form-item-half">
                <el-input
                  v-model="compareForm.location"
                  :placeholder="$t('compare.create.tradeLocationPlaceholder')"
                ></el-input>
              </el-form-item>
              <el-form-item :label="$t('compare.create.tradeMethod')" prop="tradeMethod" class="form-item-half">
                <el-radio-group v-model="compareForm.tradeMethod">
                  <el-radio-button label="线下交易">{{ $t('compare.create.methodOffline') }}</el-radio-button>
                  <el-radio-button label="线上交易">{{ $t('compare.create.methodOnline') }}</el-radio-button>
                  <el-radio-button label="不限">{{ $t('compare.create.methodAny') }}</el-radio-button>
                </el-radio-group>
              </el-form-item>
            </div>
          </div>

          <!-- 特殊要求 -->
          <div class="form-section">
            <h3 class="section-title">{{ $t('compare.create.specialRequirements') }}</h3>
            <div class="form-row">
              <el-form-item :label="$t('compare.create.specialRequirements')" class="form-item-full">
                <div class="requirements-container">
                  <div v-for="(req, index) in compareForm.requirements" :key="index" class="requirement-item">
                    <el-input
                      v-model="req.content"
                      :placeholder="$t('compare.create.requirementPlaceholder')"
                      style="margin-bottom: 10px;"
                    ></el-input>
                    <el-button
                      type="danger"
                      icon="el-icon-delete"
                      @click="removeRequirement(index)"
                      size="small"
                    ></el-button>
                  </div>
                  <el-button
                    type="primary"
                    icon="el-icon-plus"
                    @click="addRequirement"
                    size="small"
                    class="add-requirement-btn"
                  >
                    {{ $t('compare.create.addRequirement') }}
                  </el-button>
                </div>
              </el-form-item>
            </div>
          </div>

          <!-- 标签 -->
          <div class="form-section">
            <h3 class="section-title">{{ $t('compare.create.tagsSection') }}</h3>
            <div class="form-row">
              <el-form-item :label="$t('compare.create.selectTags')" class="form-item-full">
                <div class="tags-selector">
                  <el-tag
                    v-for="tag in popularTags"
                    :key="tag"
                    :disable-transitions="false"
                    :class="{ 'active-tag': selectedTags.includes(tag) }"
                    @click="toggleTag(tag)"
                    effect="plain"
                  >
                    {{ tag }}
                  </el-tag>
                </div>
                <p class="tags-hint">{{ $t('compare.create.tagsHint') }}</p>
              </el-form-item>
            </div>
            <div class="form-row">
              <el-form-item :label="$t('compare.create.customTag')" class="form-item-full">
                <el-input
                  v-model="customTag"
                  :placeholder="$t('compare.create.customTagPlaceholder')"
                  @keyup.enter="addCustomTag"
                  :maxlength="10"
                  show-word-limit
                ></el-input>
                <div class="custom-tags" v-if="selectedTags.length > 0">
                  <el-tag
                    v-for="tag in selectedTags"
                    :key="tag"
                    closable
                    @close="removeTag(tag)"
                    type="info"
                  >
                    {{ tag }}
                  </el-tag>
                </div>
              </el-form-item>
            </div>
          </div>

          <!-- 联系方式 -->
          <div class="form-section">
            <h3 class="section-title">{{ $t('compare.create.contactSettings') }}</h3>
            <div class="form-row">
              <el-form-item :label="$t('compare.create.contactSettingsLabel')" class="form-item-full">
                <el-checkbox-group v-model="contactOptions">
                  <el-checkbox label="站内信">{{ $t('compare.create.internalMessage') }}</el-checkbox>
                  <el-checkbox label="手机">{{ $t('compare.create.phoneNumber') }}</el-checkbox>
                  <el-checkbox label="微信">{{ $t('compare.create.wechatNumber') }}</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </div>
            <div v-if="contactOptions.includes('手机')" class="form-row">
              <el-form-item :label="$t('compare.create.phoneLabel')" prop="phone" class="form-item-half">
                <el-input
                  v-model="compareForm.phone"
                  :placeholder="$t('compare.create.phoneInputPlaceholder')"
                  maxlength="11"
                ></el-input>
              </el-form-item>
            </div>
            <div v-if="contactOptions.includes('微信')" class="form-row">
              <el-form-item :label="$t('compare.create.wechatLabel')" prop="wechat" class="form-item-half">
                <el-input
                  v-model="compareForm.wechat"
                  :placeholder="$t('compare.create.wechatInputPlaceholder')"
                ></el-input>
              </el-form-item>
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="form-actions">
            <el-button @click="cancelCreate">{{ $t('compare.create.cancel') }}</el-button>
            <el-button type="primary" @click="submitForm">{{ $t('compare.create.submit') }}</el-button>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useI18n } from 'vue-i18n';
import compareAPI from '@/api/compare';
const createCompareTask = compareAPI.createCompareTask;

// i18n
const { t } = useI18n();

// 路由
const router = useRouter();

// 表单引用
const compareFormRef = ref<InstanceType<any>>();

// 表单数据
const compareForm = reactive({
  title: '',
  category: '',
  budget: null,
  condition: '不限',
  description: '',
  location: '',
  tradeMethod: '不限',
  deadline: null,
  requirements: [] as { content: string }[],
  tags: [] as string[],
  phone: '',
  wechat: ''
});

// 日期选择器配置
const dateOptions = {
  disabledDate: (time: Date) => {
    return time.getTime() < Date.now() - 8.64e7;
  }
};

// 热门标签
const popularTags = computed(() => [
  t('item.list.popularTags.laptop'),
  t('item.list.popularTags.phone'),
  t('item.list.popularTags.headphones'),
  t('item.list.popularTags.examMaterials'),
  t('item.list.popularTags.textbook'),
  t('item.list.popularTags.monitor'),
  t('item.list.popularTags.keyboard'),
  t('item.list.popularTags.camera'),
  t('item.list.popularTags.sneakers'),
  t('item.list.popularTags.tablet'),
  t('item.list.popularTags.electricScooter'),
  t('item.list.popularTags.bicycle'),
  t('item.list.popularTags.books'),
  t('item.list.popularTags.instrument'),
  t('item.list.popularTags.gamingDevice')
]);

// 已选标签
const selectedTags = ref<string[]>([]);

// 自定义标签输入
const customTag = ref('');

// 联系方式选项
const contactOptions = ref(['站内信']);

// 表单验证规则
const compareRules = computed(() => ({
  title: [
    { required: true, message: t('compare.create.validation.titleRequired'), trigger: 'blur' },
    { min: 5, max: 50, message: t('compare.create.validation.titleLength'), trigger: 'blur' }
  ],
  category: [
    { required: true, message: t('compare.create.validation.categoryRequired'), trigger: 'change' }
  ],
  budget: [
    { required: true, message: t('compare.create.validation.budgetRequired'), trigger: 'blur' },
    { type: 'number', min: 0.01, message: t('compare.create.validation.budgetMin'), trigger: 'blur' }
  ],
  description: [
    { required: true, message: t('compare.create.validation.descriptionRequired'), trigger: 'blur' },
    { min: 10, max: 1000, message: t('compare.create.validation.descriptionLength'), trigger: 'blur' }
  ],
  location: [
    { required: true, message: t('compare.create.validation.locationRequired'), trigger: 'blur' }
  ],
  deadline: [
    { required: true, message: t('compare.create.validation.deadlineRequired'), trigger: 'change' }
  ],
  phone: [
    {
      pattern: /^1[3-9]\d{9}$/,
      message: t('compare.create.validation.phoneInvalid'),
      trigger: 'blur',
      required: () => contactOptions.value.includes('手机')
    }
  ],
  wechat: [
    {
      required: () => contactOptions.value.includes('微信'),
      message: t('compare.create.validation.wechatRequired'),
      trigger: 'blur'
    }
  ]
}));

// 添加要求
const addRequirement = () => {
  compareForm.requirements.push({ content: '' });
};

// 移除要求
const removeRequirement = (index: number) => {
  compareForm.requirements.splice(index, 1);
};

// 切换标签选择
const toggleTag = (tag: string) => {
  const index = selectedTags.value.indexOf(tag);
  if (index > -1) {
    selectedTags.value.splice(index, 1);
  } else if (selectedTags.value.length < 5) {
    selectedTags.value.push(tag);
  } else {
    ElMessage.warning(t('compare.create.maxTags'));
  }
};

// 添加自定义标签
const addCustomTag = () => {
  const tag = customTag.value.trim();
  if (!tag) return;
  if (selectedTags.value.length >= 5) {
    ElMessage.warning(t('compare.create.maxTags'));
    return;
  }
  if (selectedTags.value.includes(tag)) {
    ElMessage.warning(t('compare.create.tagExists'));
    return;
  }
  selectedTags.value.push(tag);
  customTag.value = '';
};

// 移除标签
const removeTag = (tag: string) => {
  const index = selectedTags.value.indexOf(tag);
  if (index > -1) {
    selectedTags.value.splice(index, 1);
  }
};

// 提交表单
const submitForm = async () => {
  if (!compareFormRef.value) return;
  
  try {
    await compareFormRef.value.validate();
    
    // 准备提交数据 - 转换为API期望的格式
    const taskData = {
      title: compareForm.title,
      description: compareForm.description,
      items: [{
        name: compareForm.title,
        price: compareForm.budget || 0,
        source: '用户期望',
        description: compareForm.description
      }],
      status: 'active',
      public: true,
      // 添加额外字段供后端使用
      category: compareForm.category,
      location: compareForm.location,
      tradeMethod: compareForm.tradeMethod,
      deadline: compareForm.deadline,
      requirements: compareForm.requirements
        .map(req => req.content.trim())
        .filter(content => content !== '')
      ,
      tags: selectedTags.value,
      contactInfo: {
        phone: compareForm.phone,
        wechat: compareForm.wechat
      }
    };
    
    // 调用API提交数据
    await createCompareTask(taskData);

    ElMessage.success(t('compare.create.publishSuccess'));

    // 跳转到比价任务详情页
    router.push('/compare-tasks');
  } catch (error) {
    console.error('Failed to create compare task:', error);
    ElMessage.error(t('compare.create.publishFailed'));
  }
};

// 取消创建
const cancelCreate = () => {
  ElMessageBox.confirm(
    t('compare.create.cancelConfirm'),
    t('compare.create.cancelTitle'),
    {
      confirmButtonText: t('common.confirm'),
      cancelButtonText: t('common.cancel'),
      type: 'warning'
    }
  ).then(() => {
    router.push('/compare-tasks');
  }).catch(() => {
    // 用户取消操作
  });
};
</script>

<style lang="scss" scoped>
.compare-create-container {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

/* 面包屑导航 */
.breadcrumb-section {
  margin-bottom: 20px;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 8px;
}

.page-header h1 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #333;
}

.page-header p {
  font-size: 16px;
  color: #666;
}

/* 表单容器 */
.form-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-card {
  border: none;
  box-shadow: none;
}

/* 表单样式 */
.compare-form {
  padding: 20px;
}

.form-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e0e0e0;
}

.form-row {
  margin-bottom: 20px;
}

.form-row:last-child {
  margin-bottom: 0;
}

.form-item-full {
  width: 100%;
}

.form-item-half {
  width: calc(50% - 10px);
  display: inline-block;
  margin-right: 20px;
}

.form-item-half:last-child {
  margin-right: 0;
}

/* 要求列表 */
.requirements-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.requirement-item {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.requirement-item .el-input {
  flex: 1;
}

.add-requirement-btn {
  align-self: flex-start;
  margin-top: 10px;
}

/* 标签选择器 */
.tags-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.tags-hint {
  font-size: 12px;
  color: #999;
  margin-top: 10px;
}

.active-tag {
  background-color: #409eff !important;
  color: white !important;
}

.custom-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

/* 联系方式 */
.el-checkbox {
  margin-right: 20px;
  margin-bottom: 10px;
}

/* 表单操作按钮 */
.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.form-actions .el-button {
  min-width: 120px;
  padding: 10px 20px;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .compare-create-container {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 24px;
  }
  
  .form-section {
    padding: 15px;
  }
  
  .section-title {
    font-size: 16px;
  }
  
  .form-item-half {
    width: 100%;
    margin-right: 0;
    margin-bottom: 20px;
  }
  
  .form-item-half:last-child {
    margin-bottom: 0;
  }
  
  .tags-selector {
    flex-direction: column;
  }
  
  .tags-selector .el-tag {
    width: auto;
  }
  
  .custom-tags {
    flex-direction: column;
  }
  
  .custom-tags .el-tag {
    width: auto;
  }
  
  .el-checkbox {
    display: block;
    margin-bottom: 15px;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 15px;
  }
  
  .form-actions .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .compare-create-container {
    padding: 10px;
  }
  
  .page-header {
    padding: 20px 15px;
  }
  
  .page-header h1 {
    font-size: 20px;
  }
  
  .page-header p {
    font-size: 14px;
  }
  
  .compare-form {
    padding: 15px;
  }
  
  .form-section {
    padding: 10px;
  }
  
  .section-title {
    font-size: 14px;
  }
  
  .requirement-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .requirement-item .el-button {
    align-self: flex-end;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-section {
  animation: fadeIn 0.3s ease-out;
}

.form-section:nth-child(n+2) {
  animation-delay: 0.1s;
}

.form-section:nth-child(n+3) {
  animation-delay: 0.2s;
}

.form-section:nth-child(n+4) {
  animation-delay: 0.3s;
}

.form-section:nth-child(n+5) {
  animation-delay: 0.4s;
}

.form-section:nth-child(n+6) {
  animation-delay: 0.5s;
}
</style>