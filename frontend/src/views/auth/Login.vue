<template>
  <div class="login-container">
    <div class="login-form">
      <h1>{{ $t('auth.loginTitle') }}</h1>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
        <el-form-item :label="$t('user.username')" prop="username">
          <el-input v-model="loginForm.username" :placeholder="$t('validation.required')" />
        </el-form-item>
        <el-form-item :label="$t('user.password')" prop="password">
          <el-input v-model="loginForm.password" type="password" :placeholder="$t('validation.required')" show-password />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="loginForm.remember">{{ $t('auth.rememberMe') }}</el-checkbox>
          <el-link type="primary" :underline="false" @click="goToRegister" class="register-link">{{ $t('auth.goRegister') }}</el-link>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" class="login-button">{{ $t('auth.loginBtn') }}</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useI18n } from 'vue-i18n';
import { login } from '@/api/auth';
import { useUserStore } from '@/store/user';

const { t } = useI18n();
const router = useRouter();
const userStore = useUserStore();
const loginFormRef = ref();
const loading = ref(false);

const loginForm = reactive({
  username: '',
  password: '',
  remember: false
});

const rules = computed(() => ({
  username: [
    { required: true, message: t('validation.required'), trigger: 'blur' }
  ],
  password: [
    { required: true, message: t('validation.required'), trigger: 'blur' }
  ]
}));

const handleLogin = async () => {
  console.log('handleLogin函数被调用');
  try {
    await loginFormRef.value.validate();
    loading.value = true;

    console.log('表单验证通过，准备发送登录请求');
    console.log('登录参数 - 用户名:', loginForm.username, '密码:', loginForm.password ? '******' : '未输入');

    // 调用登录接口
    console.log('正在调用login API...');
    // 注意：request.ts中的响应拦截器已经将返回值处理为response.data
    const data = await login(loginForm.username, loginForm.password);

    console.log('登录响应数据:', data);

    // 安全地从响应数据中提取，后端返回的是access_token字段
    const token = data?.access_token;

    if (!token) {
      throw new Error('无效的响应数据结构：缺少access_token');
    }

    console.log('提取的token:', token);

    // 保存token到store
    userStore.setToken(token);

    // 由于后端没有返回用户信息，我们使用用户名作为基础信息
    userStore.setUserInfo({
      id: '', // 暂时为空，后续可通过获取用户信息接口补充
      username: loginForm.username || '',
      nickname: loginForm.username || '', // 使用用户名作为昵称
      avatar: '', // 暂时为空，后续可扩展
      email: '', // 暂时为空，后续可扩展
      phone: '', // 暂时为空，后续可扩展
      role: 'user', // 默认为普通用户
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });

    ElMessage.success(t('auth.loginSuccess'));

    // 跳转到首页或之前的页面
    router.push('/');
  } catch (error: any) {
    console.error('登录失败:', error);
    // 处理错误信息
    let errorMsg = t('message.operationFailed');
    if (error.response) {
      // 直接使用response中的错误信息
      errorMsg = error.response.data?.message || error.response.data || errorMsg;
      console.log('响应错误详情:', error.response);
    } else if (error.message) {
      errorMsg = error.message;
    }
    ElMessage.error(errorMsg);
  } finally {
    loading.value = false;
  }
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.login-form {
  width: 400px;
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.login-form h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #303133;
}

.register-link {
  float: right;
}

.login-button {
  width: 100%;
}
</style>