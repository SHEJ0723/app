<template>
  <div class="orders-view">
    <h2>订单查看</h2>
    <el-table :data="orders" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="订单号" width="100" />
      <el-table-column prop="spot_id" label="车位ID" width="80" />
      <el-table-column prop="start_time" label="开始时间" width="180" />
      <el-table-column prop="end_time" label="结束时间" width="180" />
      <el-table-column prop="amount" label="金额(元)" width="100" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column prop="pay_method" label="支付方式" width="100" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button v-if="row.status !== '已完成'" size="small" @click="pay(row, '支付宝')">支付宝支付</el-button>
          <el-button v-if="row.status !== '已完成'" size="small" type="success" @click="pay(row, '微信')">微信支付</el-button>
          <el-tag v-else type="success">已支付</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { getOrders, payOrder } from '@/api/orders'
import { ElMessage } from 'element-plus'

const orders = ref([])
const loading = ref(false)

const fetchOrders = async () => {
  loading.value = true
  try {
    const res = await getOrders()
    orders.value = res.data || []
  } catch (e) {
    ElMessage.error(e.message || '获取订单失败')
  } finally {
    loading.value = false
  }
}

const pay = async (row, method) => {
  try {
    await payOrder(row.id, method)
    ElMessage.success('支付成功')
    fetchOrders()
  } catch (e) {
    ElMessage.error(e.message || '支付失败')
  }
}

onMounted(fetchOrders)
</script>
<style scoped>
.orders-view {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px #0001;
  padding: 32px 24px 24px 24px;
}
</style> 