<template>
  <div class="request-item-create-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>发布求购</h1>
      <p>告诉我们您需要什么，让卖家主动联系您</p>
    </div>

    <!-- 发布表单 -->
    <div class="form-container">
      <el-form ref="requestFormRef" :model="requestForm" :rules="requestRules" label-width="120px">
        <!-- 求购信息 -->
        <el-form-item label="求购标题" prop="title">
          <el-input v-model="requestForm.title" placeholder="请输入求购标题" maxlength="50" show-word-limit />
        </el-form-item>

        <el-form-item label="商品分类" prop="category">
          <el-select v-model="requestForm.category" placeholder="请选择商品分类">
            <el-option label="数码电子" value="digital"></el-option>
            <el-option label="学习资料" value="textbook"></el-option>
            <el-option label="生活家居" value="home"></el-option>
            <el-option label="体育用品" value="sports"></el-option>
            <el-option label="服饰鞋包" value="clothing"></el-option>
            <el-option label="其他类别" value="others"></el-option>
          </el-select>
        </el-form-item>

        <!-- 价格信息 -->
        <el-form-item label="最高出价" prop="maxPrice">
          <el-input-number v-model="requestForm.maxPrice" :min="0" :precision="2" placeholder="请输入您能接受的最高价格" />
        </el-form-item>

        <!-- 期望新旧程度 -->
        <el-form-item label="期望新旧" prop="expectedCondition">
          <el-radio-group v-model="requestForm.expectedCondition">
            <el-radio-button label="全新">全新</el-radio-button>
            <el-radio-button label="九成新">九成新</el-radio-button>
            <el-radio-button label="八成新">八成新</el-radio-button>
            <el-radio-button label="七成新">七成新</el-radio-button>
            <el-radio-button label="六成新及以下">六成新及以下</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <!-- 求购描述 -->
        <el-form-item label="求购描述" prop="description">
          <el-input
            v-model="requestForm.description"
            type="textarea"
            :rows="8"
            placeholder="请详细描述您的求购需求，如品牌、型号、功能要求等"
            maxlength="2000"
            show-word-limit
          />
          <div class="description-tip">* 详细的描述可以提高匹配到合适商品的几率</div>
        </el-form-item>

        <!-- 交易信息 -->
        <el-form-item label="交易地点" prop="location">
          <el-input v-model="requestForm.location" placeholder="请输入您方便的交易地点" maxlength="100" show-word-limit />
        </el-form-item>

        <el-form-item label="交易方式" prop="shippingMethods">
          <el-checkbox-group v-model="requestForm.shippingMethods">
            <el-checkbox label="校园面交" name="shipping" />
            <el-checkbox label="快递邮寄" name="shipping" />
            <el-checkbox label="其他方式" name="shipping" />
          </el-checkbox-group>
        </el-form-item>

        <!-- 求购标签 -->
        <el-form-item label="求购标签">
          <el-input
            v-model="tagInput"
            placeholder="输入标签后按回车添加"
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
          <div class="tag-tip">* 最多添加5个标签，每个标签不超过8个字符</div>
        </el-form-item>

        <!-- 特殊要求（动态添加） -->
        <el-form-item label="特殊要求">
          <div v-for="(requirement, index) in requestForm.requirements" :key="index" class="requirement-item">
            <el-input
              v-model="requirement.name"
              placeholder="要求名称"
              style="width: 150px; margin-right: 10px;"
            />
            <span>:</span>
            <el-input
              v-model="requirement.value"
              placeholder="要求内容"
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
            添加要求
          </el-button>
          <div class="requirement-tip">* 最多添加10个特殊要求</div>
        </el-form-item>

        <!-- 期望完成时间 -->
        <el-form-item label="期望完成时间" prop="expectedCompletionDate">
          <el-date-picker
            v-model="requestForm.expectedCompletionDate"
            type="date"
            placeholder="选择期望完成时间"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <!-- 联系方式设置 -->
        <el-form-item label="联系方式设置">
          <div class="contact-settings">
            <el-checkbox-group v-model="contactOptions">
              <el-checkbox label="phone" name="contact">显示手机号码</el-checkbox>
              <el-checkbox label="wechat" name="contact">显示微信</el-checkbox>
              <el-checkbox label="qq" name="contact">显示QQ</el-checkbox>
            </el-checkbox-group>
            <div class="contact-hint">* 至少选择一种联系方式，方便卖家联系您</div>
          </div>
        </el-form-item>

        <!-- 提交按钮 -->
        <el-form-item>
          <div class="form-actions">
            <el-button @click="resetForm">重置</el-button>
            <el-button type="primary" @click="submitForm">发布求购</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>

    <!-- 发布成功提示 -->
    <el-dialog v-model="successDialogVisible" title="发布成功" width="400px" :show-close="false">
      <div class="success-content">
        <div class="success-icon">
          <i class="el-icon-success"></i>
        </div>
        <p class="success-text">恭喜您，求购信息发布成功！</p>
        <p class="success-hint">您的求购信息将在审核通过后显示在求购列表中</p>
      </div>
      <template #footer>
        <div class="dialog-actions">
          <el-button @click="viewRequestItem">查看求购</el-button>
          <el-button type="primary" @click="publishAnother">发布另一个</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { createRequestItem } from '@/api/requestItem';
import { useUserStore } from '@/store/user';

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
const requestRules = reactive({
  title: [
    { required: true, message: '请输入求购标题', trigger: 'blur' },
    { min: 2, max: 50, message: '求购标题长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择商品分类', trigger: 'change' }
  ],
  maxPrice: [
    { required: true, message: '请输入最高出价', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '价格必须大于0', trigger: 'blur' }
  ],
  expectedCondition: [
    { required: true, message: '请选择期望新旧程度', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入求购描述', trigger: 'blur' },
    { min: 10, max: 2000, message: '求购描述长度在 10 到 2000 个字符', trigger: 'blur' }
  ],
  location: [
    { required: true, message: '请输入交易地点', trigger: 'blur' },
    { min: 2, max: 100, message: '交易地点长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  shippingMethods: [
    { required: true, message: '请至少选择一种交易方式', trigger: 'change' }
  ],
  expectedCompletionDate: [
    { required: true, message: '请选择期望完成时间', trigger: 'change' }
  ]
});

// 添加标签
const addTag = () => {
  if (tagInput.value.trim() && requestForm.tags.length < 5) {
    if (requestForm.tags.includes(tagInput.value.trim())) {
      ElMessage.warning('该标签已存在');
    } else {
      requestForm.tags.push(tagInput.value.trim());
      tagInput.value = '';
    }
  } else if (requestForm.tags.length >= 5) {
    ElMessage.warning('最多只能添加5个标签');
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
    ElMessage.warning('最多只能添加10个特殊要求');
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
    ElMessage.error('请至少选择一种联系方式');
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
      ElMessage.error('发布求购失败，请稍后重试');
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
    ElMessage.warning('请先登录后发布求购信息');
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