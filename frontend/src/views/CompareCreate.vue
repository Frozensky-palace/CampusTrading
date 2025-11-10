<template>
  <div class="compare-create-container">
    <!-- 面包屑导航 -->
    <div class="breadcrumb-section">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/compare-tasks' }">比价任务</el-breadcrumb-item>
        <el-breadcrumb-item>发布比价</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 页面标题 -->
    <div class="page-header">
      <h1>发布比价任务</h1>
      <p>填写以下信息，获取最优惠的价格信息</p>
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
            <h3 class="section-title">基本信息</h3>
            <div class="form-row">
              <el-form-item label="任务标题" prop="title" class="form-item-full">
                <el-input
                  v-model="compareForm.title"
                  placeholder="请输入比价任务标题（5-50字）"
                  maxlength="50"
                  show-word-limit
                ></el-input>
              </el-form-item>
            </div>
            <div class="form-row">
              <el-form-item label="商品分类" prop="category" class="form-item-half">
                <el-select v-model="compareForm.category" placeholder="请选择商品分类">
                  <el-option label="数码电子" value="digital"></el-option>
                  <el-option label="学习资料" value="textbook"></el-option>
                  <el-option label="生活家居" value="home"></el-option>
                  <el-option label="体育用品" value="sports"></el-option>
                  <el-option label="服饰鞋包" value="clothing"></el-option>
                  <el-option label="其他类别" value="others"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="预算价格" prop="budget" class="form-item-half">
                <el-input-number
                  v-model="compareForm.budget"
                  placeholder="请输入您的预算价格"
                  :min="0"
                  :precision="2"
                  style="width: 100%;"
                ></el-input-number>
              </el-form-item>
            </div>
            <div class="form-row">
              <el-form-item label="期望新旧" prop="condition" class="form-item-half">
                <el-radio-group v-model="compareForm.condition">
                  <el-radio-button label="全新"></el-radio-button>
                  <el-radio-button label="9成新"></el-radio-button>
                  <el-radio-button label="8成新"></el-radio-button>
                  <el-radio-button label="7成新及以下"></el-radio-button>
                  <el-radio-button label="不限"></el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="期望完成时间" prop="deadline" class="form-item-half">
                <el-date-picker
                  v-model="compareForm.deadline"
                  type="datetime"
                  placeholder="选择期望完成时间"
                  :picker-options="dateOptions"
                  style="width: 100%;"
                ></el-date-picker>
              </el-form-item>
            </div>
          </div>

          <!-- 详细描述 -->
          <div class="form-section">
            <h3 class="section-title">详细描述</h3>
            <div class="form-row">
              <el-form-item label="任务描述" prop="description" class="form-item-full">
                <el-input
                  v-model="compareForm.description"
                  type="textarea"
                  placeholder="请详细描述您需要比价的商品信息，包括品牌、型号、配置等（10-1000字）"
                  :rows="6"
                  maxlength="1000"
                  show-word-limit
                ></el-input>
              </el-form-item>
            </div>
          </div>

          <!-- 交易信息 -->
          <div class="form-section">
            <h3 class="section-title">交易信息</h3>
            <div class="form-row">
              <el-form-item label="交易地点" prop="location" class="form-item-half">
                <el-input
                  v-model="compareForm.location"
                  placeholder="请输入您希望的交易地点（如：校园内、附近商圈等）"
                ></el-input>
              </el-form-item>
              <el-form-item label="交易方式" prop="tradeMethod" class="form-item-half">
                <el-radio-group v-model="compareForm.tradeMethod">
                  <el-radio-button label="线下交易"></el-radio-button>
                  <el-radio-button label="线上交易"></el-radio-button>
                  <el-radio-button label="不限"></el-radio-button>
                </el-radio-group>
              </el-form-item>
            </div>
          </div>

          <!-- 特殊要求 -->
          <div class="form-section">
            <h3 class="section-title">特殊要求</h3>
            <div class="form-row">
              <el-form-item label="具体要求" class="form-item-full">
                <div class="requirements-container">
                  <div v-for="(req, index) in compareForm.requirements" :key="index" class="requirement-item">
                    <el-input
                      v-model="req.content"
                      placeholder="输入具体要求（如：官方保修、配件齐全等）"
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
                    添加要求
                  </el-button>
                </div>
              </el-form-item>
            </div>
          </div>

          <!-- 标签 -->
          <div class="form-section">
            <h3 class="section-title">标签</h3>
            <div class="form-row">
              <el-form-item label="选择标签" class="form-item-full">
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
                <p class="tags-hint">点击选择标签，最多选择5个</p>
              </el-form-item>
            </div>
            <div class="form-row">
              <el-form-item label="自定义标签" class="form-item-full">
                <el-input
                  v-model="customTag"
                  placeholder="输入自定义标签，按回车添加"
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
            <h3 class="section-title">联系方式</h3>
            <div class="form-row">
              <el-form-item label="联系方式设置" class="form-item-full">
                <el-checkbox-group v-model="contactOptions">
                  <el-checkbox label="站内信">站内信（默认开启）</el-checkbox>
                  <el-checkbox label="手机">手机</el-checkbox>
                  <el-checkbox label="微信">微信</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </div>
            <div v-if="contactOptions.includes('手机')" class="form-row">
              <el-form-item label="手机号码" prop="phone" class="form-item-half">
                <el-input
                  v-model="compareForm.phone"
                  placeholder="请输入您的手机号码"
                  maxlength="11"
                ></el-input>
              </el-form-item>
            </div>
            <div v-if="contactOptions.includes('微信')" class="form-row">
              <el-form-item label="微信号码" prop="wechat" class="form-item-half">
                <el-input
                  v-model="compareForm.wechat"
                  placeholder="请输入您的微信号码"
                ></el-input>
              </el-form-item>
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="form-actions">
            <el-button @click="cancelCreate">取消</el-button>
            <el-button type="primary" @click="submitForm">发布比价任务</el-button>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import compareAPI from '@/api/compare';
