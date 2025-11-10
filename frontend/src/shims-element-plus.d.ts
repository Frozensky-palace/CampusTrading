// Element Plus 类型声明
import { DefineComponent } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';

// Element Plus 组件类型声明
declare module '@element-plus/components/*' {
  const component: DefineComponent<any, any, any>;
  export default component;
}

// Element Plus 图标类型声明
declare module '@element-plus/icons-vue' {
  const component: DefineComponent<any, any, any>;
  export default component;
}

// 全局Element接口扩展以支持focus和blur方法
declare global {
  interface Element {
    focus(options?: FocusOptions): void;
    blur(): void;
  }
}

// Vue组件自定义属性扩展
declare module 'vue' {
  interface ComponentCustomProperties {
    $message: typeof ElMessage;
    $confirm: typeof ElMessageBox.confirm;
    $alert: typeof ElMessageBox.alert;
    $prompt: typeof ElMessageBox.prompt;
  }
}

// Vue运行时核心扩展
declare module '@vue/runtime-core' {
  export interface ComponentCustomProperties {
    $message: typeof ElMessage;
    $confirm: typeof ElMessageBox.confirm;
    $alert: typeof ElMessageBox.alert;
    $prompt: typeof ElMessageBox.prompt;
  }
}