<template>
  <div class="home-page">
    <div class="content-wrap">
      <div class="main-col">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索文章..."
        clearable
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">
            <el-icon><Search /></el-icon>
          </el-button>
        </template>
      </el-input>
    </div>
    
    <!-- 文章列表 -->
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="posts.length === 0" class="empty">
      <el-empty description="暂无文章" />
    </div>
    
    <div v-else class="post-list">
      <el-card
        v-for="post in posts"
        :key="post.id"
        class="post-card"
        shadow="hover"
        @click="goToPost(post.slug)"
      >
        <div class="post-header">
          <h3 class="post-title">{{ post.title }}</h3>
          <div class="post-meta">
            <span><el-icon><Calendar /></el-icon> {{ formatDate(post.published_at) }}</span>
            <span><el-icon><User /></el-icon> {{ post.author?.username }}</span>
            <span v-if="post.category"><el-icon><Folder /></el-icon> {{ post.category.name }}</span>
            <span><el-icon><View /></el-icon> {{ post.view_count }} 阅读</span>
          </div>
        </div>
        
        <p class="post-summary">{{ post.summary || '暂无摘要' }}</p>
        
        <div class="post-tags" v-if="post.tags && post.tags.length > 0">
          <el-tag
            v-for="tag in post.tags"
            :key="tag.id"
            size="small"
            effect="plain"
            @click.stop="goToTag(tag.slug)"
          >
            {{ tag.name }}
          </el-tag>
        </div>
      </el-card>
    </div>
    
    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
      </div>
      <aside class="side-col">
        <AuthorWidget />
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getPosts } from '../api/posts'
import { ElMessage } from 'element-plus'
import AuthorWidget from '../components/AuthorWidget.vue'

const router = useRouter()
const route = useRoute()

const posts = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchKeyword = ref('')

const fetchPosts = async () => {
  loading.value = true
  try {
    const res = await getPosts({
      page: currentPage.value,
      per_page: pageSize.value,
      keyword: searchKeyword.value || undefined
    })
    posts.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取文章列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchPosts()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchPosts()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchPosts()
}

const goToPost = (slug) => {
  router.push(`/post/${slug}`)
}

const goToTag = (slug) => {
  router.push(`/tag/${slug}`)
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchPosts()
})

// 监听路由变化
watch(() => route.query.keyword, (newVal) => {
  if (newVal) {
    searchKeyword.value = newVal
    fetchPosts()
  }
})
</script>

<style scoped>
.home-page {
  padding: 20px 0;
}

.content-wrap{
  display:flex;
  gap: 20px;
}

.main-col{
  flex: 1;
  min-width: 0;
}

.side-col{
  width: 300px;
}

.search-bar {
  max-width: 600px;
  margin: 0 0 30px 0;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.post-card:hover {
  transform: translateY(-2px);
}

.post-header {
  margin-bottom: 15px;
}

.post-title {
  margin: 0 0 10px 0;
  font-size: 20px;
  color: #303133;
}

.post-meta {
  display: flex;
  gap: 15px;
  color: #909399;
  font-size: 14px;
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.post-summary {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 15px;
}

.post-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

.loading {
  padding: 40px;
}

.empty {
  padding: 60px 0;
}
</style>
