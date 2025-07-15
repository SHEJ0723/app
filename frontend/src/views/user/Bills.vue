<template>
  <div class="bills-view">
    <h2>收费明细</h2>
    <el-table :data="bills" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="账单号" width="100" />
      <el-table-column prop="order_id" label="订单号" width="100" />
      <el-table-column prop="amount" label="金额(元)" width="100" />
      <el-table-column prop="pay_time" label="支付时间" width="180" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column prop="pay_method" label="支付方式" width="100" />
    </el-table>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { getBills } from '@/api/bills'
import { ElMessage } from 'element-plus'

const bills = ref([])
const loading = ref(false)

const fetchBills = async () => {
  loading.value = true
  try {
    const res = await getBills()
    bills.value = res.data || []
  } catch (e) {
    ElMessage.error(e.message || '获取账单失败')
  } finally {
    loading.value = false
  }
}

onMounted(fetchBills)
</script>
<style scoped>
.bills-view {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px #0001;
  padding: 32px 24px 24px 24px;
}
</style> 