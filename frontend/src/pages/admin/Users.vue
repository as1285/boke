<template>
  <div class="users-page">
    <h2>用户管理</h2>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.total_users || 0 }}</div>
          <div class="stat-label">总用户数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.admin_count || 0 }}</div>
          <div class="stat-label">管理员数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.today_registered || 0 }}</div>
          <div class="stat-label">今日注册</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.active_users || 0 }}</div>
          <div class="stat-label">活跃用户(7天)</div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 用户表格 -->
    <el-card>
      <el-table :data="users" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="email" label="邮箱" show-overflow-tooltip />
        <el-table-column prop="is_admin" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_admin ? 'danger' : 'info'" size="small">
              {{ row.is_admin ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="post_count" label="文章数" width="90" />
        <el-table-column prop="comment_count" label="评论数" width="90" />
        <el-table-column prop="created_at" label="注册时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="最近登录" width="180">
          <template #default="{ row }">
            <div v-if="row.last_log">
              <div>{{ row.last_log.ip_address }}</div>
              <div class="text-gray">{{ formatDate(row.last_log.created_at) }}</div>
            </div>
            <span v-else class="text-gray">无记录</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button 
              size="small" 
              :type="row.is_admin ? 'warning' : 'primary'"
              @click="toggleAdmin(row)"
              :disabled="row.id === currentUserId"
            >
              {{ row.is_admin ? '取消管理员' : '设为管理员' }}
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="deleteUser(row)"
              :disabled="row.id === currentUserId"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchUsers"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '../../stores/user'
import { getUsers, getUsersStats, deleteUser as deleteUserApi, toggleUserAdmin } from '../../api/admin'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const currentUserId = computed(() => userStore.userInfo?.id)

const users = ref([])
const stats = ref({})
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await getUsers({
      page: currentPage.value,
      per_page: pageSize.value
    })
    users.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const fetchStats = async () => {
  try {
    const res = await getUsersStats()
    stats.value = res.data
  } catch (error) {
    console.error('获取统计失败', error)
  }
}

const toggleAdmin = async (row) => {
  const action = row.is_admin ? '取消管理员权限' : '设为管理员'
  try {
    await ElMessageBox.confirm(`确定要${action}用户 "${row.username}" 吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await toggleUserAdmin(row.id)
    ElMessage.success('修改成功')
    fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('修改失败')
    }
  }
}

const deleteUser = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除用户 "${row.username}" 吗？此操作不可恢复！`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'danger'
    })
    
    await deleteUserApi(row.id)
    ElMessage.success('删除成功')
    fetchUsers()
    fetchStats()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchUsers()
  fetchStats()
})
</script>

<style scoped>
.users-page {
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.text-gray {
  color: #909399;
  font-size: 12px;
}
</style>
