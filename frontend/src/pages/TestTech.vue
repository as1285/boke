<template>
  <div class="test-tech-page">
    <div class="page-header">
      <h1>🧪 测试技术资源</h1>
      <p class="subtitle">汇总主流测试技术网站，助力测试工程师成长</p>
    </div>
    
    <!-- 分类筛选 -->
    <div class="category-filter">
      <el-radio-group v-model="selectedCategory" @change="filterByCategory">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button 
          v-for="cat in categories" 
          :key="cat" 
          :label="cat"
        >
          {{ cat }}
        </el-radio-button>
      </el-radio-group>
    </div>
    
    <!-- 推荐资源 -->
    <div v-if="!selectedCategory" class="recommended-section">
      <h2>⭐ 推荐资源</h2>
      <el-row :gutter="20">
        <el-col 
          v-for="resource in recommendedResources" 
          :key="resource.id" 
          :xs="24" :sm="12" :md="8" :lg="6"
        >
          <el-card class="resource-card recommended" shadow="hover">
            <div class="card-header">
              <img v-if="resource.icon" :src="resource.icon" class="resource-icon" @error="handleIconError">
              <div v-else class="resource-icon-placeholder">{{ resource.name[0] }}</div>
              <el-tag v-if="resource.is_recommended" type="danger" size="small" effect="dark">推荐</el-tag>
            </div>
            <h3 class="resource-name">{{ resource.name }}</h3>
            <p class="resource-desc">{{ resource.description }}</p>
            <div class="card-footer">
              <el-tag size="small" type="info">{{ resource.category }}</el-tag>
              <el-button type="primary" size="small" @click="openUrl(resource.url)">
                访问 <el-icon><Link /></el-icon>
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 分类展示 -->
    <div v-for="group in filteredResources" :key="group.category" class="category-section">
      <h2>
        {{ getCategoryIcon(group.category) }} {{ group.category }}
        <span class="count">({{ group.resources.length }})</span>
      </h2>
      <el-row :gutter="20">
        <el-col 
          v-for="resource in group.resources" 
          :key="resource.id" 
          :xs="24" :sm="12" :md="8" :lg="6"
        >
          <el-card class="resource-card" shadow="hover">
            <div class="card-header">
              <img v-if="resource.icon" :src="resource.icon" class="resource-icon" @error="handleIconError">
              <div v-else class="resource-icon-placeholder">{{ resource.name[0] }}</div>
              <el-tag v-if="resource.is_recommended" type="danger" size="small">推荐</el-tag>
            </div>
            <h3 class="resource-name">{{ resource.name }}</h3>
            <p class="resource-desc">{{ resource.description }}</p>
            <div class="card-footer">
              <el-tag size="small" type="info">{{ resource.category }}</el-tag>
              <el-button type="primary" size="small" @click="openUrl(resource.url)">
                访问 <el-icon><Link /></el-icon>
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getTestTechResources, getTechCategories } from '../api/tech'
import { ElMessage } from 'element-plus'

const resources = ref([])
const categories = ref([])
const selectedCategory = ref('')
const loading = ref(false)

// 获取资源数据
const fetchResources = async () => {
  loading.value = true
  try {
    const res = await getTestTechResources()
    resources.value = res.data
  } catch (error) {
    ElMessage.error('获取资源失败')
  } finally {
    loading.value = false
  }
}

// 获取分类
const fetchCategories = async () => {
  try {
    const res = await getTechCategories()
    categories.value = res.data
  } catch (error) {
    console.error('获取分类失败', error)
  }
}

// 推荐资源
const recommendedResources = computed(() => {
  const allResources = resources.value.flatMap(g => g.resources)
  return allResources.filter(r => r.is_recommended).slice(0, 8)
})

// 过滤后的资源
const filteredResources = computed(() => {
  if (!selectedCategory.value) {
    return resources.value
  }
  return resources.value.filter(g => g.category === selectedCategory.value)
})

// 按分类筛选
const filterByCategory = () => {
  // 筛选逻辑在computed中处理
}

// 打开链接
const openUrl = (url) => {
  window.open(url, '_blank')
}

// 图标加载失败处理
const handleIconError = (e) => {
  e.target.style.display = 'none'
}

// 获取分类图标
const getCategoryIcon = (category) => {
  const icons = {
    '自动化测试框架': '🤖',
    'API测试工具': '🔌',
    '性能测试工具': '⚡',
    '测试管理工具': '📋',
    '持续集成': '🔄',
    '代码质量': '✨',
    '安全测试': '🔒',
    '移动测试': '📱',
    '测试社区': '👥'
  }
  return icons[category] || '📦'
}

onMounted(() => {
  fetchResources()
  fetchCategories()
})
</script>

<style scoped>
.test-tech-page {
  padding: 40px 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 36px;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #909399;
  font-size: 16px;
}

.category-filter {
  text-align: center;
  margin-bottom: 40px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.recommended-section {
  margin-bottom: 50px;
}

.category-section {
  margin-bottom: 40px;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #ebeef5;
}

.count {
  font-size: 14px;
  color: #909399;
  font-weight: normal;
}

.resource-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.resource-card:hover {
  transform: translateY(-5px);
}

.resource-card.recommended {
  border: 2px solid #f56c6c;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.resource-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: contain;
}

.resource-icon-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
}

.resource-name {
  font-size: 18px;
  margin: 0 0 10px 0;
  color: #303133;
}

.resource-desc {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 28px;
  }
  
  .category-filter {
    overflow-x: auto;
    white-space: nowrap;
  }
}
</style>
