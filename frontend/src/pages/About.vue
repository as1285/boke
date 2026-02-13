<template>
  <div class="about-page">
    <el-card>
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
  </div>
</template>

<style scoped>
.about-page {
  padding: 20px 0;
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
</style>
