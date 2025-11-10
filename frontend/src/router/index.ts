import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

// 路由配置
const routes: Array<RouteRecordRaw> = [
  // 公共路由
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: {
      title: '首页',
      requiresAuth: false
    }
  },
  
  // 认证路由
  { 
    path: '/login', 
    name: 'Login', 
    component: () => import('../views/auth/Login.vue'),
    meta: {        
      title: '登录',
      requiresAuth: false
    }
  },
  { 
    path: '/register', 
    name: 'Register', 
    component: () => import('../views/auth/Register.vue'),
    meta: {        
      title: '注册',
      requiresAuth: false
    }
  },
  
  // 用户路由 - 暂时注释，稍后实现
  /*
  { 
    path: '/user/profile', 
    name: 'UserProfile', 
    component: () => import('../views/user/Profile.vue'),
    meta: {
      title: '个人中心',
      requiresAuth: true
    }
  },
  { 
    path: '/user/settings', 
    name: 'UserSettings', 
    component: () => import('../views/user/Settings.vue'),
    meta: {
      title: '账户设置',
      requiresAuth: true
    }
  },
  */
  
  // 商品路由
  {
    path: '/items',
    name: 'ItemList',
    component: () => import('../views/ItemList.vue'),
    meta: {
      title: '商品列表',
      requiresAuth: false
    }
  },
  {
    path: '/items/detail/:id',
    name: 'ItemDetail',
    component: () => import('../views/ItemDetail.vue'),
    meta: {
      title: '商品详情',
      requiresAuth: false
    }
  },
  {
    path: '/items/create',
    name: 'ItemCreate',
    component: () => import('../views/ItemCreate.vue'),
    meta: {
      title: '发布商品',
      requiresAuth: true
    }
  },
  {
    path: '/items/my',
    name: 'MyItems',
    component: () => import('../views/ItemList.vue'),
    meta: {
      title: '我的商品',
      requiresAuth: true
    }
  },
  
  // 求购路由
  {
    path: '/requests',
    name: 'RequestList',
    component: () => import('../views/RequestItemList.vue'),
    meta: {
      title: '求购列表',
      requiresAuth: false
    }
  },
  {
    path: '/requests/detail/:id',
    name: 'RequestDetail',
    component: () => import('../views/RequestItemDetail.vue'),
    meta: {
      title: '求购详情',
      requiresAuth: false
    }
  },
  {
    path: '/requests/create',
    name: 'RequestCreate',
    component: () => import('../views/RequestItemCreate.vue'),
    meta: {
      title: '发布求购',
      requiresAuth: true
    }
  },
  {
    path: '/requests/my',
    name: 'MyRequests',
    component: () => import('../views/RequestItemList.vue'),
    meta: {
      title: '我的求购',
      requiresAuth: true
    }
  },
  
  // 比价路由
  {
    path: '/compare',
    name: 'CompareList',
    component: () => import('../views/CompareList.vue'),
    meta: {
      title: '比价任务',
      requiresAuth: true
    }
  },
  {
    path: '/compare/create',
    name: 'CompareCreate',
    component: () => import('../views/CompareCreate.vue'),
    meta: {
      title: '创建比价',
      requiresAuth: true
    }
  },
  {
    path: '/compare/detail/:id',
    name: 'CompareDetail',
    component: () => import('../views/CompareDetail.vue'),
    meta: {
      title: '比价详情',
      requiresAuth: true
    }
  },

  
  // 404路由
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: {
      template: '<div style="text-align: center; padding: 100px 20px;"><h1>404</h1><p>页面不存在</p><router-link to="/">返回首页</router-link></div>'
    },
    meta: {
      title: '页面不存在',
      requiresAuth: false,
      hideInMenu: true
    }
  }
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// 路由守卫
router.beforeEach((to, _from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 校园二手交易平台`;
  } else {
    document.title = '校园二手交易平台';
  }

  // 暂时禁用登录检查，让用户能够访问所有功能
  // 后续需要实现完整的登录功能
  /*
  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    // 从localStorage中检查登录状态
    const isLoggedIn = localStorage.getItem('token') !== null;
    if (!isLoggedIn) {
      // 显示提示
      setTimeout(() => {
        ElMessage.warning('请先登录后再使用该功能');
      }, 100);
      // 暂时直接通过，后续跳转到登录页
      // next({ name: 'Login', query: { redirect: to.fullPath } });
      // return;
    }
  }
  */

  // 继续路由
  next();
});

export default router;