<template>
  <div class="category-page">
    <h2>分类：{{ categoryName }}</h2>
    <p v-if="categoryDesc" class="desc">{{ categoryDesc }}</p>
    
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="posts.length === 0" class="empty">
      <el-empty description="该分类下暂无文章" />
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
import { getPosts, getCategories } from '../api/posts'
import { ElMessage } from 'element-plus'

const route = useRoute()

const posts = ref([])
const categoryName = ref('')
const categoryDesc = ref('')
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchCategory = async () => {
  try {
    const res = await getCategories()
    const category = res.data.find(c => c.slug === route.params.slug)
    if (category) {
      categoryName.value = category.name
      categoryDesc.value = category.description
      return category.id
    }
  } catch (error) {
    console.error('获取分类失败', error)
  }
  return null
}

const fetchPosts = async () => {
  const categoryId = await fetchCategory()
  if (!categoryId) return
  
  loading.value = true
  try {
    const res = await getPosts({
      page: currentPage.value,
      per_page: pageSize.value,
      category_id: categoryId
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
.category-page {
  padding: 20px 0;
}

.desc {
  color: #666;
  margin-bottom: 20px;
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
