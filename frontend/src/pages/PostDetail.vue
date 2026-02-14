<template>
  <div class="post-detail-page">
    <div v-if="loading" class="loading">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!post" class="empty">
      <el-empty description="文章不存在" />
    </div>
    
    <div v-else class="post-content">
      <el-card class="post-header">
        <h1 class="post-title">{{ post.title }}</h1>
        <div class="post-meta">
          <span><el-icon><Calendar /></el-icon> {{ formatDate(post.published_at) }}</span>
          <span><el-icon><User /></el-icon> {{ post.author?.username }}</span>
          <span v-if="post.category"><el-icon><Folder /></el-icon> {{ post.category.name }}</span>
          <span><el-icon><View /></el-icon> {{ post.view_count }} 阅读</span>
        </div>
        <div class="post-tags" v-if="post.tags && post.tags.length > 0">
          <el-tag
            v-for="tag in post.tags"
            :key="tag.id"
            size="small"
            effect="plain"
            @click="$router.push(`/tag/${tag.slug}`)"
          >
            {{ tag.name }}
          </el-tag>
        </div>
      </el-card>
      
      <el-card class="post-body">
        <div class="markdown-body" v-html="post.content_html"></div>
      </el-card>
      
      <el-card class="author-card">
        <template #header>
          <h3>关于作者</h3>
        </template>
        <div class="author">
          <img class="avatar" src="/default_avatar.png" alt="avatar" />
          <div class="meta">
            <div class="name">{{ post.author?.username || '作者' }}</div>
            <div class="bio">分享开发实践与学习笔记，欢迎交流。</div>
            <div class="links">
              <el-link type="primary" href="https://github.com/as1285/boke" target="_blank">
                <el-icon><Link /></el-icon>
                <span style="margin-left:4px;">GitHub 仓库</span>
              </el-link>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- 评论区 -->
      <el-card class="comments-section">
        <template #header>
          <h3>评论 ({{ comments.length }})</h3>
        </template>
        
        <!-- 发表评论 -->
        <div v-if="userStore.isLoggedIn" class="comment-form">
          <el-input
            v-model="newComment"
            type="textarea"
            :rows="3"
            placeholder="发表你的评论..."
          />
          <el-button type="primary" @click="submitComment" :loading="submitting">
            发表评论
          </el-button>
        </div>
        <div v-else class="login-tip">
          <el-button type="primary" @click="$router.push('/login')">登录后发表评论</el-button>
        </div>
        
        <!-- 评论列表 -->
        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="username">{{ comment.author?.username }}</span>
              <span class="time">{{ formatDate(comment.created_at) }}</span>
            </div>
            <div class="comment-content" v-html="comment.content_html"></div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { getPost, getComments, createComment } from '../api/posts'
import { ElMessage } from 'element-plus'

const route = useRoute()
const userStore = useUserStore()

const post = ref(null)
const comments = ref([])
const loading = ref(false)
const newComment = ref('')
const submitting = ref(false)

const fetchPost = async () => {
  loading.value = true
  try {
    const res = await getPost(route.params.slug)
    post.value = res.data
    fetchComments(res.data.id)
  } catch (error) {
    ElMessage.error('获取文章失败')
  } finally {
    loading.value = false
  }
}

const fetchComments = async (postId) => {
  try {
    const res = await getComments(postId)
    comments.value = res.data.items
  } catch (error) {
    console.error('获取评论失败', error)
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  
  submitting.value = true
  try {
    await createComment(post.value.id, { content: newComment.value })
    ElMessage.success('评论成功')
    newComment.value = ''
    fetchComments(post.value.id)
  } catch (error) {
    // 错误已在请求拦截器中处理
  } finally {
    submitting.value = false
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchPost()
})
</script>

<style scoped>
.post-detail-page {
  padding: 20px 0;
}

.post-header {
  margin-bottom: 20px;
}

.post-title {
  margin: 0 0 15px 0;
  font-size: 28px;
  color: #303133;
}

.post-meta {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 14px;
  margin-bottom: 15px;
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.post-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.post-body {
  margin-bottom: 20px;
}

.markdown-body {
  line-height: 1.8;
  font-size: 16px;
}

.author-card{
  margin-bottom: 20px;
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
  margin-bottom:6px;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
  margin-top: 24px;
  margin-bottom: 16px;
}

.markdown-body :deep(p) {
  margin-bottom: 16px;
}

.markdown-body :deep(pre) {
  background-color: #f6f8fa;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
}

.markdown-body :deep(code) {
  background-color: #f6f8fa;
  padding: 2px 6px;
  border-radius: 3px;
}

.comments-section {
  margin-top: 20px;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-form .el-button {
  margin-top: 10px;
}

.login-tip {
  text-align: center;
  padding: 20px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.comment-item {
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.comment-header .username {
  font-weight: bold;
  color: #409eff;
}

.comment-header .time {
  color: #909399;
  font-size: 12px;
}

.comment-content {
  color: #606266;
  line-height: 1.6;
}

.loading {
  padding: 40px;
}
</style>
