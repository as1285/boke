<template>
  <div class="post-edit-page">
    <el-page-header @back="$router.back()" :title="isEdit ? '编辑文章' : '新建文章'" />
    
    <el-card class="edit-card">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="文章标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文章标题" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类">
              <el-select v-model="form.category_id" placeholder="选择分类" clearable style="width: 100%">
                <el-option
                  v-for="cat in categories"
                  :key="cat.id"
                  :label="cat.name"
                  :value="cat.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="标签">
              <el-select v-model="form.tag_ids" multiple placeholder="选择标签" style="width: 100%">
                <el-option
                  v-for="tag in tags"
                  :key="tag.id"
                  :label="tag.name"
                  :value="tag.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="文章摘要">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="2"
            placeholder="请输入文章摘要（可选）"
          />
        </el-form-item>
        
<el-form-item label="文章内容" prop="content">
  <MavonEditor
    v-model="form.content"
    :toolbars="toolbars"
    placeholder="请输入文章内容，支持Markdown格式"
    style="min-height: 500px"
  />
</el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="form.is_published">立即发布</el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '创建文章' }}
          </el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, defineAsyncComponent } from 'vue'
import 'mavon-editor/dist/css/index.css'
const MavonEditor = defineAsyncComponent(() => import('mavon-editor'))
import { useRoute, useRouter } from 'vue-router'
import { getCategories, getTags, createPost, updatePost, getPost } from '../../api/posts'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const postId = computed(() => route.params.id)

const formRef = ref()
const loading = ref(false)
const categories = ref([])
const tags = ref([])

const form = reactive({
  title: '',
  content: '',
  summary: '',
  category_id: null,
  tag_ids: [],
  is_published: false
})

const rules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' }
  ]
}

// Markdown编辑器工具栏配置
const toolbars = {
  bold: true,
  italic: true,
  header: true,
  underline: true,
  strikethrough: true,
  mark: true,
  superscript: true,
  subscript: true,
  quote: true,
  ol: true,
  ul: true,
  link: true,
  imagelink: true,
  code: true,
  table: true,
  fullscreen: true,
  readmodel: true,
  htmlcode: true,
  help: true,
  undo: true,
  redo: true,
  trash: true,
  save: false,
  navigation: true,
  alignleft: true,
  aligncenter: true,
  alignright: true,
  subfield: true,
  preview: true
}

const fetchCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch (error) {
    console.error('获取分类失败', error)
  }
}

const fetchTags = async () => {
  try {
    const res = await getTags()
    tags.value = res.data
  } catch (error) {
    console.error('获取标签失败', error)
  }
}

const fetchPost = async () => {
  if (!isEdit.value) return
  
  try {
    // 注意：这里需要slug来获取文章，但编辑页面使用id
    // 实际项目中可能需要调整API
    const res = await getPost(postId.value)
    const post = res.data
    form.title = post.title
    form.content = post.content
    form.summary = post.summary
    form.category_id = post.category?.id
    form.tag_ids = post.tags?.map(t => t.id) || []
    form.is_published = post.is_published
  } catch (error) {
    ElMessage.error('获取文章失败')
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  loading.value = true
  try {
    if (isEdit.value) {
      await updatePost(postId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createPost(form)
      ElMessage.success('创建成功')
    }
    router.push('/admin/posts')
  } catch (error) {
    // 错误已在请求拦截器中处理
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
  fetchTags()
  fetchPost()
})
</script>

<style scoped>
.post-edit-page {
  padding: 20px;
}

.edit-card {
  margin-top: 20px;
}
</style>
