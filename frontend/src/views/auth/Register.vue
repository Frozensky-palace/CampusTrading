<template>
  <div class="register-container">
    <div class="register-form">
      <h1>{{ $t('auth.registerTitle') }}</h1>
      <el-form :model="registerForm" :rules="rules" ref="registerFormRef" label-width="80px">
        <el-form-item :label="$t('user.username')" prop="username">
          <el-input v-model="registerForm.username" :placeholder="$t('validation.required')" />
        </el-form-item>
        <el-form-item :label="$t('user.email')" prop="email">
          <el-input v-model="registerForm.email" type="email" :placeholder="$t('validation.required')" />
        </el-form-item>
        <el-form-item :label="$t('user.password')" prop="password">
          <el-input v-model="registerForm.password" type="password" :placeholder="$t('validation.required')" show-password />
        </el-form-item>
        <el-form-item :label="$t('user.confirmPassword')" prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" :placeholder="$t('validation.required')" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading" class="register-button">{{ $t('auth.registerBtn') }}</el-button>
        </el-form-item>
        <el-form-item>
          <span>{{ $t('auth.hasAccount') }}</span>
          <el-link type="primary" :underline="false" @click="goToLogin">{{ $t('auth.goLogin') }}</el-link>
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
import { register } from '@/api/auth';

const { t } = useI18n();
const router = useRouter();
const registerFormRef = ref();
const loading = ref(false);

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const rules = computed(() => ({
  username: [
    { required: true, message: t('validation.required'), trigger: 'blur' },
    { min: 3, max: 20, message: t('validation.usernameMin'), trigger: 'blur' }
  ],
  email: [
    { required: true, message: t('validation.required'), trigger: 'blur' },
    { type: 'email', message: t('validation.emailInvalid'), trigger: 'blur' }
  ],
  password: [
    { required: true, message: t('validation.required'), trigger: 'blur' },
    { min: 6, message: t('validation.passwordMin'), trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: t('validation.required'), trigger: 'blur' },
    {
      validator: (_rule: any, value: string, callback: Function) => {
        if (value !== registerForm.password) {
          callback(new Error(t('validation.passwordNotMatch')));
        } else {
          callback();
        }
      },
      trigger: 'blur'
    }
  ]
}));

const handleRegister = async () => {
  try {
    await registerFormRef.value.validate();
    loading.value = true;

    // 调用注册接口，添加student_id参数（这里使用邮箱前缀作为学号）
    const studentId = registerForm.email.split('@')[0];
    await register({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password,
      student_id: studentId
    });

    ElMessage.success(t('auth.registerSuccess'));

    // 注册成功后跳转到登录页
    router.push('/login');
  } catch (error) {
    console.error('注册失败:', error);
    // 尝试获取更详细的错误信息
    if ((error as any).response?.data?.message) {
      ElMessage.error((error as any).response.data.message);
    } else {
      ElMessage.error(t('message.operationFailed'));
    }
  } finally {
    loading.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.register-form {
  width: 400px;
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.register-form h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #303133;
}

.register-button {
  width: 100%;
}

.el-form-item:last-child {
  text-align: center;
  margin-bottom: 0;
}
</style>