import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import {
  Document,
  ArrowDown,
  Search,
  Calendar,
  User,
  Folder,
  View,
  Link,
  Plus,
  CollectionTag,
  Setting,
  Odometer,
  List,
  Collection,
  UserFilled,
  Back
} from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// 按需注册使用到的图标
const icons = {
  Document,
  ArrowDown,
  Search,
  Calendar,
  User,
  Folder,
  View,
  Link,
  Plus,
  CollectionTag,
  Setting,
  Odometer,
  List,
  Collection,
  UserFilled,
  Back
}
Object.entries(icons).forEach(([name, comp]) => app.component(name, comp))

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
