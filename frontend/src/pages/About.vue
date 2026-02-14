<template>
  <div class="about-page">
    <el-card class="about-card">
      <template #header>
        <h2>关于本站</h2>
      </template>
      
      <div class="about-content">
        <h3>Flask + Vue 博客系统</h3>
        <p>这是一个基于 Python Flask 和 Vue 3 开发的前后端分离个人博客系统。</p>
        
        <h4>技术栈</h4>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="后端框架">Flask 3.0</el-descriptions-item>
          <el-descriptions-item label="数据库">MySQL + SQLAlchemy</el-descriptions-item>
          <el-descriptions-item label="认证">JWT (Flask-JWT-Extended)</el-descriptions-item>
          <el-descriptions-item label="前端框架">Vue 3 + Vite</el-descriptions-item>
          <el-descriptions-item label="UI组件">Element Plus</el-descriptions-item>
          <el-descriptions-item label="Markdown编辑器">mavon-editor</el-descriptions-item>
        </el-descriptions>
        
        <h4>功能特性</h4>
        <ul>
          <li>用户注册、登录、JWT认证</li>
          <li>文章发布、编辑、删除，支持Markdown</li>
          <li>文章分类和标签管理</li>
          <li>评论系统</li>
          <li>文章搜索功能</li>
          <li>响应式设计</li>
        </ul>
      </div>
    </el-card>

    <el-card class="author-card" style="margin-top: 16px;">
      <template #header>
        <h2>作者介绍</h2>
      </template>
      <div class="author">
        <img class="avatar" :src="avatarUrl" alt="avatar" />
        <div class="meta">
          <div class="name">作者：{{ authorName }}</div>
          <div class="bio">{{ authorBio }}</div>
          <div class="links">
            <el-link type="primary" :href="githubUrl" target="_blank">
              <el-icon><Link /></el-icon>
              <span style="margin-left:4px;">GitHub 仓库</span>
            </el-link>
          </div>
        </div>
      </div>
      <el-divider />
      <div class="intro">
        <p>本博客用于记录开发笔记、技术文章与项目实践，涵盖后端、前端、数据库与运维等内容，欢迎交流与反馈。</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const authorName = 'as1285'
const authorBio = '热爱开源与分享，关注后端架构、前端工程化与 DevOps 实践。'
const githubUrl = 'https://github.com/as1285/boke'
const avatarUrl = '/default_avatar.png'
</script>

<style scoped>
.about-page {
  padding: 20px 0;
}

.about-card :deep(.el-card__header),
.author-card :deep(.el-card__header) {
  padding: 12px 16px;
}

.about-content h3 {
  color: #409eff;
  margin-bottom: 15px;
}

.about-content h4 {
  margin: 20px 0 10px 0;
  color: #303133;
}

.about-content p {
  line-height: 1.8;
  color: #606266;
  margin-bottom: 15px;
}

.about-content ul {
  padding-left: 20px;
  color: #606266;
}

.about-content li {
  margin-bottom: 8px;
  line-height: 1.6;
}

.author {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #e4e7ed;
}

.meta .name {
  font-weight: 600;
  margin-bottom: 6px;
}

.meta .bio {
  color: #606266;
  margin-bottom: 10px;
}
</style>
