<template>
  <div class="user-management-container table-card-gradient">
    <h2>用户管理</h2>
    
    <div class="action-bar">
      <el-button type="primary" @click="showAddModal">添加用户</el-button>
      <el-input
        v-model="searchKeyword"
        placeholder="搜索用户名或手机号"
        style="width: 300px"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">
            <el-icon><search /></el-icon>
          </el-button>
        </template>
      </el-input>
    </div>

    <el-table
      :data="userList"
      v-loading="loading"
      style="width: 100%"
    >
      <el-table-column prop="id" label="用户编号" min-width="100" />
      <el-table-column label="用户名" min-width="120">
        <template #default="{ row }">
          <span v-if="!row._showName">{{ row.name?.[0] + '**' }}</span>
          <span v-else>{{ row.name }}</span>
          <el-button type="text" size="small" @click="row._showName = !row._showName">{{ row._showName ? '隐藏' : '显示' }}</el-button>
        </template>
      </el-table-column>
      <el-table-column label="手机号" min-width="140">
        <template #default="{ row }">
          <span v-if="!row._showPhone">{{ row.phone?.slice(0,3) + '****' }}</span>
          <span v-else>{{ row.phone }}</span>
          <el-button type="text" size="small" @click="row._showPhone = !row._showPhone">{{ row._showPhone ? '隐藏' : '显示' }}</el-button>
        </template>
      </el-table-column>
      <el-table-column prop="email" label="邮箱" min-width="180" />
      <el-table-column label="密码" min-width="120">
        <template #default="{ row }">
          <span v-if="!row._showPwd">******</span>
          <span v-else>{{ row._showPwdVal || '******' }}</span>
          <el-button type="text" size="small" @click="showPassword(row)">{{ row._showPwd ? '隐藏' : '显示' }}</el-button>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{row}">
          <el-button size="small" @click="showEditModal(row)">编辑</el-button>
          <el-popconfirm
            title="确定要删除此用户吗？"
            @confirm="handleDelete(row.id)"
          >
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="pagination.current"
      v-model:page-size="pagination.pageSize"
      :total="pagination.total"
      :page-sizes="[10, 20, 50]"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="fetchUsers"
      @current-change="fetchUsers"
    />

    <!-- 添加/编辑用户模态框 -->
    <el-dialog
      v-model="modalVisible"
      :title="modalTitle"
      @closed="resetForm"
    >
      <el-form
        ref="formRef"
        :model="formState"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="name" required>
          <el-input v-model="formState.name" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone" required>
          <el-input v-model="formState.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formState.email" placeholder="请输入邮箱（可选）" />
        </el-form-item>
        <el-form-item label="密码" prop="password" :required="isAddMode">
          <el-input v-model="formState.password" placeholder="请输入密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="modalVisible = false">取消</el-button>
        <el-button type="primary" @click="handleModalOk">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, addUser, updateUser, deleteUser } from '@/api/users'

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0
})

// 数据状态
const userList = ref([])
const loading = ref(false)
const searchKeyword = ref('')
const modalVisible = ref(false)
const isAddMode = ref(true)
const modalTitle = ref('添加用户')
const hasError = ref(false)

// 字段中文名映射
const fieldLabelMap = {
  id: '用户编号',
  name: '用户名',
  phone: '手机号',
  role: '用户角色'
}

// 自动获取所有字段（不显示 password）
const dataKeys = computed(() => {
  if (userList.value.length === 0) return []
  return Object.keys(userList.value[0]).filter(key => !['password', 'password_hash'].includes(key))
})

// 表单状态
const formState = reactive({
  id: null,
  name: '',
  phone: '',
  email: '',
  password: '',
  role: 'user' // 默认普通用户
})

// 角色选项
const roleOptions = [
  { label: '普通用户', value: 'user' },
  { label: '管理员', value: 'admin' }
]

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度2-20个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { 
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号格式',
      trigger: 'blur'
    }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur', required: false }
  ],
  password: [
    { 
      required: isAddMode.value, 
      message: '请输入密码', 
      trigger: 'blur' 
    },
    { 
      min: 6, 
      message: '密码至少6个字符', 
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (!isAddMode.value && !value) {
          callback() // 编辑时密码可为空
        } else if (value && value.length < 6) {
          callback(new Error('密码至少6个字符'))
        } else {
          callback()
        }
      }
    }
  ],
  role: [
    { required: true, message: '请选择用户角色', trigger: 'change' }
  ]
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    loading.value = true
    hasError.value = false
    const params = {
      page: pagination.current,
      pageSize: pagination.pageSize,
      keyword: searchKeyword.value
    }
    const res = await getUsers(params)
    userList.value = (res?.list || []).map(user => ({
      ...user,
      _showName: false,
      _showPhone: false,
      _showPwd: false,
      _showPwdVal: '******'
    }))
    pagination.total = res?.total || 0
  } catch (error) {
    console.error('获取用户列表错误:', error)
    hasError.value = true
    userList.value = []
    if (error.response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
      router.push('/login')
    } else if (error.response?.status === 403) {
      ElMessage.error('权限不足，请联系管理员')
    } else {
      ElMessage.error(`获取用户列表失败: ${error.message || '未知错误'}`)
    }
  } finally {
    loading.value = false
  }
}

// 搜索用户
const handleSearch = () => {
  pagination.current = 1 // 搜索时重置到第一页
  fetchUsers()
}

// 显示添加用户模态框
const showAddModal = () => {
  isAddMode.value = true
  modalTitle.value = '添加用户'
  resetForm()
  modalVisible.value = true
}

// 显示编辑用户模态框
const showEditModal = (record) => {
  isAddMode.value = false
  modalTitle.value = '编辑用户'
  Object.assign(formState, record)
  formState.password = '' // 编辑时密码不显示
  modalVisible.value = true
}

// 提交表单
const handleModalOk = async () => {
  try {
    if (isAddMode.value) {
      if (!formState.password) {
        ElMessage.error('请填写密码')
        return
      }
      await addUser(formState)
      ElMessage.success('用户添加成功')
    } else {
      await updateUser(formState.id, formState)
      ElMessage.success('用户更新成功')
    }
    modalVisible.value = false
    resetForm()
    fetchUsers()
  } catch (error) {
    ElMessage.error('操作失败')
    console.error(error)
  }
}

// 删除用户
const handleDelete = async (userId) => {
  try {
    await deleteUser(userId)
    ElMessage.success('用户删除成功')
    fetchUsers()
  } catch (error) {
    ElMessage.error('删除用户失败')
    console.error(error)
  }
}

// 重置表单
const resetForm = () => {
  formState.id = null
  formState.name = ''
  formState.phone = ''
  formState.email = ''
  formState.password = ''
}

// 密码显示逻辑（确保 _showPwd 字段响应式）
const showPassword = (row) => {
  if (!('_showPwd' in row)) {
    row._showPwd = false
  }
  row._showPwd = !row._showPwd
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.user-management-container {
  padding: 20px;
  background: #fff;
  border-radius: 4px;
}

.action-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.table-card-gradient {
  background: linear-gradient(120deg, #f0f9ff 60%, #e0e7ff 100%);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(80,80,160,0.10);
  padding: 32px 24px;
  margin-bottom: 32px;
  position: relative;
}
.el-table tr:nth-child(even) {
  background: #f0f9ff;
}
</style>