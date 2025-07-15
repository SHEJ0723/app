<template>
  <div class="admin-bills-container">
    <el-card>
      <template #header>
        <h3>账单管理</h3>
      </template>
      <div class="action-bar">
        <el-button type="primary" @click="showAddModal">新增账单</el-button>
      </div>
      <el-table :data="bills" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="账单号" width="100" />
        <el-table-column prop="user_id" label="用户ID" width="100" />
        <el-table-column prop="order_id" label="订单号" width="100" />
        <el-table-column prop="amount" label="金额(元)" width="100" />
        <el-table-column prop="pay_time" label="支付时间" width="180" />
        <el-table-column prop="status" label="状态" width="100" />
        <el-table-column prop="pay_method" label="支付方式" width="100" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-popconfirm title="确定要删除该账单吗？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog v-model="addModalVisible" title="新增账单" @closed="resetForm">
        <el-form :model="form" label-width="80px">
          <el-form-item label="用户ID" required>
            <el-input v-model="form.user_id" />
          </el-form-item>
          <el-form-item label="订单号" required>
            <el-input v-model="form.order_id" />
          </el-form-item>
          <el-form-item label="金额(元)" required>
            <el-input v-model="form.amount" />
          </el-form-item>
          <el-form-item label="支付时间">
            <el-date-picker v-model="form.pay_time" type="datetime" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="form.status">
              <el-option label="未支付" value="未支付" />
              <el-option label="已支付" value="已支付" />
            </el-select>
          </el-form-item>
          <el-form-item label="支付方式">
            <el-select v-model="form.pay_method">
              <el-option label="支付宝" value="支付宝" />
              <el-option label="微信" value="微信" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="addModalVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAdd">确定</el-button>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { getBills, createBill, deleteBill } from '@/api/bills'
import { ElMessage } from 'element-plus'

const bills = ref([])
const loading = ref(false)
const addModalVisible = ref(false)
const form = ref({ user_id: '', order_id: '', amount: '', pay_time: '', status: '未支付', pay_method: '' })

const fetchBills = async () => {
  loading.value = true
  try {
    const res = await getBills({ per_page: 100 })
    bills.value = res.data || []
  } catch (e) {
    ElMessage.error(e.message || '获取账单失败')
  } finally {
    loading.value = false
  }
}

const showAddModal = () => {
  addModalVisible.value = true
  resetForm()
}
const resetForm = () => {
  form.value = { user_id: '', order_id: '', amount: '', pay_time: '', status: '未支付', pay_method: '' }
}
const handleAdd = async () => {
  try {
    await createBill(form.value)
    ElMessage.success('新增成功')
    addModalVisible.value = false
    fetchBills()
  } catch (e) {
    ElMessage.error(e.message || '新增失败')
  }
}
const handleDelete = async (id) => {
  try {
    await deleteBill(id)
    ElMessage.success('删除成功')
    fetchBills()
  } catch (e) {
    ElMessage.error(e.message || '删除失败')
  }
}
onMounted(fetchBills)
</script>
<style scoped>
.admin-bills-container {
  max-width: 1100px;
  margin: 30px auto;
  padding: 20px;
}
.action-bar {
  margin-bottom: 16px;
}
</style> 