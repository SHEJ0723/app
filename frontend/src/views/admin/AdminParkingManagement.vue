<template>
  <div class="admin-parking-management">
    <h2>停车场管理</h2>
    
    <!-- 搜索和过滤 -->
    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="分区">
        <el-select v-model="searchForm.zone" placeholder="选择分区" clearable>
          <el-option v-for="zone in zones" :key="zone.value" :label="zone.label" :value="zone.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="类型">
        <el-select v-model="searchForm.type" placeholder="选择类型" clearable>
          <el-option v-for="type in types" :key="type.value" :label="type.label" :value="type.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="searchForm.status" placeholder="选择状态" clearable>
          <el-option v-for="status in statuses" :key="status.value" :label="status.label" :value="status.value" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadParkingSpots">搜索</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 添加停车位按钮 -->
    <el-button type="primary" @click="showAddDialog">添加停车位</el-button>

    <!-- 停车位列表 -->
    <el-table :data="parkingSpots" style="width: 100%; margin-top: 20px" v-loading="loading">
      <el-table-column
        v-for="key in dataKeys"
        :key="key"
        :prop="key"
        :label="fieldLabelMap[key] || key"
        :min-width="100"
      >
        <template v-if="key === 'status'" #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
        </template>
        <template v-else-if="key === 'is_active'" #default="{ row }">
          <el-switch v-model="row.is_active" @change="handleStatusChange(row)" />
        </template>
        <template v-else #default="{ row }">
          {{ row[key] }}
        </template>
      </el-table-column>
      <!-- 操作列 -->
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      class="pagination"
    />

    <!-- 添加/编辑对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '添加停车位' : '编辑停车位'"
      v-model="dialogVisible"
      width="500px"
      @closed="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="车位号" prop="spot_number">
          <el-input 
            v-model="form.spot_number" 
            :disabled="dialogType === 'edit'"
            placeholder="请输入车位号，如A001"
          />
        </el-form-item>
        <el-form-item label="分区" prop="zone">
          <el-select v-model="form.zone" placeholder="选择分区">
            <el-option v-for="zone in zones" :key="zone.value" :label="zone.label" :value="zone.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="选择类型">
            <el-option v-for="type in types" :key="type.value" :label="type.label" :value="type.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="选择状态">
            <el-option v-for="status in statuses" :key="status.value" :label="status.label" :value="status.value" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getParkingSpots,
  createParkingSpot,
  updateParkingSpot,
  deleteParkingSpot
} from '@/api/parking'

// 数据
const parkingSpots = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref(null)

// 字段中文名映射（可选）
const fieldLabelMap = {
  spot_number: '车位号',
  zone: '分区',
  type: '类型',
  status: '状态',
  is_active: '是否启用'
}

// 自动获取所有字段
const dataKeys = computed(() => {
  if (parkingSpots.value.length === 0) return []
  // 过滤掉不需要展示的字段（如 id、created_at、updated_at）
  return Object.keys(parkingSpots.value[0]).filter(
    key => !['id', 'created_at', 'updated_at'].includes(key)
  )
})

// 选项数据
const zones = [
  { value: 'A', label: 'A区' },
  { value: 'B', label: 'B区' },
  { value: 'C', label: 'C区' }
]

const types = [
  { value: '普通', label: '普通' },
  { value: '新能源', label: '新能源' },
  { value: '无障碍', label: '无障碍' }
]

const statuses = [
  { value: '空闲', label: '空闲' },
  { value: '占用', label: '占用' },
  { value: '维修', label: '维修' }
]

// 搜索表单
const searchForm = reactive({
  zone: '',
  type: '',
  status: ''
})

// 表单数据
const form = reactive({
  id: '',
  spot_number: '',
  zone: '',
  type: '',
  status: '空闲'
})

// 表单验证规则
const rules = {
  spot_number: [
    { required: true, message: '请输入车位号', trigger: 'blur' },
    { pattern: /^[A-Z0-9]{1,10}$/, message: '车位号只能包含大写字母和数字，长度1-10', trigger: 'blur' }
  ],
  zone: [
    { required: true, message: '请选择分区', trigger: 'change' }
  ],
  type: [
    { required: true, message: '请选择类型', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 生命周期
onMounted(() => {
  loadParkingSpots()
})

// 方法
const loadParkingSpots = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      ...searchForm
    }
    const response = await getParkingSpots(params)
    parkingSpots.value = response.data
    total.value = response.total
  } catch (error) {
    console.error('获取车位列表失败:', error)
    ElMessage.error(error.message || '获取车位列表失败')
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  currentPage.value = 1
  loadParkingSpots()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  loadParkingSpots()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  loadParkingSpots()
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  form.spot_number = ''
  form.zone = ''
  form.type = ''
  form.status = '空闲'
}

const showAddDialog = () => {
  dialogType.value = 'add'
  resetForm()
  dialogVisible.value = true
}

const showEditDialog = (row) => {
  dialogType.value = 'edit'
  Object.keys(form).forEach(key => {
    form[key] = row[key]
  })
  form.id = row.id
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      const loadingInstance = ElMessage({
        message: '正在提交...',
        duration: 0,
        icon: 'loading'
      })
      try {
        if (dialogType.value === 'add') {
          await createParkingSpot(form)
          ElMessage.success('添加成功')
        } else {
          await updateParkingSpot(form.id, form)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        setTimeout(() => {
          loadParkingSpots()
        }, 1000)
      } catch (error) {
        console.error('提交表单失败:', error)
        let errorMsg = '操作失败'
        if (error.response) {
          if (error.response.data.message) {
            errorMsg = error.response.data.message
          } else if (error.response.status === 400) {
            errorMsg = '请求参数错误'
          } else if (error.response.status === 404) {
            errorMsg = '停车位不存在'
          }
        }
        ElMessage.error(errorMsg)
      } finally {
        loadingInstance.close()
      }
    }
  })
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该停车位吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteParkingSpot(row.id)
      ElMessage.success('删除成功')
      loadParkingSpots()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error(error.message || '删除失败')
    }
  })
}

const handleStatusChange = async (row) => {
  try {
    await updateParkingSpot(row.id, { is_active: row.is_active })
    ElMessage.success('状态更新成功')
  } catch (error) {
    console.error('状态更新失败:', error)
    ElMessage.error(error.message || '状态更新失败')
    row.is_active = !row.is_active // 恢复原状态
  }
}

const getStatusType = (status) => {
  const types = {
    '空闲': 'success',
    '占用': 'warning',
    '维修': 'danger'
  }
  return types[status] || 'info'
}
</script>

<style scoped>
.admin-parking-management {
  padding: 20px;
}

.search-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.el-select {
  width: 100%;
  min-width: 120px;
}
</style> 