import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/',
    name: 'Layout',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../pages/Home.vue')
      },
      {
        path: 'post/:slug',
        name: 'PostDetail',
        component: () => import('../pages/PostDetail.vue')
      },
      {
        path: 'category/:slug',
        name: 'Category',
        component: () => import('../pages/Category.vue')
      },
      {
        path: 'tag/:slug',
        name: 'Tag',
        component: () => import('../pages/Tag.vue')
      },
      {
        path: 'archives',
        name: 'Archives',
        component: () => import('../pages/Archives.vue')
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('../pages/About.vue')
      },
      {
        path: 'test-tech',
        name: 'TestTech',
        component: () => import('../pages/TestTech.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../pages/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../pages/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/admin',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('../pages/admin/Dashboard.vue')
      },
      {
        path: 'posts',
        name: 'AdminPosts',
        component: () => import('../pages/admin/Posts.vue')
      },
      {
        path: 'posts/new',
        name: 'AdminPostNew',
        component: () => import('../pages/admin/PostEdit.vue')
      },
      {
        path: 'posts/edit/:id',
        name: 'AdminPostEdit',
        component: () => import('../pages/admin/PostEdit.vue')
      },
      {
        path: 'logs',
        name: 'AdminLogs',
        component: () => import('../pages/admin/Logs.vue')
      },
      {
        path: 'api-docs',
        name: 'AdminApiDocs',
        component: () => import('../pages/admin/ApiDocs.vue')
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('../pages/admin/Users.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 需要登录的页面
  if (to.meta.requiresAuth && !userStore.token) {
    next('/login')
    return
  }
  
  // 需要管理员权限
  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next('/')
    return
  }
  
  // 游客页面（已登录用户不能访问）
  if (to.meta.guest && userStore.token) {
    next('/')
    return
  }
  
  next()
})

export default router
