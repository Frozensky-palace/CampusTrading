import { createPinia } from 'pinia';
import { useUserStore } from './user';

// 创建pinia实例
const pinia = createPinia();

// 导出store实例和所有的store模块
export { pinia, useUserStore };

export default pinia;