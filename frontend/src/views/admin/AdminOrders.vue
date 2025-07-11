<template>
  <div class="admin-orders-container">
    <el-card>
      <template #header>
        <h3>车辆进出记录与订单补录</h3>
      </template>
      <el-form :inline="true" style="margin-bottom: 20px;">
        <el-form-item label="车牌号">
          <el-input v-model="search.plate" placeholder="请输入车牌号" />
        </el-form-item>
        <el-form-item label="时间">
          <el-date-picker v-model="search.time" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="orders" style="width: 100%">
        <el-table-column prop="id" label="订单号" width="180" />
        <el-table-column prop="plate" label="车牌号" width="120" />
        <el-table-column prop="inTime" label="入场时间" width="180" />
        <el-table-column prop="outTime" label="出场时间" width="180" />
        <el-table-column prop="amount" label="金额(元)" width="120" />
        <el-table-column label="操作" width="120">
          <template #default>
            <el-button size="small">补录</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>
<script setup>
import { ref } from 'vue'
// 假设有订单API文件，后续可调整路径
import api from '@/api/index'
const search = ref({ plate: '', time: [] })
const orders = ref([])

const handleSearch = async () => {
  try {
    // 构造查询参数
    const params = {}
    if (search.value.plate) params.plate = search.value.plate
    if (search.value.time && search.value.time.length === 2) {
      params.start_time = search.value.time[0]
      params.end_time = search.value.time[1]
    }
    // 假设后端接口为 /api/orders，GET请求
    const res = await api.get('/api/orders', { params })
    // 兼容不同返回结构
    orders.value = res.data || res.orders || []
  } catch (e) {
    orders.value = []
    // 可用ElMessage弹窗提示
    // ElMessage.error(e.message || '查询失败')
    console.error('查询失败', e)
  }
}
// 页面加载时可自动查询一次
handleSearch()
</script>
<style scoped>
.admin-orders-container {
  max-width: 1100px;
  margin: 30px auto;
  padding: 20px;
}
</style> 