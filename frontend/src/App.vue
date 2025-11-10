<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <Header />
    
    <!-- 主要内容区 -->
    <main class="main-container">
      <router-view />
    </main>
    
    <!-- 底部导航 -->
    <Footer />
    
    <!-- Element Plus的消息服务不需要在模板中声明 -->
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from './store';
import Header from './components/layout/Header.vue';
import Footer from './components/layout/Footer.vue';
import { ElMessage } from 'element-plus';
import { showMessage, showNotification, showLoading } from './utils/message';
import './assets/styles/main.scss';

// 路由和状态管理
const router = useRouter();
const userStore = useUserStore();

// 全局组件引用 - 移除无效的ref引用，Element Plus的消息服务不需要ref绑定

// 应用初始化
onMounted(async () => {
  try {
    // 初始化用户信息
    await userStore.initializeUser();
    
    // 监听路由变化，设置页面标题
    router.afterEach((to) => {
      if (to.meta.title) {
        document.title = `${to.meta.title} - 校园二手交易平台`;
      } else {
        document.title = '校园二手交易平台';
      }
    });
    
  } catch (error) {
    console.error('应用初始化失败:', error);
  }
});

// 全局错误处理
window.addEventListener('error', (event) => {
  console.error('全局错误:', event.error);
  ElMessage.error('发生未知错误，请刷新页面重试');
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('未处理的Promise拒绝:', event.reason);
  ElMessage.error('发生未知错误，请刷新页面重试');
});

// 导出全局属性，便于在其他组件中使用（如果需要）
// 注意：在<script setup>中，defineExpose不需要重新定义已导入的函数
defineExpose({
  showMessage,
  showNotification,
  showLoading
});
</script>

<style lang="scss">
/* 全局样式重置和应用级样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
  color: #333;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-container {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-container {
    padding: 10px;
  }
}

/* 打印样式 */
@media print {
  .header, .footer {
    display: none;
  }
  
  .main-container {
    box-shadow: none;
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

.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

/* 禁用状态样式 */
.disabled {
  opacity: 0.6;
  cursor: not-allowed !important;
  pointer-events: none;
}

/* 工具类 */
.text-center {
  text-align: center;
}

.text-left {
  text-align: left;
}

.text-right {
  text-align: right;
}

.mt-10 {
  margin-top: 10px;
}

.mt-20 {
  margin-top: 20px;
}

.mb-10 {
  margin-bottom: 10px;
}

.mb-20 {
  margin-bottom: 20px;
}

.p-10 {
  padding: 10px;
}

.p-20 {
  padding: 20px;
}

/* 加载动画 */
.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
