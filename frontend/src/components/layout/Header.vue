<template>
  <header class="header">
    <div class="header-container">
      <!-- 网站Logo和名称 -->
      <div class="logo-container">
        <router-link to="/" class="logo">
          <span class="logo-text">校园二手交易平台</span>
        </router-link>
      </div>
      
      <!-- 导航菜单 - 桌面版 -->
      <nav class="main-nav">
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">首页</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/items" class="nav-link" :class="{ active: route.path.startsWith('/items') }">商品列表</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/requests" class="nav-link" :class="{ active: route.path.startsWith('/requests') }">求购信息</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/compare" class="nav-link" :class="{ active: route.path.startsWith('/compare') }">比价中心</router-link>
          </li>
          <li class="nav-item">
            <a href="#" class="nav-link">关于我们</a>
          </li>
        </ul>
      </nav>
      
      <!-- 右侧功能区 -->
      <div class="header-actions">
        <!-- 搜索框 -->
        <div class="search-container">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索商品或求购信息..."
            class="search-input"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button icon="el-icon-search" @click="handleSearch"></el-button>
            </template>
          </el-input>
        </div>
        
        <!-- 发布按钮 -->
        <div class="publish-container" v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click">
            <el-button type="primary" icon="el-icon-plus">发布</el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="goToPublishItem">
                  <i class="el-icon-goods"></i> 发布商品
                </el-dropdown-item>
                <el-dropdown-item @click="goToPublishRequest">
                  <i class="el-icon-shopping-bag-1"></i> 发布求购
                </el-dropdown-item>
                <el-dropdown-item @click="goToCreateCompare">
                  <i class="el-icon-s-data"></i> 创建比价
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        
        <!-- 用户菜单 -->
        <div class="user-container">
          <template v-if="userStore.isLoggedIn">
            <!-- 消息通知 -->
            <el-badge :value="unreadCount" class="notification-badge">
              <el-button
                icon="el-icon-bell"
                class="notification-btn"
                @click="goToMessages"
              ></el-button>
            </el-badge>
            
            <!-- 用户头像 -->
            <el-dropdown trigger="hover">
              <div class="user-avatar">
                <img :src="userStore.user?.avatar || defaultAvatar" alt="用户头像" />
                <span class="user-name">{{ userStore.user?.nickname || userStore.user?.username }}</span>
                <i class="el-icon-arrow-down el-icon--right"></i>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="goToProfile">
                    <i class="el-icon-user"></i> 个人中心
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToMyItems">
                    <i class="el-icon-goods"></i> 我的商品
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToMyRequests">
                    <i class="el-icon-shopping-bag-1"></i> 我的求购
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToMyTransactions">
                    <i class="el-icon-s-order"></i> 交易记录
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToFavorites">
                    <i class="el-icon-star-off"></i> 我的收藏
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.isAdmin" @click="goToAdmin">
                    <i class="el-icon-setting"></i> 管理后台
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    <i class="el-icon-logout"></i> 退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          
          <!-- 未登录 -->
          <template v-else>
            <el-button type="primary" size="small" class="login-btn" @click="goToLogin">登录</el-button>
            <el-button size="small" class="register-btn" @click="goToRegister">注册</el-button>
          </template>
        </div>
        
        <!-- 移动端菜单按钮 -->
        <el-button
          icon="el-icon-menu" 
          class="mobile-menu-btn"
          @click="toggleMobileMenu"
          v-show="!showMobileMenu"
        ></el-button>
        <el-button
          icon="el-icon-close" 
          class="mobile-menu-btn"
          @click="toggleMobileMenu"
          v-show="showMobileMenu"
        ></el-button>
      </div>
    </div>
    
    <!-- 移动端菜单 -->
    <div class="mobile-menu" v-show="showMobileMenu">
      <ul class="mobile-nav-list">
        <li class="mobile-nav-item">
          <router-link to="/" class="mobile-nav-link" :class="{ active: route.path === '/' }" @click="toggleMobileMenu">首页</router-link>
        </li>
        <li class="mobile-nav-item">
          <router-link to="/items" class="mobile-nav-link" :class="{ active: route.path.startsWith('/items') }" @click="toggleMobileMenu">商品列表</router-link>
        </li>
        <li class="mobile-nav-item">
          <router-link to="/requests" class="mobile-nav-link" :class="{ active: route.path.startsWith('/requests') }" @click="toggleMobileMenu">求购信息</router-link>
        </li>
        <li class="mobile-nav-item">
          <router-link to="/compare" class="mobile-nav-link" :class="{ active: route.path.startsWith('/compare') }" @click="toggleMobileMenu">比价中心</router-link>
        </li>
        <li class="mobile-nav-item">
          <a href="#" class="mobile-nav-link" @click="toggleMobileMenu">关于我们</a>
        </li>
        <li v-if="userStore.isLoggedIn" class="mobile-nav-item">
          <a href="#" class="mobile-nav-link" @click="toggleMobileMenu">发布商品</a>
        </li>
        <li v-if="userStore.isLoggedIn" class="mobile-nav-item">
          <a href="#" class="mobile-nav-link" @click="toggleMobileMenu">发布求购</a>
        </li>
        <li v-if="userStore.isLoggedIn" class="mobile-nav-item">
          <a href="#" class="mobile-nav-link" @click="toggleMobileMenu">个人中心</a>
        </li>
        <li v-if="userStore.isLoggedIn" class="mobile-nav-item">
          <a href="#" class="mobile-nav-link" @click="toggleMobileMenu">我的消息</a>
        </li>
        <li v-if="userStore.isAdmin" class="mobile-nav-item">
          <a href="#" class="mobile-nav-link" @click="toggleMobileMenu">管理后台</a>
        </li>
        <li v-if="userStore.isLoggedIn" class="mobile-nav-item">
          <a href="#" class="mobile-nav-link" @click="handleLogout">退出登录</a>
        </li>
        <li v-else class="mobile-nav-item">
          <el-button type="primary" size="small" class="mobile-login-btn" @click="handleMobileLogin">登录</el-button>
        </li>
        <li class="mobile-nav-item">
          <el-button size="small" class="mobile-register-btn" @click="handleMobileRegister">注册</el-button>
        </li>
      </ul>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/store/user';
