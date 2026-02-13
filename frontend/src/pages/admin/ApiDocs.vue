<template>
  <div class="api-docs-page">
    <h2>博客接口文档</h2>
    
    <el-card v-for="(module, key) in apiDocs" :key="key" class="module-card">
      <template #header>
        <div class="module-header">
          <h3>{{ module.name }}</h3>
          <p class="module-desc">{{ module.description }}</p>
        </div>
      </template>
      
      <el-collapse>
        <el-collapse-item 
          v-for="(endpoint, index) in module.endpoints" 
          :key="index"
          :title="`${endpoint.method} ${endpoint.path} - ${endpoint.name}`"
        >
          <div class="endpoint-detail">
            <p><strong>描述：</strong>{{ endpoint.description }}</p>
            <p><strong>权限：</strong>
              <el-tag :type="getPermissionType(endpoint.permission)" size="small">
                {{ endpoint.permission }}
              </el-tag>
            </p>
            
            <div v-if="Object.keys(endpoint.params).length > 0" class="params-section">
              <h4>请求参数</h4>
              <el-table :data="formatParams(endpoint.params)" border size="small">
                <el-table-column prop="name" label="参数名" width="150" />
                <el-table-column prop="description" label="说明" />
              </el-table>
            </div>
            
            <div class="response-section">
              <h4>响应数据</h4>
              <pre>{{ JSON.stringify(endpoint.response, null, 2) }}</pre>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getApiDocs } from '../../api/admin'
import { ElMessage } from 'element-plus'

const apiDocs = ref({})

const fetchApiDocs = async () => {
  try {
    const res = await getApiDocs()
    apiDocs.value = res.data
  } catch (error) {
    ElMessage.error('获取接口文档失败')
  }
}

const formatParams = (params) => {
  return Object.keys(params).map(key => ({
    name: key,
    description: params[key]
  }))
}

const getPermissionType = (permission) => {
  const types = {
    '公开': 'success',
    '登录用户': 'primary',
    '管理员': 'warning',
    '管理员/评论作者': 'danger'
  }
  return types[permission] || 'info'
}

onMounted(() => {
  fetchApiDocs()
})
</script>

<style scoped>
.api-docs-page {
  padding: 20px;
}

.module-card {
  margin-bottom: 20px;
}

.module-header h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.module-desc {
  color: #909399;
  margin: 0;
}

.endpoint-detail {
  padding: 10px;
}

.endpoint-detail h4 {
  margin: 15px 0 10px 0;
  color: #606266;
  border-left: 4px solid #409eff;
  padding-left: 10px;
}

.params-section,
.response-section {
  margin-top: 15px;
}

pre {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.6;
}
</style>
