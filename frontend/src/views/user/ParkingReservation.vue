<template>
  <div class="parking-reservation">
    <h2>预订车位</h2>
    <el-table :data="availableSpots" style="width: 100%" v-loading="loading">
      <el-table-column prop="spot_number" label="车位号" width="100" />
      <el-table-column prop="zone" label="分区" width="80" />
      <el-table-column prop="type" label="类型" width="100" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="reserve(row)">预约</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { getParkingSpots, updateParkingSpot } from '@/api/parking'
import { createOrder } from '@/api/orders'
import { ElMessage } from 'element-plus'

const spots = ref([])
const loading = ref(false)

const fetchSpots = async () => {
  loading.value = true
  try {
    const res = await getParkingSpots({ status: 'Available', per_page: 100 })
    spots.value = res.data || []
  } catch (e) {
    ElMessage.error(e.message || '获取车位失败')
  } finally {
    loading.value = false
  }
}

const availableSpots = ref([])

onMounted(async () => {
  await fetchSpots()
  availableSpots.value = spots.value
})

const reserve = async (spot) => {
  try {
    // 获取当前用户ID
    const userInfo = JSON.parse(localStorage.getItem('userInfo'))
    if (!userInfo || !userInfo.id) {
      ElMessage.error('请先登录')
      return
    }
    // 创建订单
    await createOrder({
      user_id: userInfo.id,
      spot_id: spot.id,
      start_time: new Date().toISOString(),
      status: '未支付',
      amount: 0
    })
    // 更新车位状态为Reserved
    await updateParkingSpot(spot.id, { status: 'Reserved' })
    ElMessage.success('预约成功，请前往订单页面支付')
    fetchSpots()
  } catch (e) {
    ElMessage.error(e.message || '预约失败')
  }
}
</script>
<style scoped>
.parking-reservation {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px #0001;
  padding: 32px 24px 24px 24px;
}
</style> 