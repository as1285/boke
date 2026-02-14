<template>
  <el-card class="author-widget" shadow="always">
    <template #header>
      <div class="header">
        <span>作者</span>
      </div>
    </template>
    <div class="author">
      <img class="avatar" :src="avatarUrl" alt="avatar" />
      <div class="meta">
        <div class="name">{{ authorName }}</div>
        <div class="bio">{{ authorBio }}</div>
      </div>
    </div>
    <el-divider />
    <div class="links">
      <el-link type="primary" :href="githubUrl" target="_blank">
        <el-icon><Link /></el-icon>
        <span style="margin-left:4px;">GitHub 仓库</span>
      </el-link>
    </div>
  </el-card>
  </template>

<script setup>
const authorName = 'as1285'
const authorBio = '分享后端、前端与 DevOps 实践。'
const githubUrl = 'https://github.com/as1285/boke'
const avatarUrl = '/default_avatar.png'
</script>

<style scoped>
.author-widget :deep(.el-card__header){
  padding: 12px 16px;
}
.author{
  display:flex;
  align-items:center;
  gap:12px;
}
.avatar{
  width:56px;
  height:56px;
  border-radius:50%;
  object-fit:cover;
  border:1px solid #e4e7ed;
}
.name{
  font-weight:600;
  margin-bottom:4px;
}
.bio{
  color:#606266;
  font-size:13px;
}
.links{
  display:flex;
  justify-content:flex-start;
}
</style>

