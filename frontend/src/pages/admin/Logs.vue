<template>
  <div class="logs-page">
    <h2>API调用日志</h2>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.total_requests || 0 }}</div>
          <div class="stat-label">总请求数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.today_requests || 0 }}</div>
          <div class="stat-label">今日请求</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ (stats.avg_response_time || 0).toFixed(4) }}s</div>
          <div class="stat-label">平均响应时间</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ logs.length }}</div>
          <div class="stat-label">当前页记录</div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="HTTP方法">
          <el-select v-model="filterForm.method" placeholder="全部" clearable style="width: 120px">
            <el-option label="GET" value="GET"></el-option>
            <el-option label="POST" value="POST"></el-option>
            <el-option label="PUT" value="PUT"></el-option>
            <el-option label="DELETE" value="DELETE"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态码">
          <el-select v-model="filterForm.status_code" placeholder="全部" clearable style="width: 140px">
            <el-option label="200 成功" :value="200"></el-option>
            <el-option label="201 创建" :value="201"></el-option>
            <el-option label="400 错误" :value="400"></el-option>
            <el-option label="401 未授权" :value="401"></el-option>
            <el-option label="403 禁止" :value="403"></el-option>
            <el-option label="404 不存在" :value="404"></el-option>
            <el-option label="500 错误" :value="500"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchLogs">筛选</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 日志表格 -->
    <el-card>
      <el-table :data="logs" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="method" label="方法" width="80">
          <template #default="{ row }">
            <el-tag :type="getMethodType(row.method)" size="small">
              {{ row.method }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="path" label="路径" show-overflow-tooltip />
        <el-table-column prop="status_code" label="状态码" width="90">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status_code)" size="small">
              {{ row.status_code }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="response_time" label="响应时间" width="100">
          <template #default="{ row }">
            {{ row.response_time }}s
          </template>
        </el-table-column>
        <el-table-column prop="ip_address" label="IP地址" width="130" />
        <el-table-column prop="username" label="用户" width="100">
          <template #default="{ row }">
            {{ row.username || '匿名' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button size="small" @click="showDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchLogs"
        />
      </div>
    </el-card>
    
    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="日志详情" width="700px">
      <el-descriptions :column="2" border v-if="currentLog">
        <el-descriptions-item label="ID">{{ currentLog.id }}</el-descriptions-item>
        <el-descriptions-item label="方法">
          <el-tag :type="getMethodType(currentLog.method)">{{ currentLog.method }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="路径" :span="2">{{ currentLog.path }}</el-descriptions-item>
        <el-descriptions-item label="状态码">
          <el-tag :type="getStatusType(currentLog.status_code)">{{ currentLog.status_code }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="响应时间">{{ currentLog.response_time }}s</el-descriptions-item>
        <el-descriptions-item label="IP地址">{{ currentLog.ip_address }}</el-descriptions-item>
        <el-descriptions-item label="用户">{{ currentLog.username || '匿名' }}</el-descriptions-item>
        <el-descriptions-item label="时间">{{ formatDate(currentLog.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="User Agent" :span="2">{{ currentLog.user_agent }}</el-descriptions-item>
        <el-descriptions-item label="请求数据" :span="2">
          <pre class="json-data" v-if="currentLog.request_data">{{ formatJson(currentLog.request_data) }}</pre>
          <span v-else>无</span>
        </el-descriptions-item>
        <el-descriptions-item label="响应数据" :span="2">
          <pre class="json-data" v-if="currentLog.response_data">{{ formatJson(currentLog.response_data) }}</pre>
          <span v-else>无</span>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getLogs, getLogsStats } from '../../api/admin'
import { ElMessage } from 'element-plus'

const logs = ref([])
const stats = ref({})
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const filterForm = ref({
  method: '',
  status_code: null
})

const detailVisible = ref(false)
const currentLog = ref(null)

const fetchLogs = async () => {
  loading.value = true
  try {
    const res = await getLogs({
      page: currentPage.value,
      per_page: pageSize.value,
      method: filterForm.value.method || undefined,
      status_code: filterForm.value.status_code || undefined
    })
    logs.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取日志失败')
  } finally {
    loading.value = false
  }
}

const fetchStats = async () => {
  try {
    const res = await getLogsStats()
    stats.value = res.data
  } catch (error) {
    console.error('获取统计失败', error)
  }
}

const resetFilter = () => {
  filterForm.value = {
    method: '',
    status_code: null
  }
  fetchLogs()
}

const showDetail = (row) => {
  currentLog.value = row
  detailVisible.value = true
}

const getMethodType = (method) => {
  const types = {
    'GET': 'success',
    'POST': 'primary',
    'PUT': 'warning',
    'DELETE': 'danger'
  }
  return types[method] || 'info'
}

const getStatusType = (code) => {
  if (code >= 200 && code < 300) return 'success'
  if (code >= 300 && code < 400) return 'warning'
  if (code >= 400 && code < 500) return 'danger'
  return 'info'
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN')
}

const formatJson = (data) => {
  if (!data) return ''
  try {
    const parsed = JSON.parse(data)
    return JSON.stringify(parsed, null, 2)
  } catch (e) {
    return data
  }
}

onMounted(() => {
  fetchLogs()
  fetchStats()
})
</script>

<style scoped>
.logs-page {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  color: #909399;
  margin-top: 5px;
}

.filter-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

pre {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  max-height: 200px;
}

pre.json-data {
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 300px;
  overflow-y: auto;
}
</style>