const createCompareTask = compareAPI.createCompareTask;

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
const popularTags = [
  '笔记本电脑', '手机', '耳机', '考研资料', '教材',
  '显示器', '键盘', '相机', '运动鞋', '平板',
  '电动车', '自行车', '书籍', '乐器', '游戏设备'
];

// 已选标签
const selectedTags = ref<string[]>([]);

// 自定义标签输入
const customTag = ref('');

// 联系方式选项
const contactOptions = ref(['站内信']);

// 表单验证规则
const compareRules = {
  title: [
    { required: true, message: '请输入任务标题', trigger: 'blur' },
    { min: 5, max: 50, message: '标题长度在5到50个字符之间', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择商品分类', trigger: 'change' }
  ],
  budget: [
    { required: true, message: '请输入预算价格', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '预算价格必须大于0', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入任务描述', trigger: 'blur' },
    { min: 10, max: 1000, message: '描述长度在10到1000个字符之间', trigger: 'blur' }
  ],
  location: [
    { required: true, message: '请输入交易地点', trigger: 'blur' }
  ],
  deadline: [
    { required: true, message: '请选择期望完成时间', trigger: 'change' }
  ],
  phone: [
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号码',
      trigger: 'blur',
      required: () => contactOptions.value.includes('手机')
    }
  ],
  wechat: [
    {
      required: () => contactOptions.value.includes('微信'),
      message: '请输入微信号码',
      trigger: 'blur'
    }
  ]
};

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
    ElMessage.warning('最多只能选择5个标签');
  }
};

// 添加自定义标签
const addCustomTag = () => {
  const tag = customTag.value.trim();
  if (!tag) return;
  if (selectedTags.value.length >= 5) {
    ElMessage.warning('最多只能选择5个标签');
    return;
  }
  if (selectedTags.value.includes(tag)) {
    ElMessage.warning('该标签已添加');
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
    
    ElMessage.success('比价任务发布成功！');
    
    // 跳转到比价任务详情页
    router.push('/compare-tasks');
  } catch (error) {
    console.error('Failed to create compare task:', error);
    ElMessage.error('发布失败，请稍后重试');
  }
};

// 取消创建
const cancelCreate = () => {
  ElMessageBox.confirm(
    '确定要取消发布比价任务吗？已填写的内容将会丢失',
    '确认取消',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
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