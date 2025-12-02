import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// 导入 Element Plus 组件库
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 导入 Element Plus 图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 导入状态管理
import pinia from './store'

// 导入路由
import router from './router'

// 导入国际化
import i18n from './i18n'

// 创建应用实例
const app = createApp(App)

// 注册 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用插件
app.use(ElementPlus)
app.use(pinia)
app.use(router)
app.use(i18n)

// 挂载应用
app.mount('#app')