import { ElMessage } from 'element-plus';

// 路由和状态管理
const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

// 响应式数据
const searchKeyword = ref('');
const showMobileMenu = ref(false);
const unreadCount = ref(3); // 示例：未读消息数量
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';

// 搜索处理
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({
      path: '/items',
      query: { keyword: searchKeyword.value.trim() }
    });
  } else {
    ElMessage.warning('请输入搜索关键词');
  }
};

// 切换移动端菜单
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
};

// 退出登录
const handleLogout = async () => {
  try {
    await userStore.logout();
    ElMessage.success('退出登录成功');
    router.push('/');
  } catch (error) {
    ElMessage.error('退出登录失败');
  }
};

// 导航到发布商品页面
const goToPublishItem = () => {
  router.push('/items/create');
};

// 导航到发布求购页面
const goToPublishRequest = () => {
  router.push('/requests/create');
};

// 导航到创建比价页面
const goToCreateCompare = () => {
  router.push('/compare/create');
};

// 导航到消息页面
const goToMessages = () => {
  ElMessage.info('消息功能暂不可用');
};

// 导航到个人中心
const goToProfile = () => {
  ElMessage.info('个人中心功能暂不可用');
};

// 导航到我的商品
const goToMyItems = () => {
  router.push('/items');
};

// 导航到我的求购
const goToMyRequests = () => {
  router.push('/requests/my');
};

// 导航到交易记录
const goToMyTransactions = () => {
  ElMessage.info('交易记录功能暂不可用');
};

// 导航到我的收藏
const goToFavorites = () => {
  ElMessage.info('收藏功能暂不可用');
};

// 导航到管理后台
const goToAdmin = () => {
  ElMessage.info('管理后台功能暂不可用');
};

// 导航到登录页面 - 使用更直接的实现
const goToLogin = () => {
  console.log('登录按钮被点击');
  router.push('/login');
};

// 导航到注册页面 - 使用更直接的实现
const goToRegister = () => {
  console.log('注册按钮被点击');
  router.push('/register');
};

// 移动端登录处理
const handleMobileLogin = () => {
  console.log('移动端登录按钮被点击');
  toggleMobileMenu();
  setTimeout(() => {
    router.push('/login');
  }, 100);
};

// 移动端注册处理
const handleMobileRegister = () => {
  console.log('移动端注册按钮被点击');
  toggleMobileMenu();
  setTimeout(() => {
    router.push('/register');
  }, 100);
};
</script>

<style lang="scss" scoped>
.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

/* Logo样式 */
.logo-container {
  flex-shrink: 0;
}

.logo {
  display: flex;
  align-items: center;
  color: #333;
  text-decoration: none;
  font-weight: bold;
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.logo-text {
  font-size: 20px;
  color: #333;
}

/* 主导航样式 */
.main-nav {
  display: flex;
  align-items: center;
}

.nav-list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  margin: 0 15px;
}

.nav-link {
  color: #333;
  text-decoration: none;
  padding: 5px 0;
  position: relative;
  transition: color 0.3s;
  font-size: 16px;
}

.nav-link:hover {
  color: #409eff;
}

.nav-link.active {
  color: #409eff;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #409eff;
}

/* 右侧功能区样式 */
.header-actions {
  display: flex;
  align-items: center;
}

.search-container {
  margin-right: 15px;
  position: relative;
}

.search-input {
  width: 200px;
  height: 36px;
}

.publish-container {
  margin-right: 15px;
}

.user-container {
  display: flex;
  align-items: center;
}

.notification-badge {
  margin-right: 10px;
}

.notification-btn {
  background: none;
  border: none;
  color: #666;
}

.user-avatar {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-avatar:hover {
  background-color: #f5f5f5;
}

.user-avatar img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin-right: 8px;
}

.user-name {
  font-size: 14px;
  color: #333;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.login-link,
.register-link {
  margin: 0 10px;
  font-size: 14px;
}

.register-link {
  color: #409eff;
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: #666;
}

/* 移动端菜单 */
.mobile-menu {
  display: none;
  background-color: #fff;
  border-top: 1px solid #eee;
}

.mobile-nav-list {
  list-style: none;
  margin: 0;
  padding: 10px 0;
}

.mobile-nav-item {
  margin: 0;
}

.mobile-nav-link {
  display: block;
  padding: 12px 20px;
  color: #333;
  text-decoration: none;
  font-size: 16px;
  border-bottom: 1px solid #f5f5f5;
  transition: background-color 0.3s;
}

.mobile-nav-link:hover {
  background-color: #f5f5f5;
}

.mobile-nav-link.active {
  color: #409eff;
  background-color: #ecf5ff;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .search-input {
    width: 150px;
  }
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 10px;
  }
  
  .main-nav {
    display: none;
  }
  
  .search-container {
    display: none;
  }
  
  .publish-container {
    display: none;
  }
  
  .user-container {
    display: none;
  }
  
  .mobile-menu-btn {
    display: block;
  }
  
  .mobile-menu {
    display: block;
  }
  
  .logo-text {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .header-container {
    height: 50px;
  }
  
  .logo-text {
    font-size: 14px;
  }
  
  .mobile-nav-link {
    padding: 10px 15px;
    font-size: 14px;
  }
}
</style>