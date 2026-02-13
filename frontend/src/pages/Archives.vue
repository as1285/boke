<template>
  <div class="archives-page">
    <h2>文章归档</h2>
    
    <div v-if="loading" class="loading">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="archives.length === 0" class="empty">
      <el-empty description="暂无文章" />
    </div>
    
    <div v-else class="archives-list">
      <div v-for="group in archives" :key="group.month" class="archive-group">
        <h3 class="archive-month">{{ group.month }}</h3>
        <el-timeline>
          <el-timeline-item
            v-for="post in group.posts"
            :key="post.id"
            :timestamp="formatDate(post.published_at)"
          >
            <el-link @click="$router.push(`/post/${post.slug}`)">
              {{ post.title }}
            </el-link>
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts } from '../api/posts'
import { ElMessage } from 'element-plus'

const archives = ref([])
const loading = ref(false)

const fetchArchives = async () => {
  loading.value = true
  try {
    const res = await getPosts({ per_page: 1000 })
    const posts = res.data.items
    
    // 按月份分组
    const groups = {}
    posts.forEach(post => {
      const date = new Date(post.published_at)
      const month = `${date.getFullYear()}年${date.getMonth() + 1}月`
      
      if (!groups[month]) {
        groups[month] = []
      }
      groups[month].push(post)
    })
    
    // 转换为数组
    archives.value = Object.keys(groups).map(month => ({
      month,
      posts: groups[month]
    }))
  } catch (error) {
    ElMessage.error('获取归档失败')
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
}

onMounted(() => {
  fetchArchives()
})
</script>

<style scoped>
.archives-page {
  padding: 20px 0;
}

.archives-list {
  margin-top: 20px;
}

.archive-group {
  margin-bottom: 30px;
}

.archive-month {
  color: #409eff;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #ebeef5;
}
</style>
