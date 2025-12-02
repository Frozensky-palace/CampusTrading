<template>
  <header class="header">
    <div class="header-container">
      <!-- 网站Logo和名称 -->
      <div class="logo-container">
        <router-link to="/" class="logo">
          <span class="logo-text">{{ $t('footer.about') }}</span>
        </router-link>
      </div>

      <!-- 导航菜单 - 桌面版 -->
      <nav class="main-nav">
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">{{ $t('nav.home') }}</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/items" class="nav-link" :class="{ active: route.path.startsWith('/items') }">{{ $t('nav.items') }}</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/rent/list" class="nav-link" :class="{ active: route.path.startsWith('/rent') }">{{ $t('item.transactionType.rent') }}</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/requests" class="nav-link" :class="{ active: route.path.startsWith('/requests') }">{{ $t('nav.requests') }}</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/compare" class="nav-link" :class="{ active: route.path.startsWith('/compare') }">{{ $t('nav.compare') }}</router-link>
          </li>
          <li class="nav-item">
            <a href="#" class="nav-link">{{ $t('nav.about') }}</a>
          </li>
        </ul>
      </nav>

      <!-- 右侧功能区 -->
      <div class="header-actions">
        <!-- 搜索框 -->
        <div class="search-container">
          <el-input
            v-model="searchKeyword"
            :placeholder="$t('common.search') + '...'"
            class="search-input"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button @click="handleSearch">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>

        <!-- 发布按钮 -->
        <div class="publish-container" v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click">
            <el-button type="primary">{{ $t('nav.publish') }}</el-button>
            <template #dropdown>
              <el-dropdown-menu>
                  <el-dropdown-item @click="goToPublishItem">
                    {{ $t('nav.publishItem') }}
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToPublishRent">
                    {{ $t('item.transactionType.rent') }}
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToPublishRequest">
                    {{ $t('nav.publishRequest') }}
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToCreateCompare">
                    {{ $t('nav.createCompare') }}
                  </el-dropdown-item>
                </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>

        <!-- 语言切换 -->
        <div class="language-switch">
          <el-dropdown trigger="click" @command="handleLanguageChange">
            <el-button circle>
              <el-icon><Eleme /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="zh-CN" :class="{ 'is-active': currentLocale === 'zh-CN' }">
                  🇨🇳 {{ $t('language.zh') }}
                </el-dropdown-item>
                <el-dropdown-item command="en-US" :class="{ 'is-active': currentLocale === 'en-US' }">
                  🇺🇸 {{ $t('language.en') }}
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
                class="notification-btn"
                @click="goToMessages"
              >
                <el-icon><Bell /></el-icon>
              </el-button>
            </el-badge>

            <!-- 用户头像 -->
            <el-dropdown trigger="hover">
              <div class="user-avatar">
                <img :src="userStore.user?.avatar || defaultAvatar" :alt="$t('user.avatar')" />
                <span class="user-name">{{ userStore.user?.nickname || userStore.user?.username }}</span>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="goToProfile">
                    {{ $t('nav.myProfile') }}
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToMyItems">
                    {{ $t('nav.myItems') }}
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToMyRents">
                    {{ $t('item.transactionType.rent') }}
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToMyRequests">
                    {{ $t('nav.requests') }}
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToMyTransactions">
                    {{ $t('nav.myOrders') }}
                  </el-dropdown-item>
                  <el-dropdown-item @click="goToFavorites">
                    {{ $t('nav.myFavorites') }}
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.isAdmin" @click="goToAdmin">
                    {{ $t('nav.settings') }}
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    {{ $t('common.logout') }}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>

          <!-- 未登录 -->
          <template v-else>
            <el-button type="primary" size="small" class="login-btn" @click="goToLogin">{{ $t('common.login') }}</el-button>
            <el-button size="small" class="register-btn" @click="goToRegister">{{ $t('common.register') }}</el-button>
          </template>
        </div>

        <!-- 移动端菜单按钮 -->
        <el-button
          class="mobile-menu-btn"
          @click="toggleMobileMenu"
          v-show="!showMobileMenu"
        >
          <el-icon><Menu /></el-icon>
        </el-button>
        <el-button
          class="mobile-menu-btn"
          @click="toggleMobileMenu"
          v-show="showMobileMenu"
        >
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- 移动端菜单 -->
    <div class="mobile-menu" v-show="showMobileMenu">
      <ul class="mobile-nav-list">
        <li class="mobile-nav-item">
          <router-link to="/" class="mobile-nav-link" :class="{ active: route.path === '/' }" @click="toggleMobileMenu">{{ $t('nav.home') }}</router-link>
        </li>
        <li class="mobile-nav-item">
          <router-link to="/items" class="mobile-nav-link" :class="{ active: route.path.startsWith('/items') }" @click="toggleMobileMenu">{{ $t('nav.items') }}</router-link>
        </li>
        <li class="mobile-nav-item">
          <router-link to="/rent/list" class="mobile-nav-link" :class="{ active: route.path.startsWith('/rent') }" @click="toggleMobileMenu">{{ $t('item.transactionType.rent') }}</router-link>
        </li>
        <li class="mobile-nav-item">
          <router-link to="/requests" class="mobile-nav-link" :class="{ active: route.path.startsWith('/requests') }" @click="toggleMobileMenu">{{ $t('nav.requests') }}</router-link>
        </li>
        <li class="mobile-nav-item">
          <router-link to="/compare" class="mobile-nav-link" :class="{ active: route.path.startsWith('/compare') }" @click="toggleMobileMenu">{{ $t('nav.compare') }}</router-link>
        </li>
        <li class="mobile-nav-item">
          <a href="#" class="mobile-nav-link" @click="toggleMobileMenu">{{ $t('nav.about') }}</a>
        </li>
        <li class="mobile-nav-item language-mobile">
          <span class="mobile-nav-link" @click="handleLanguageChange(currentLocale === 'zh-CN' ? 'en-US' : 'zh-CN')">
            {{ $t('language.switchLanguage') }}: {{ currentLocale === 'zh-CN' ? '🇺🇸 EN' : '🇨🇳 中文' }}
          </span>
        </li>
        <li v-if="userStore.isLoggedIn" class="mobile-nav-item">
          <a href="#" class="mobile-nav-link" @click="handleLogout">{{ $t('common.logout') }}</a>
        </li>
        <li v-else class="mobile-nav-item">
          <el-button type="primary" size="small" class="mobile-login-btn" @click="handleMobileLogin">{{ $t('common.login') }}</el-button>
        </li>
        <li v-if="!userStore.isLoggedIn" class="mobile-nav-item">
          <el-button size="small" class="mobile-register-btn" @click="handleMobileRegister">{{ $t('common.register') }}</el-button>
        </li>
      </ul>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useUserStore } from '@/store/user';
