<template>
  <div class="tag-page">
    <h2>标签：{{ tagName }}</h2>
    
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="posts.length === 0" class="empty">
      <el-empty description="该标签下暂无文章" />
    </div>
    
    <div v-else class="post-list">
      <el-card
        v-for="post in posts"
        :key="post.id"
        class="post-card"
        shadow="hover"
        @click="$router.push(`/post/${post.slug}`)"
      >
        <h3>{{ post.title }}</h3>
        <p class="summary">{{ post.summary || '暂无摘要' }}</p>
        <div class="meta">
          <span>{{ formatDate(post.published_at) }}</span>
          <span>{{ post.view_count }} 阅读</span>
        </div>
      </el-card>
    </div>
    
    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="fetchPosts"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPosts, getTags } from '../api/posts'
import { ElMessage } from 'element-plus'

const route = useRoute()

const posts = ref([])
const tagName = ref('')
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchTag = async () => {
  try {
    const res = await getTags()
    const tag = res.data.find(t => t.slug === route.params.slug)
    if (tag) {
      tagName.value = tag.name
      return tag.id
    }
  } catch (error) {
    console.error('获取标签失败', error)
  }
  return null
}

const fetchPosts = async () => {
  const tagId = await fetchTag()
  if (!tagId) return
  
  loading.value = true
  try {
    const res = await getPosts({
      page: currentPage.value,
      per_page: pageSize.value,
      tag_id: tagId
    })
    posts.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取文章失败')
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.tag-page {
  padding: 20px 0;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.post-card {
  cursor: pointer;
}

.post-card h3 {
  margin: 0 0 10px 0;
}

.summary {
  color: #666;
  margin-bottom: 10px;
}

.meta {
  color: #999;
  font-size: 12px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
