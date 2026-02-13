<template>
  <div class="dashboard-page">
    <h2>控制台</h2>
    
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #409eff;">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_posts }}</div>
            <div class="stat-label">总文章数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #67c23a;">
            <el-icon><View /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.published_posts }}</div>
            <div class="stat-label">已发布</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #e6a23c;">
            <el-icon><Folder /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ categories.length }}</div>
            <div class="stat-label">分类数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #909399;">
            <el-icon><CollectionTag /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ tags.length }}</div>
            <div class="stat-label">标签数</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="recent-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>最近文章</span>
          </template>
          <el-table :data="recentPosts" style="width: 100%">
            <el-table-column prop="title" label="标题" show-overflow-tooltip />
            <el-table-column prop="published_at" label="发布时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.published_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/admin/posts/new')">
              <el-icon><Plus /></el-icon>
              新建文章
            </el-button>
            <el-button @click="$router.push('/admin/posts')">
              <el-icon><Document /></el-icon>
              管理文章
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts, getCategories, getTags } from '../../api/posts'

const stats = ref({
  total_posts: 0,
  published_posts: 0
})
const recentPosts = ref([])
const categories = ref([])
const tags = ref([])

const fetchData = async () => {
  try {
    const [postsRes, catRes, tagRes] = await Promise.all([
      getPosts({ per_page: 5 }),
      getCategories(),
      getTags()
    ])
    
    recentPosts.value = postsRes.data.items
    stats.value.total_posts = postsRes.data.total
    stats.value.published_posts = postsRes.data.items.filter(p => p.is_published).length
    categories.value = catRes.data
    tags.value = tagRes.data
  } catch (error) {
    console.error('获取数据失败', error)
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.dashboard-page {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 10px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
  margin-right: 15px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  color: #909399;
  font-size: 14px;
  margin-top: 5px;
}

.quick-actions {
  display: flex;
  gap: 15px;
}
</style>