import { ElMessage } from 'element-plus';
import { Search, Bell, Menu, Close, Eleme } from '@element-plus/icons-vue';
import { setLocale, getLocale } from '@/i18n';

// 国际化
const { t } = useI18n();

// 路由和状态管理
const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

// 当前语言
const currentLocale = computed(() => getLocale());

// 响应式数据
const searchKeyword = ref('');
const showMobileMenu = ref(false);
const unreadCount = ref(3);
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';

// 切换语言
const handleLanguageChange = (lang: string) => {
  setLocale(lang);
  ElMessage.success(t('message.operationSuccess'));
};

// 搜索处理
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({
      path: '/items',
      query: { keyword: searchKeyword.value.trim() }
    });
  } else {
    ElMessage.warning(t('validation.required'));
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
    ElMessage.success(t('auth.logoutSuccess'));
    router.push('/');
  } catch (error) {
    ElMessage.error(t('message.operationFailed'));
  }
};

// 导航函数
const goToPublishItem = () => router.push('/items/create');
const goToPublishRequest = () => router.push('/requests/create');
const goToCreateCompare = () => router.push('/compare/create');
const goToPublishRent = () => router.push('/rent/create');
const goToMyRents = () => router.push('/rent/list');
const goToMessages = () => ElMessage.info(t('message.notFound'));
const goToProfile = () => ElMessage.info(t('message.notFound'));
const goToMyItems = () => router.push('/items');
const goToMyRequests = () => router.push('/requests/my');
const goToMyTransactions = () => ElMessage.info(t('message.notFound'));
const goToFavorites = () => ElMessage.info(t('message.notFound'));
const goToAdmin = () => ElMessage.info(t('message.notFound'));
const goToLogin = () => router.push('/login');
const goToRegister = () => router.push('/register');

const handleMobileLogin = () => {
  toggleMobileMenu();
  setTimeout(() => router.push('/login'), 100);
};

const handleMobileRegister = () => {
  toggleMobileMenu();
  setTimeout(() => router.push('/register'), 100);
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
  padding: 10px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 60px;
  height: auto;
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

/* 响应式布局 */
@media (max-width: 1024px) {
  .header-container {
    padding: 8px 15px;
  }
  
  .search-input {
    max-width: 180px;
  }
  
  .nav-item {
    margin: 0 10px;
  }
  
  .nav-link {
    font-size: 14px;
  }
}

@media (max-width: 768px) {
  .search-input {
    max-width: 150px;
  }
  
  .logo-text {
    font-size: 18px;
  }
}

@media (max-width: 640px) {
  .header-actions {
    gap: 10px;
  }
  
  .search-input {
    width: 150px;
  }
  
  .nav-item {
    margin: 0 5px;
  }
  
  .nav-link {
    font-size: 13px;
  }
}

/* 右侧功能区样式 */
.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 15px;
  white-space: nowrap;
}

.search-container {
  position: relative;
  white-space: nowrap;
}

.search-input {
  width: 200px;
  height: 36px;
  flex-shrink: 0;
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