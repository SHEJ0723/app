import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './assets/theme.css'

// 创建应用实例
const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用 Element Plus，并配置全局选项
app.use(ElementPlus, {
  // 配置全局选项
  experimentalFeatures: {
    // 启用新版本的 API
    vueNext: true
  }
})

// 注册路由
app.use(router)

// 挂载应用
app.mount('#app') 