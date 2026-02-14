<template>
  <el-container class="main-layout">
    <el-header class="header">
      <div class="header-content">
        <div class="logo" @click="$router.push('/')">
          <el-icon><Document /></el-icon>
          <span>Flask博客</span>
        </div>
        
        <el-menu
          :default-active="activeMenu"
          class="nav-menu"
          mode="horizontal"
          router
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/archives">归档</el-menu-item>
          <el-menu-item index="/test-tech">🧪 测试技术</el-menu-item>
          <el-menu-item index="/about">关于</el-menu-item>
        </el-menu>
        
        <div class="header-right">
          <template v-if="userStore.isLoggedIn">
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                {{ userStore.userInfo?.username }}
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-if="userStore.isAdmin" command="admin">后台管理</el-dropdown-item>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button type="primary" @click="$router.push('/login')">登录</el-button>
            <el-button @click="$router.push('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>
    
    <el-main class="main-content">
      <router-view />
    </el-main>
    
    <el-footer class="footer">
      <p>&copy; 2026 Flask博客系统 · 基于 Flask + Vue3 开发 · 
        <a class="github-link" href="https://github.com/as1285/boke" target="_blank" rel="noopener">GitHub</a>
      </p>
    </el-footer>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const handleCommand = (command) => {
  if (command === 'admin') {
    router.push('/admin')
  } else if (command === 'logout') {
    userStore.logout()
    ElMessage.success('退出成功')
    router.push('/')
  }
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
}

.header {
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  cursor: pointer;
  margin-right: 40px;
}

.logo .el-icon {
  font-size: 24px;
  margin-right: 8px;
}

.nav-menu {
  flex: 1;
  border-bottom: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 20px;
}

.footer {
  text-align: center;
  color: #666;
  background: #f5f5f5;
}

.github-link {
  color: #409eff;
  text-decoration: none;
  margin-left: 6px;
}

.github-link:hover {
  text-decoration: underline;
}
</style>
